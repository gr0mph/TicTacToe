import 'dart:io';
import 'dart:math';

int nbRoll = 0;
var error = stderr.writeln, parse = int.parse;
String read() {
  String? s = stdin.readLineSync();
  return s == null ? '' : s;
}
final int kNONE = 0 , kMINE = 1 , kOPP = 2 , kNEVER = 3;
final int kCG = 0 , kDEBUG = 1;
final int kTIME_START = 800 , kTIME_TURN = 80;
final int kLIMIT_START = 999 , kLIMIT_TURN = 99;
final Board k_ = new Board();
final int console = kDEBUG;
final List<String> kWIN = [ "NONE" , "MINE" , "OPPONENT" , "GAME OVER"];

final List<List<List<int>>> kLINE = [
    [ [ 0 , 1 , 2 ] , [ 0 , 4 , 8 ] , [ 0 , 3 , 6 ] ],
    [ [ 0 , 1 , 2 ] , [ 1 , 4 , 7 ] ],
    [ [ 0 , 1 , 2 ] , [ 6 , 4 , 2 ] , [ 2 , 5 , 8 ] ],
    [ [ 0 , 3 , 6 ] , [ 3 , 4 , 5 ] ] ,
    [ [ 0 , 4 , 8 ] , [ 6 , 4 , 2 ] , [ 3 , 4 , 5 ] , [ 1 , 4 , 7 ] ] ,
    [ [ 3 , 4 , 5 ] , [ 2 , 5 , 8 ] ] ,
    [ [ 0 , 3 , 6 ] , [ 6 , 4 , 2 ] , [ 6 , 7 , 8 ] ] ,
    [ [ 6 , 7 , 8 ] , [ 1 , 4 , 7 ] ] ,
    [ [ 6 , 7 , 8 ] , [ 0 , 4 , 8 ] , [ 2 , 5 , 8 ] ] ,
];


Stopwatch stopwatch = new Stopwatch();
int rtTime = kTIME_START;
int rtLimit = kLIMIT_START;

void display(List<int> c , List<int> t , List<int> r)
{
	error("${c[0]}${c[1]}${c[2]} ${c[9]}${c[10]}${c[11]} ${c[18]}${c[19]}${c[20]} ${t[0]}${t[1]}${t[2]}");
	error("${c[3]}${c[4]}${c[5]} ${c[12]}${c[13]}${c[14]} ${c[21]}${c[22]}${c[23]} ${t[3]}${t[4]}${t[5]}");
	error("${c[6]}${c[7]}${c[8]} ${c[15]}${c[16]}${c[17]} ${c[24]}${c[25]}${c[26]} ${t[6]}${t[7]}${t[8]}");
	error("");
	error("${c[27]}${c[28]}${c[29]} ${c[36]}${c[37]}${c[38]} ${c[45]}${c[46]}${c[47]} ${r[0]}${r[1]}${r[2]}");
	error("${c[30]}${c[31]}${c[32]} ${c[39]}${c[40]}${c[41]} ${c[48]}${c[49]}${c[50]} ${r[3]}${r[4]}${r[5]}");
	error("${c[33]}${c[34]}${c[35]} ${c[42]}${c[43]}${c[44]} ${c[51]}${c[52]}${c[53]} ${r[6]}${r[7]}${r[8]}");
	error("");
	error("${c[54]}${c[55]}${c[56]} ${c[63]}${c[64]}${c[65]} ${c[72]}${c[73]}${c[74]}");
	error("${c[57]}${c[58]}${c[59]} ${c[66]}${c[67]}${c[68]} ${c[75]}${c[76]}${c[77]}");
	error("${c[60]}${c[61]}${c[62]} ${c[69]}${c[70]}${c[71]} ${c[78]}${c[79]}${c[80]}");
}

class UTTT
{
    List<int> _cell = List.generate( 81 , (i) => kNONE , growable : false );
    List<int> _ttt = List.generate( 9 , (i) => kNONE , growable : false );
    List<int> _rest = List.generate( 9 , (i) => 9 , growable : false );
    int over = kNONE;

    List<int> get cell => _cell;
    List<int> get ttt => _ttt;
    List<int> get rest => _rest;

    void set cell( List<int> c ) => this._cell = List.generate( c.length ,
    (i) => this._cell[i] = c[i] , growable : false );

    void set ttt( List<int> t ) => this._ttt = List.generate( t.length ,
    (i) => this._ttt[i] = t[i] , growable : false );

    void set rest( List<int> r ) => this._rest = List.generate( r.length ,
    (i) => this._rest[i] = r[i] , growable : false );

    @override
    bool operator == (o) {
        if( o is UTTT )
        {
            for( int i = 0 ; i < 81 ; i++ )
                if( this.cell[i] != o.cell[i] ) return false;
            for( int i = 0 ; i < 9 ; i++ )
                if( this.ttt[i] != o.ttt[i] )   return false;
            return true;
        }
        return false;
    }

    @override
    String toString() {
        display( this.cell , this.ttt , this.rest );
        return "${this.over} : ${kWIN[this.over]}";
    }

    int readConsole() {
		if( console == kCG )
		{
        	List inputs = read().split(' ');
        	int oRow = int.parse(inputs[0]);
        	int oCol = int.parse(inputs[1]);
        	int validActionCount = int.parse(read());
        	for (int i = 0; i < validActionCount; i++)  var _ = read();
        	if( oRow == -1 ) {
            	return -1;
        	}
        	return k_.cellFromYX[oRow][oCol];
		}
		else
			return parse(read());
    }

    int isLine( int base , List<List<int>> list , int isMine )
    {
        for( final i in list )
        {
            if( this.cell[base + i[0] ] == this.cell[base + i[1] ] &&
				this.cell[base + i[0] ] == this.cell[base + i[2] ] )
            {
                this.ttt[ base ~/ 9 ] = isMine;
                this.rest[ base ~/ 9 ] = 0;
                for( int i = 0 ; i < 9 ; i++ )
                {
                    this.cell[base + i] = kNEVER;
                }
                return isMine;
            }
        }
        return kNONE;
    }

    int isOver( int base , List<List<int>> list , int isMine )
    {
        if( this.ttt[base] == isMine )
        {
            for( final i in list )
            {
                if( this.ttt[ i[0] ] == this.ttt[ i[1] ] &&
                    this.ttt[ i[0] ] == this.ttt[ i[2] ] )
                {
                    this.over = isMine;
                    return this.over;
                }
            }
        }

        for( int i = 0 ; i < 9 ; i++ )
        {
            if( this.rest[i] > 0 ) {
                return kNONE;
            }
        }
        this.over = kNEVER;
        return this.over;
    }

    void play( int c , int isMine )
    {
        int upper = (c ~/ 9);
        int base = (c ~/ 9) * 9;
        int index = ( c % 9);

        this.cell[c] = isMine;
        this.rest[upper]--;

        if( this.rest[upper] == 0 ) this.ttt[upper] = kNEVER;

        isLine( base , kLINE[index] , isMine );

        isOver( upper , kLINE[upper] , isMine );

    }

    List<int> validAction(int c , int isMine )
    {
        List<int> r = [];
        int modulo = c % 9;
        if( this.ttt[modulo] != kNONE )
        {
            for( int i = 0 ; i < 81 ; i++ )
            {
                if( this.cell[i] == kNONE )
                    r.add(i);
            }
        }
        else
        {
            for( int i = 0 ; i < 9 ; i++ ) {
                if( this.cell[modulo * 9 + i] == kNONE )
                    r.add(modulo * 9 + i);
            }
        }
        return r;
    }
}

class MCTS
{
    final int W = 0 , N = 1 ;

    //  Link with parent
    int i1 = 0 , i2 = 0;

    //  Tree
    MCTS? p;
    List<List<MCTS>> child = [];

    //  Result
    List<int> w1 = [] ;
    List<int> n1 = [] ;

    //  Action played
    int playedMine = -1;
    int playedOpp = -1;
    List<int> nextMine = [];

    //  Link with UTTT (Board)
    late UTTT info;

    int get n {
        int n = 1;
        for( final _ in n1 )    n = n + _;
        return n;
    }

    int get w {
        int w = 0;
        for( final _ in w1 )    w = w + _;
        return w;
    }

    @override
    String toString() {
        display( this.info.cell , this.info.ttt , this.info.rest );
        for( final rowChild in this.child )
        {
            stderr.write("${rowChild[0].i1}: w ${this.w1[rowChild[0].i1]} n ${this.n1[rowChild[0].i1]} l ${rowChild.length} ");
            for( final c in rowChild)
                stderr.write("[ ${c.playedMine} ${c.playedOpp} ]");
            error("");
        }
        error("");

        if( playedMine >= 0 && playedOpp >= 0 )
            return "OVER : ${kWIN[this.info.over]} $i1 $i2 $playedMine [y:${k_.y[playedMine]},x:${k_.x[playedMine]}] $playedOpp [y:${k_.y[playedOpp]},x:${k_.x[playedOpp]},] \n$w1 \n$n1";
        else
            return "OVER : ${kWIN[this.info.over]} $i1 $i2 $playedMine $playedOpp \n$w1 \n$n1";
    }

    MCTS selection( double c )
    {
        MCTS _ = this;

        int i2 = 0;
        while( _.n1.length > 0 )
        {
            //  Check Time
            if( stopwatch.elapsedMilliseconds >= rtTime )
            {
                error("SELECTION TIME LIMIT EXCEED ON CALL ${stopwatch.elapsedMilliseconds}");
                return _;
            }

            //  End of Game
            if( _.info.over != kNONE )  return _;

            List<double> weight = List.generate( _.n1.length ,
            (i1) => _.w1[i1] / _.n1[i1] + c * sqrt ( 2 * _.n / _.n1[i1] ) );

            double wMax = -0.1;
            int iMax = -1;
            for( int i = 0 ; i < weight.length ; i++ )
            {
                if( wMax < weight[i] ) {
                    iMax = i;
                    wMax = weight[i];
                }
            }

            i2 = Random().nextInt( _.child[iMax].length );
            _ = _.child[iMax][i2];
        }
        return _;
    }

    MCTS expansion()
    {
        MCTS _ = this;
        //List<int> nextMine = [];

        error("EXPANSION ${stopwatch.elapsedMilliseconds}");

        //  Check Time
        if( stopwatch.elapsedMilliseconds > rtTime ) {
            error("EXPAND TIME LIMIT EXCEED ON CALL ${stopwatch.elapsedMilliseconds}");
            return _;
        }

        //  End of Game
        if( _.info.over != kNONE ) return _;

        if( _.playedOpp == -1 )  _.nextMine = [ 40 ];
        else
            _.nextMine = _.info.validAction( _.playedOpp , kMINE );

        _.w1 = List.generate( _.nextMine.length , (i) => 0 , growable : false );
        _.n1 = List.generate( _.nextMine.length , (i) => 1 , growable : false );
        _.child = List.generate( _.nextMine.length , (i) => [] , growable : false );

        int i1 = 0 , i2 = 0;
        for( final int playedMine in _.nextMine )
        {
            UTTT next = new UTTT()..over = _.info.over..ttt = _.info.ttt..cell = _.info.cell..rest = _.info.rest;
            next.play( playedMine , kMINE );

            i2 = 0;

            //  End game discover after kMINE play.
            if( next.over != kNONE )
            {
                MCTS l = new MCTS()..info = next
                ..i1 = i1..i2 = i2..playedMine = playedMine..playedOpp = -1..p = _ ;

                _.child[i1].add(l);

                //_.child[i1].add( new MCTS()..info = next
                //..i1 = i1..i2 = i2..playedMine = playedMine..playedOpp = -1..p = _ );
            }
            else
            {
                List<int> nextOpp = next.validAction( playedMine , kOPP );

                for( final int playedOpp in nextOpp )
                {
                    if( stopwatch.elapsedMilliseconds > rtTime ){
                        error("EXPAND TIME LIMIT EXCEED NEW STEP ${stopwatch.elapsedMilliseconds}");
                        return _;
                    }

                    UTTT existing = new UTTT()..cell = next.cell..ttt = next.ttt..over = next.over..rest = next.rest;
                    _.child[i1].add( new MCTS()..info = existing
                    ..i1 = i1..i2 = i2..playedMine = playedMine..playedOpp = playedOpp..p = _ );

                    existing.play( playedOpp , kOPP );

                    i2++;
                }
            }
            i1++;
        }

        i1 = 0;
        i2 = _.child[i1].length ;
        return _.child[i1][ Random().nextInt(i2) ];
    }

    int simulation()
    {
        nbRoll++;
        UTTT roll = new UTTT()..cell = this.info.cell..ttt = this.info.ttt..over =this.info.over..rest = this.info.rest;
        int playedMine = this.playedMine, playedOpp = this.playedOpp;
        while( roll.over == kNONE )
        {
            if( stopwatch.elapsedMilliseconds > rtTime )
            {
                error("SIMULATION TIME LIMIT EXCEED ON CALL");
                break;
            }

            List<int> nextMine = roll.validAction( playedOpp , kMINE );

            if( nextMine.length == 0 )
            {
                //  BUG
                error("BUG playedOpp : $playedOpp");
                error(roll);
            }

            playedMine = nextMine[ Random().nextInt( nextMine.length ) ];
            roll.play( playedMine , kMINE );

            if( roll.over != kNONE )   break;

            if( stopwatch.elapsedMilliseconds > rtTime ){
                break;
            }

            List<int> nextOpp = roll.validAction( playedMine , kOPP );

            if( nextOpp.length == 0 )
            {
                //  BUG
                error("BUG playedMine : $playedMine");
                error(roll);
            }

            playedOpp = nextOpp[ Random().nextInt( nextOpp.length ) ];
            roll.play( playedOpp , kOPP );

        }
        return roll.over;
    }

    void backpropagation( int result )
    {
        int i1 = this.i1;
        MCTS? _ = this.p;

        if( stopwatch.elapsedMilliseconds > rtTime )
        {
            error("BACK PROPAGATION TIME LIMIT EXCEED ON CALL");
            return;
        }

        if( result == kMINE )
            while( _ != null ) {
                _.w1[ i1 ]++;
                _.n1[ i1 ]++;
                i1 = _.i1;
                _ = _.p;
            }
        else
            while( _ != null ) {
                _.n1[ i1 ]++;
                i1 = _.i1;
                _ = _.p;
            }
    }
}

class Board {

    final List<int> x = List.generate( 81 , (i) => 0 , growable : false );
    final List<int> y = List.generate( 81 , (i) => 0 , growable : false );
    final List<List<int>> cellFromYX = List.generate( 9 ,
    (i) => List.generate( 9 , (i) => 0 ) , growable : false );

    void memoization()
    {
        for( int cell = 0 , xCol = 0 , yRow = 0 ; cell < 81 ;  )
        {
            //  Cell
            cellFromYX[yRow][xCol] = cell;
            x[cell] = xCol;
            y[cell] = yRow;

            cell++;
            xCol++;

            if( cell % 27 == 0 ) {
                yRow++;
                xCol = 0;
            }
            else
            if( cell % 9 == 0 )  yRow = yRow - 2;
            else
            if( cell % 3 == 0 ) {
                yRow++;
                xCol = xCol - 3;
            }
        }
    }

}

void main() {

    UTTT uttt = new UTTT();
    MCTS mcts = new MCTS()..info = uttt;
    int iMine = -1;

	stopwatch.start();

    int rtTime = kTIME_START;
    k_.memoization();

    // Game Loop
    while (true)
    {
        int playedOpp = uttt.readConsole();
		stopwatch.reset();

        error("READ CONSOLE ${stopwatch.elapsedMilliseconds}");

        if( iMine != -1 )
            for( final MCTS _ in mcts.child[iMine] )
                if( _.playedOpp == playedOpp )
                {
                    mcts = _;
                    uttt = _.info;
                    mcts.p = null;
                    break;
                }
        else
        if( _ != -1 )
        {
            uttt.play( playedOpp , kOPP );
            mcts.playedOpp = playedOpp;
        }

        if( console == kDEBUG )
        {
            if( mcts.info.over != kNONE )
            {
                error("==== GAME OVER ====");
                error(mcts.info);
                error("==== GAME OVER ====");
                return;
            }
        }

        error(mcts);

        //  Missing link between action and here...
        int i = 0;
        while( stopwatch.elapsedMilliseconds < rtTime )
        {
            //  Best child
            MCTS _ = mcts.selection( 1.41 );

            if( stopwatch.elapsedMilliseconds > rtTime ){
                error("LOOP SELECTION TIME LIMIT EXCEED AFTER ${stopwatch.elapsedMilliseconds}");
                break;
            }

            _ = _.expansion();

            if( stopwatch.elapsedMilliseconds > rtTime ){
                error("LOOP EXPANSION TIME LIMIT EXCEED AFTER ${stopwatch.elapsedMilliseconds}");
                break;
            }

            int k = _.simulation();

            if( stopwatch.elapsedMilliseconds > rtTime ){
                error("SIOMULATION SELECTION TIME LIMIT EXCEED AFTER ${stopwatch.elapsedMilliseconds}");
                break;
            }

            _.backpropagation( k );

            i++;
        }

        double ratioMax = -1, current = -1;
        for( int i = 0 ; i < mcts.w1.length ; i++ )
        {
            current = mcts.w1[i] / mcts.n1[i] ;
            if( current > ratioMax )
            {
                ratioMax = current;
                iMine = i;
            }
        }

        if( console == kDEBUG )
        {
            if( mcts.info.over != kNONE )
            {
                error("==== GAME OVER ====");
                error(mcts.info);
                error("==== GAME OVER ====");
                return;
            }
        }

        int playedMine = mcts.child[iMine][0].playedMine;
        int yRow = k_.y[ playedMine ];
        int xCol = k_.x[ playedMine ];

        error("PLAY >>>>>>");
        print("$yRow $xCol TIME : ${stopwatch.elapsedMilliseconds}");

        if( console == kDEBUG )
        {
            mcts.info.play( playedMine , kMINE);
            print("--- --- --- ---");
            print(mcts.info);
            print("--- --- --- ---");
            print(mcts.info.validAction(playedMine,kMINE));
        }

        if( stopwatch.elapsedMilliseconds >= rtLimit )
        {
            print("TIME LIMIT EXCEED");
            return;
        }

        stopwatch.reset();
        rtTime = kTIME_TURN;
        rtLimit = kLIMIT_TURN;
        if( console == kDEBUG )
            rtTime = kTIME_TURN;

    }
}
