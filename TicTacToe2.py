import sys
import math
import random, copy
import numpy as np

DRAW, NEITHER, MINE, OPP = -2 , -1 , 0 , 1
TYPE_TURN = { -2 : 'D' , -1 : 'N'  , 0 : 'M' , 1 : 'O' }

FIRST_TURN = {
    0 : [ 0 ] , 1 : [ 3 , 5 , 7 ] , 2 : [ 2 ] ,
    3 : [ 1 , 5 , 7 ] , 4 : [ 4 ] , 5 : [ 1 , 3 , 7 ] ,
    6 : [ 6 ] , 7 : [ 1 , 3 , 5 ] , 8 : [ 8 ] }

NB_RAND_FIRST = 700 #1000
NB_RAND_AFTER = 30 #78

t_str = lambda obj : f'{str(obj)} {TYPE_TURN[obj]}'

f_row = lambda obj : obj.param[0]
f_col = lambda obj : obj.param[1]
f_prop = lambda obj : obj.param[2]

f_win = lambda obj : obj[0]
f_all = lambda obj : obj[1]

TYPE_STR1 = { DRAW : '# # #' , NEITHER : '     ' ,  MINE : '     ' , OPP : '     ' }
TYPE_STR2 = { DRAW : '#   #' , NEITHER : '     ' ,  MINE : '  X  ' , OPP : '  O  ' }
TYPE_STR3 = { DRAW : '# # #' , NEITHER : '     ' ,  MINE : '     ' , OPP : '     ' }

SIMPLEST_STR = { NEITHER : '-' , MINE : 'X' , OPP : 'O' }

TUPLE_WIN = (
    (0,1,2) , (3,4,5) , (6,7,8) ,
    (0,3,6) , (1,4,7) , (2,5,8) ,
    (0,4,8) , (2,4,6)
)

class Neuron():

    def __init__(self,clone):
        pass

    def __str__(self):
        return f'{self.row} {self.col}'

    def setup( self , ind1 , ind2 ):
        self.row = (ind1 // 3) * 3 + (ind2 // 3)
        self.col = (ind1 % 3) * 3 + (ind2 % 3)
        self.ind1, self.ind2 = ind1, ind2

def victory_check2( obj , ind1 , owner ):
    for ind2 in TUPLE_WIN:
        if obj[ (ind1 , ind2[0]) ] != owner :   continue
        if obj[ (ind1 , ind2[1]) ] != owner :   continue
        if obj[ (ind1 , ind2[2]) ] != owner :   continue
        return owner

    for i2 in range(9):
        if obj[ (ind1 , i2 ) ] == NEITHER :     return NEITHER

    return DRAW

def victory_check3( obj , owner ):
    for ind1 in TUPLE_WIN:
        if obj[ ind1[0] ] != owner :   continue
        if obj[ ind1[1] ] != owner :   continue
        if obj[ ind1[2] ] != owner :   continue
        return owner

    for i1 in range(9):
        if obj[ i1 ] == NEITHER :     return NEITHER

    return DRAW

def coord_pToIndex( inrow , incol ):
    ind1 = (inrow // 3) * 3 + (incol // 3)
    ind2 = (inrow % 3) * 3 + (incol % 3)
    return ( ind1 , ind2 )

class TicTacToe():

    def __init__(self,clone):
        if clone is None :
            self._secret , self._state, self._predict = {}, {}, []
            self._mine , self._first , self._over = {} , 4 , NEITHER

            for ind1 in range(9):
                self._secret[ ind1 ] = NEITHER

            for ind1 in range(9):
                for ind2 in range(9):
                    self._state[ ( ind1 , ind2 )] = NEITHER

        elif clone is not None :
            self._predict = copy.copy( clone._predict )
            self._secret = copy.copy( clone._secret )
            self._state = copy.copy( clone._state )

            self._mine = copy.copy( clone._mine )
            self._first = clone._first
            self._over = clone._over

    def __str__(self):
        out = f'GAME : {TYPE_TURN[self._over]}'
        out = f'{out}\n  0 1 2 3 4 5 6 7 8 0 1 2 3 4 5 6 7 8'

        for row in range(3):
            out1 = f'{row * 3 + 0}'
            out2 = f'{row * 3 + 1}'
            out3 = f'{row * 3 + 2}'
            for ind1 in range( 3 * row , 3 * row + 3 ):
                _ = self._secret[ind1]

                out1 = f'{out1} {TYPE_STR1[_]}'
                out2 = f'{out2} {TYPE_STR2[_]}'
                out3 = f'{out3} {TYPE_STR3[_]}'

            for ind1 in range( 3 * row , 3 * row + 3 ):
                #if self._secret[ind1] == NEITHER or self._secret[ind1] == DRAW :
                for ind2 in range(0,3):
                    _ = self._state[ (ind1, ind2) ]
                    out1 = f'{out1} {SIMPLEST_STR[_]}'
                for ind2 in range(3,6):
                    _ = self._state[ (ind1, ind2) ]
                    out2 = f'{out2} {SIMPLEST_STR[_]}'
                for ind2 in range(6,9):
                    _ = self._state[ (ind1, ind2) ]
                    out3 = f'{out3} {SIMPLEST_STR[_]}'
                #else :
                #out1 = f'{out1} {TYPE_STR1[NEITHER]}'
                #out2 = f'{out2} {TYPE_STR2[NEITHER]}'
                #out3 = f'{out3} {TYPE_STR3[NEITHER]}'

            out = f'{out}\n{out1}\n{out2}\n{out3}'

        return out

    def real_update( self , row , col , owner ) :

        _ = self.update( row , col , owner )

    def update( self , row , col , owner ):
        ind1 = (row // 3) * 3 + (col // 3)
        ind2 = (row % 3) * 3 + (col % 3)

        #   DELETE THIS POSSIBILITY
        del self._mine[ ( ind1 , ind2 ) ]
        self._first = ind2

        #   MARK
        self._state[ ( ind1 , ind2 ) ] = owner

        _ = victory_check2 ( self._state , ind1 , owner )

        if _ != NEITHER :

            #   MARK
            for i2 in range(9):
                if (ind1,i2) in self._mine :
                    del self._mine[ ind1 , i2 ]

            self._secret[ ind1 ] = _

            self._over = victory_check3 ( self._secret , owner )

        return _

    def possibility( self , own , ind2 ):

        _ = ind2

        #   TODO: Simplify
        s1 = frozenset([(_,0),(_,1),(_,2),(_,3),(_,4),(_,5),(_,6),(_,7),(_,8)])

        s1 = s1.intersection(self._mine)

        if self._secret[ind2] == NEITHER :
            n1 = []
            for _ in s1:
                n1.append( self._mine[_] )

            return n1

        else :

            _ = [c1 for c1 in self._secret.values()]

            n1 = []
            for _ in self._mine.values():
                n1.append(_)

            return n1

    def __eq__( self , o ):
        return True if self._state == o._state else False

def mcts_generate( mcts_parent , n1 ):
    childs = []
    status_mine = NEITHER
    status_opp = NEITHER

    ochild1 = MonteCarloTreeSearch( mcts_parent )
    ochild1._state._predict.append( n1 )
    ochild1._state.update( n1.row , n1.col , MINE )

    #   ADD MIN MAX
    if ochild1._state._secret[n1.ind1] == MINE :

        if ochild1._state._over == MINE :
            ochild1._min_max = 0
        else :
            ochild1._min_max = ochild1._min_max - 1

        #print('MCTS GENERATE MINE',file=sys.stderr)
        #print(ochild1._state,file=sys.stderr)

    s1 = frozenset([(n1.ind2,0),(n1.ind2,1),(n1.ind2,2),(n1.ind2,3),(n1.ind2,4),(n1.ind2,5),(n1.ind2,6),(n1.ind2,7),(n1.ind2,8)])

    s1 = s1.intersection(ochild1._state._mine)

    #   RULE OF TIC-TAC-TOE
    if len(s1) == 0 :
        s1 = list(ochild1._state._mine.keys())

    #   LAST CASE
    if len(s1) == 0 :
        childs.append( ochild1 )

    max_choice_found = []
    for k1 in s1:

        child = MonteCarloTreeSearch( ochild1 )
        m1 = ochild1._state._mine[k1]
        child._state.update( m1.row , m1.col , OPP )

        if child._state._secret[m1.ind1] == OPP :

            max_choice_found.append( child )

            #if child._state._over == OPP :
            #    child._min_max = 0
            #else :
            #    child._min_max = child._min_max - 1

        childs.append(child)

    if len(max_choice_found) > 0 :

        for c1 in childs :
            if c1 not in max_choice_found :
                c1._result = [ 0, 10 ]

    return childs

class MonteCarloTreeSearch():

    def __init__(self,clone):
        self._children = []
        self._result = [ 0 , 0 ]

        if clone is not None:
            self._parent = clone
            clone._children.append(self)
            self._state = TicTacToe(clone._state)
            self._min_max = clone._min_max

        else:
            self._parent = None
            self._state = None
            self._min_max = 9

    @property
    def n(self):
        return f_all(self._result)

    @property
    def w(self):
        return f_win(self._result)

    #def generate( self , first ):
    def generate( self ):

        if self._state._secret[ self._state._first ] != NEITHER :

            s1 = list( self._state._mine.keys() )

        else :

            _ = self._state._first

            s1 = frozenset([(_,0),(_,1),(_,2),(_,3),(_,4),(_,5),(_,6),(_,7),(_,8)])

            s1 = s1.intersection(self._state._mine)

            #   BEST CHOICE
            if len(s1) == 9 :

                t1 = FIRST_TURN[ _ ]
                s2 = []

                for i1 in t1 :

                    s2.append( ( _ , i1 ) )

                s1 = s1.intersection( s2 )


        if len(self._children) == 0 :

            childs = []

            for _ in s1:

                n1 = self._state._mine[_]

                childs.extend( mcts_generate( self , n1 ) )

            self._children = []
            self._children.extend(childs)

        else :

            childs = []

            for m1 in self._children :
                n1 = m1._state._predict[0]
                if (n1.ind1,n1.ind2) in s1 :
                    del s1[ (n1.ind1 , n1.ind2) ]
                    childs.append(m1)

            for _ in s1 :

                n1 = self._state._mine

                childs.extend( mcts_generate( self , n1 ) )

            self._children = []
            self._children.extend(childs)

    def best_child( self, c_parameter ):
        #  Upper Confidence Bounds (UCB1) formula
        _ = self

        while len(_._children) > 0 :

            children, minmax, find = [] , 0 , False #   0 --> OVER, 9 --> START GAME
            isexpand = False

            while minmax < 10 :
                for c1 in _._children :

                    if c1._min_max == minmax :
                        children.append( c1 )
                        find = True

                    if c1.n == 0 :
                        isexpand = True

                if find == True :
                    break

                minmax = minmax + 1

            if isexpand == True :
                return _

            weight = [
                (c.w / c.n) + c_parameter * math.sqrt( (2 * math.log2(_.n) / c.n ) )
                for c in children
            ]

            _ = children[ np.argmax( weight ) ]

            #check = sum( [ 1 for c in _._children if c.n == 0 ])

            #if check > 0 : return _

            #weight = [
            #    (c.w / c.n) + c_parameter * math.sqrt( (2 * math.log2(_.n) / c.n ) )
            #    for c in _._children
            #]

            #_ = _._children[ np.argmax( weight ) ]

        return _

    def expand_turns(self):
        #   SELECT NEXT/RANDOM ACTION
        #   COMPUTE STATE
        if self._state._over != NEITHER :
            return self

        if len(self._children) == 0 :
            self.generate( )

        #childs = [c for c in self._children if c.n == 0 ]
        #return childs[0]

        children, minmax, find = [] , 0 , False #   0 --> OVER, 9 --> START GAME
        isexpand = False

        while minmax < 10 :

            for c1 in self._children :

                if c1._min_max == minmax and c1.n == 0 :

                    children.append( c1 )
                    find = True

            if find == True :
                break

            minmax = minmax + 1

        if len(children) == 0 :

            print('DEBUG >>> EXPAND',file=sys.stderr)

            for c1 in self._children :

                if c1._state._over == MINE :
                    print(c1._state,file=sys.stderr)
                    return c1


        #print('DEBUG >>> EXPAND',file=sys.stderr)
        #print(children[0]._state,file=sys.stderr)
        return children[0]
        #if len(childs) == 0 :
        #    self._state._first = -1
        #    self.generate()
        #    childs = [c for c in self._children if c.n == 0 ]

        #   RANDOM CAN BE ADD


    def randomseq( self ):
        TURN = 80
        ROLLOUT_TURN = MINE
        rollout_state = TicTacToe(self._state)

        while rollout_state._over == NEITHER and TURN > 0 :

            TURN = TURN - 1

            _ = rollout_state.possibility( ROLLOUT_TURN , rollout_state._first )

            sel = random.choice(_)

            sel_row , sel_col = sel.row , sel.col

            rollout_state.update( sel_row , sel_col , ROLLOUT_TURN )

            ROLLOUT_TURN = MINE if ROLLOUT_TURN == OPP else OPP

        return [ 1 , 1 ] if rollout_state._over == MINE else [ 0 , 1 ]

    def backpropagate(self, result):
        self._result[0] = f_win(self._result) + f_win(result)
        self._result[1] = f_all(self._result) + f_all(result)
        _ = self._parent
        while _ is not None :
            _._result[0] = f_win(_._result) + f_win(result)
            _._result[1] = f_all(_._result) + f_all(result)
            _ = _._parent

    def predict_update(self):

        for c1 in self._children:
            c1.predict_update()

        self._state._predict.pop(0)

    def update( self, mine_row , mine_col , opp_row , opp_col ):
        self._state.real_update( mine_row , mine_col , MINE )
        self._state.real_update( opp_row , opp_col , OPP )

        _ = None
        for _ in self._children :
            if _._state == self._state :
                return _

        self._state._predict = []
        self._parent = None
        self._children = []
        self._result = [ 0 , 1 ]
        return self

if __name__ == '__main__':

    # INIT NEURON
    __mine__action__ = {}
    __opp__action__ = {}

    for ind1 in range(9):
        for ind2 in range(9):
            _ = Neuron(None)
            _.setup( ind1 , ind2 )
            __mine__action__[ (ind1,ind2) ] = _
            __opp__action__[ (ind1,ind2) ] = _

    __mine__ = TicTacToe(None)

    #   INIT ALL ACTION
    __mine__._mine = copy.copy( __mine__action__ )
    __mine__._opp = copy.copy( __opp__action__ )

    #   FIRST TURN
    _ = [int(i) for i in input().split()] + [OPP]
    if _[0] != -1 :
        __mine__.update( _[0] , _[1] , _[2] )

    #   POSSIBILITY
    for i in range(int(input())):
        _ = [int(j) for j in input().split()]

    # MONTE-CARLO TREE SEARCH INITIALIZATION
    __mine__mcts__ = MonteCarloTreeSearch(None)
    __mine__mcts__._state = __mine__

    for i in range(NB_RAND_FIRST):

        __children__ = __mine__mcts__.best_child( 1.4 )

        __children__ = __children__.expand_turns()

        _ = __children__.randomseq()

        __children__.backpropagate( _ )

    _ = np.argmax( [ c.w / c.n for c in __mine__mcts__._children ] )

    _ = __mine__mcts__._children[ _ ]

    _ = _._state._predict[0]

    print(_)

    # AFTER FIRST TURN
    while True:
        #   OPPONENT ACTION
        _ = [_.row] + [_.col] + [int(i) for i in input().split()]

        #   UPDATE
        __mine__mcts__ = __mine__mcts__.update( _[0] , _[1] , _[2] , _[3] )
        __mine__mcts__.predict_update()

        print(__mine__mcts__._state,file=sys.stderr)

        #   POSSIBILITY
        for i in range(int(input())):
            _ = [int(j) for j in input().split()]

        #   CHECK LEN
        #   ONE OR MORE TIC-TAC-TOE

        #   FIRST GENERATION
        for i in range(NB_RAND_AFTER):

            #   MINIMAL MCTS >>> GENERATE ALL POSSIBILITY
            __children__ = __mine__mcts__.best_child( 1.4 )

            __children__ = __children__.expand_turns()

            _ = __children__.randomseq()

            __children__.backpropagate( _ )

        #   CHECK RESULT
        _ = []
        for c in __mine__mcts__._children :
            if c.n != 0 :
                _.append( c )

        #   NEW TURN >>> BEST CHILD
        _ = np.argmax( [ c.w / c.n for c in _ ] )

        _ = __mine__mcts__._children[ _ ]

        print(f'PREDICT >>> {list(map(str,_._state._predict))}',file=sys.stderr)

        _ = _._state._predict[0]

        print(_)
