import sys
import math
import random, copy
import numpy as np

DRAW, NEITHER, MINE, OPP = -2 , -1 , 0 , 1
TYPE_TURN = { 0 : 'MINE' , 1 : 'OPP' }

NB_RAND_FIRST = 40
NB_RAND_AFTER = 25

NB_TTT_ONE = 1
NB_TTT_MORE = 2
NB_TTT_FEW = 3
NB_TTT_TURN1 = 0

f_row = lambda obj : obj.param[0]
f_col = lambda obj : obj.param[1]
f_prop = lambda obj : obj.param[2]

f_win = lambda obj : obj[0]
f_all = lambda obj : obj[1]

TYPE_STR1 = { NEITHER : '     ' ,  MINE : '     ' , OPP : '     ' }
TYPE_STR2 = { NEITHER : '     ' ,  MINE : '  X  ' , OPP : '  O  ' }
TYPE_STR3 = { NEITHER : '     ' ,  MINE : '     ' , OPP : '     ' }

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

def victory_check2( obj , ind1 ):
    for ind2 in TUPLE_WIN:
        if obj[ (ind1, ind2[0]) ] == obj[ (ind1, ind2[1]) ] == obj[ (ind1, ind2[2]) ] :
            return obj[ (ind1, ind2[0]) ]
    return NEITHER

def victory_check3( obj ):
    for ind1 in TUPLE_WIN:
        if obj[ ind1[0] ] == obj[ ind1[1] ] == obj[ ind1[2] ] :
            return obj[ ind1[0] ]
    return NEITHER

def coord_upAndLeft( inrow , incol ):
    row = ( inrow // 3 ) * 3
    col = ( incol // 3 ) * 3
    return ( row , col )

def coord_pToIndex( inrow , incol ):
    ind1 = (inrow // 3) * 3 + (incol // 3)
    ind2 = (inrow % 3) * 3 + (incol % 3)
    return ( ind1 , ind2 )

def coord_indexToP( inind1 , inind2 ):
    row = (inind1 // 3) * 3 + (ind2 // 3)
    col = (ind1 % 3) * 3 + (ind2 % 3)
    return ( row , col )

class TicTacToe():

    def __init__(self,clone):
        if clone is None :
            self._secret , self._state, self._predict = {}, {}, []
            self._mine , self._first = {} , {}

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
            self._first = copy.copy( clone._first )


    def __str__(self):
        out = '  0 1 2 3 4 5 6 7 8 0 1 2 3 4 5 6 7 8'

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
                if self._secret[ind1] == NEITHER :
                    for ind2 in range(0,3):
                        _ = self._state[ (ind1, ind2) ]
                        out1 = f'{out1} {SIMPLEST_STR[_]}'
                    for ind2 in range(3,6):
                        _ = self._state[ (ind1, ind2) ]
                        out2 = f'{out2} {SIMPLEST_STR[_]}'
                    for ind2 in range(6,9):
                        _ = self._state[ (ind1, ind2) ]
                        out3 = f'{out3} {SIMPLEST_STR[_]}'
                else :
                    out1 = f'{out1} {TYPE_STR1[NEITHER]}'
                    out2 = f'{out2} {TYPE_STR2[NEITHER]}'
                    out3 = f'{out3} {TYPE_STR3[NEITHER]}'

            out = f'{out}\n{out1}\n{out2}\n{out3}'

        return out

    def update( self , row , col , owner ):
        ind1 = (row // 3) * 3 + (col // 3)
        ind2 = (row % 3) * 3 + (col % 3)

        #   DELETE THIS POSSIBILITY
        del self._mine[ ( ind1 , ind2 ) ]
        try:
            del self._first[ ( ind1 , ind2 ) ]
        except:
            pass

        #   HAS BEEN ALREADY GAINED
        if self._secret[ ind1 ] != NEITHER :
            return NEITHER

        #   MARK
        self._state[ ( ind1 , ind2 ) ] = owner

        _ = victory_check2 ( self._state , ind1 )

        if _ != NEITHER :

            #   MARK
            self._secret[ ind1 ] = _

            _ = victory_check3 ( self._secret )

            #print(f'UPDATE <<< {self}',file=sys.stderr)

            return _

        return NEITHER

    def is_game_over( self , ind1 ):

        if self._secret[ind1] == NEITHER and len(self.possibility(MINE)) == 0 :
            return OPP

        return self._secret[ind1]

    def possibility( self , own ):
        return list( self._first.values() )

    def __eq__( self , o ):
        return True if self._state == o._state else False

class MonteCarloTreeSearch():

    def __init__(self,clone):
        if clone is not None:
            self._parent = clone
            self._children = []
            clone._children.append(self)
            self._result = [ 0 , 1 ]

            self._state = TicTacToe(clone._state)
            #print(f'MonteCarloTreeSearch init from previous',file=sys.stderr)
        else:
            self._parent = None
            self._children = []
            self._result = [ 0 , 1 ]

            self._state = None

    @property
    def n(self):
        return f_all(self._result)

    @property
    def w(self):
        return f_win(self._result)

    def first_generation(self, first):

        if len(self._children) == 0 :

            childs = []
            self._state._first = first

            for o1 in self._state.possibility( MINE ) :

                ochild1 = MonteCarloTreeSearch(self)

                ochild1._state._predict.append( o1 )

                ochild1._state.update( o1.row , o1.col , MINE )

                if ochild1._state.is_game_over( o1.ind1 ) == MINE :
                    self._children = [ ochild1 ]
                    return

                childs_opp = []

                for m1 in ochild1._state.possibility( OPP ) :

                    child = MonteCarloTreeSearch(ochild1)

                    child._state.update( m1.row , m1.col , OPP )

                    if child._state.is_game_over( o1.ind1 ) == OPP :
                        childs_opp = []
                        break

                    childs_opp.append( child )

                childs.extend( childs_opp )

            self._children = childs

        else :

            childs = []
            self._state._first = first

            for m1 in self._children :

                n1 = m1._state._predict[0]

                if n1 in first :

                    m1._state._first = copy.copy( first )

                    del first[ ( n1.ind1 , n1.ind2 ) ]

                    childs.append( m1 )

            for o1 in self._state.possibility( MINE ) :

                ochild1 = MonteCarloTreeSearch(self)

                ochild1._state._predict.append( o1 )

                ochild1._state.update( o1.row , o1.col , MINE )

                if ochild1._state.is_game_over( o1.ind1 ) == MINE :
                    self._children = [ ochild1 ]
                    return

                childs_opp = []

                for m1 in ochild1._state.possibility( OPP ) :

                    child = MonteCarloTreeSearch(ochild1)

                    child._state.update( m1.row , m1.col , OPP )

                    if child._state.is_game_over( o1.ind1 ) == OPP :
                        childs_opp = []
                        break

                    childs_opp.append( child )

                childs.extend( childs_opp )

            self._children = childs

    def best_child(self, c_parameter ):
        #  Upper Confidence Bounds (UCB1) formula
        _ = self

        while len(_._children) > 0 :
            weight = [
                (c.w / c.n) + c_parameter * math.sqrt( (2 * math.log2(_.n) / c.n ) )
                for c in _._children
            ]
            #print(f'weight {list(map(str,weight))}',file=sys.stderr)
            _ = _._children[ np.argmax( weight ) ]

        return _

    def expand_turns(self):
        #   SELECT NEXT/RANDOM ACTION
        #   COMPUTE STATE
        childs = []
        #for o1 in random.sample( self._state.possibility( MINE ) , 9 ):
        for o1 in self._state.possibility( MINE ):

            #print(f'EXPAND_TURNS >>> {o1}',file=sys.stderr )

            ochild1 = MonteCarloTreeSearch(self)

            ochild1._state._predict.append( o1 )

            ochild1._state.update( o1.row , o1.col , MINE )

            if ochild1._state.is_game_over( o1.ind1 ) == MINE :
                self._children = [ ochild1 ]
                return ochild1

            childs_opp = []

            #for m1 in random.sample( ochild1._state.possibility( OPP ) , 9 ):
            for m1 in ochild1._state.possibility( OPP ):

                child = MonteCarloTreeSearch(ochild1)

                child._state.update( m1.row , m1.col , OPP )

                if child._state.is_game_over( o1.ind1 ) == OPP :
                    childs_opp = []
                    break

                childs_opp.append( child )

            else :

                childs_opp.append( ochild1 )

            childs.extend( childs_opp )

        else :

            return self

        self._children = childs

        child = random.choice(self._children)

        return child

    def randomseq( self , ind1 ):
        TURN = 5
        ROLLOUT_TURN = MINE
        rollout_state = TicTacToe(self._state)

        #print("START >>> randomseq",file=sys.stderr)
        #print(f'{rollout_state}',file=sys.stderr)

        while rollout_state.is_game_over( ind1 ) == NEITHER and TURN > 0 :

            TURN = TURN - 1

            _ = rollout_state.possibility( ROLLOUT_TURN )

            sel = random.choice(_)

            sel_row , sel_col = sel.row , sel.col

            rollout_state.update( sel_row , sel_col , ROLLOUT_TURN )

            ROLLOUT_TURN = MINE if ROLLOUT_TURN == OPP else OPP

        #print(f" END  >>> randomseq RESULT [ {rollout_state.is_game_over(ind1)} ]",file=sys.stderr)
        #print(f' SECRET >>> {list(map(str,rollout_state._secret.values() ))}',file=sys.stderr)
        #print(f'{rollout_state}',file=sys.stderr)

        if rollout_state.is_game_over( ind1 ) == MINE:
            return [ 2 * (TURN + 1) , 2 * (TURN + 1) ]
        elif rollout_state.is_game_over( ind1 ) == NEITHER :
            return [ 1 * (TURN + 1) , 2 * (TURN + 1) ]
        else :
            return [ 0 * (TURN + 1) , 2 * (TURN + 1) ]

    def backpropagate(self, result):
        self._result[0] = f_win(self._result) + f_win(result)
        self._result[1] = f_all(self._result) + f_all(result)
        _ = self._parent
        while _ is not None :
            _._result[0] = f_win(_._result) + f_win(result)
            _._result[1] = f_all(_._result) + f_all(result)
            _ = _._parent

    def update(self, mine_row , mine_col , opp_row , opp_col ):
        self._state.update( mine_row , mine_col , MINE )
        self._state.update( opp_row , opp_col , OPP )

        _ = None
        for _ in self._children :
            if _._state == self._state :
                _._state._predict.pop(0)
                return _

        self._state._predict = []
        self._parent = None
        self._children = []
        self._result = [ 0 , 1 ]
        return self

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
    state = NB_TTT_ONE
    __mine__.update( _[0] , _[1] , _[2] )
else :
    state = NB_TTT_TURN1

#   POSSIBILITY
check = [ 0 ] * 9
first_generation = {}
for i in range(int(input())):

    _ = [int(j) for j in input().split()]
    ind1 , ind2 = coord_pToIndex( _[0] , _[1] )
    check[ ind1 ] = check[ ind1 ] + 1
    first_generation[ (ind1,ind2) ] = __mine__action__[ (ind1,ind2)]
    print(f'ind1 {ind1} ind2 {ind2} action {__mine__action__[ (ind1,ind2)]}',file=sys.stderr)

#   FIRST TURN TIC-TAC-TOE
if state == NB_TTT_TURN1 :
    print(f'STATE >>> NB_TTT_TURN1',file=sys.stderr)
    _ = {}
    for k1 , k2 in first_generation.keys():
        if k1 == 4 :
            _[ k1 , k2 ] = first_generation[ k1 , k2 ]

    first_generation = _
    turn1 = 4

else :
    print(f'STATE >>> NB_TTT_ONE',file=sys.stderr)
    state = NB_TTT_ONE
    turn1 = np.argmax( check )

# MONTE-CARLO TREE SEARCH INITIALIZATION
__mine__mcts__ = MonteCarloTreeSearch(None)
__mine__mcts__._state = __mine__

print(f'first {list(map(str,first_generation.items()))}',file=sys.stderr)

__mine__mcts__.first_generation( first_generation )

for i in range(NB_RAND_FIRST):

    __children__ = __mine__mcts__.best_child( 1.4 )

    __children__ = __children__.expand_turns()

    _ = __children__.randomseq( turn1 )

    #print(f'RESULT >>> (simulation) randomseq {list(map(str,_))}',file=sys.stderr)

    __children__.backpropagate( _ )

#   FIRST TURN >>> CHOOSE BEST CHILD
print(f'c.w / c.n {list(map( str, [ c.w / c.n for c in __mine__mcts__._children ] ))}',file=sys.stderr)
#print(f'predict 0 {list(map( str, [ c._state._predict[0] for c in __mine__mcts__._children ] ))}', file=sys.stderr)

_ = np.argmax( [ c.w / c.n for c in __mine__mcts__._children ] )

_ = __mine__mcts__._children[ _ ]

print(f'_predict {list(map(str,_._state._predict))}',file=sys.stderr)

_ = _._state._predict[0]

print(_)

# AFTER FIRST TURN
while True:
    #   OPPONENT ACTION
    _ = [_.row] + [_.col] + [int(i) for i in input().split()]

    #   UPDATE
    __mine__mcts__ = __mine__mcts__.update( _[0] , _[1] , _[2] , _[3] )

    #   POSSIBILITY
    check = [ 0 ] * 9
    state = NB_TTT_TURN1

    first_generation = {}
    for i in range(int(input())):

        _ = [int(j) for j in input().split()]
        ind1 , ind2 = coord_pToIndex( _[0] , _[1] )
        check[ ind1 ] = check[ ind1 ] + 1
        first_generation[ (ind1,ind2) ] = __mine__action__[ (ind1,ind2)]

    #   CHECK LEN
    #   ONE OR MORE TIC-TAC-TOE
    print(f'CHECK >>> {list(map(str,check))}',file=sys.stderr)

    if sum( [ 1 for _ in check if _ > 0 ] ) == 1 :
        state = NB_TTT_ONE
        print(f'STATE >>> NB_TTT_ONE',file=sys.stderr)

    elif len(first_generation) <= 9 :
        state = NB_TTT_FEW
        print(f'STATE >>> NB_TTT_FEW',file=sys.stderr)

    else :
        state = NB_TTT_MORE
        print(f'STATE >>> NB_TTT_MORE',file=sys.stderr)
        _ = {}
        for i1, k1 in zip( range(9), list(first_generation.keys()) ):
            _[ k1 ] = first_generation[ k1 ]

        first_generation = _

    #   FIRST GENERATION
    __mine__mcts__.first_generation( first_generation )

    for i in range(NB_RAND_AFTER):

        #   MINIMAL MCTS >>> GENERATE ALL POSSIBILITY
        __children__ = __mine__mcts__.best_child( 1.4 )

        __children__ = __children__.expand_turns()

        #_ = __children__.qsimulate()
        _ = __children__.randomseq( np.argmax( check ) )

        __children__.backpropagate( _ )

    #   NEW TURN >>> BEST CHILD
    _ = np.argmax( [ c.w / c.n for c in __mine__mcts__._children ] )

    _ = __mine__mcts__._children[ _ ]

    print(f'_predict {list(map(str,_._state._predict))}',file=sys.stderr)

    _ = _._state._predict[0]

    print(_)
