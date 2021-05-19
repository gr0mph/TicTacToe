import 'dart:io';
import 'dart:math';

var error = stderr.writeln, parse = int.parse;
String read() {
  String? s = stdin.readLineSync();
  return s == null ? '' : s;
}
final int kNONE = 0 , kMINE = 1 , kOPP = 2 , kNEVER = 3;
final int kTIME_START = 900 , kTIME_TURN = 90;
final Board k_ = new Board();
int crc24q( List<int> crc24q , int input , int crc )
	=> ( (crc << 8) &0xffffff ) ^ crc24q[ (crc >> 16) ^ input ];

final Map<int,List<UTTT>> g_map = new Map();

void memoization_crc24q( List<int> CRC24Q )
{
	int divisor = 0x1864cfb , crc24q = 0;
	for( int i = 0 ; i < 256 ; i++ )
	{
		crc24q = i << 16;
		for( int j = 0 ; j < 8 ; j++ )
		{
			crc24q = crc24q << 1;
            if( crc24q & 0x1000000 == 0x1000000 )
				crc24q = crc24q ^ divisor;
		}
		CRC24Q[i] = crc24q & 0xffffff;
	}
}

class UTTT
{
    List<int> _memento = List.generate( 9 , (i) => kNONE , growable : false );
    List<int> _cell = List.generate( 81 , (i) => kNONE , growable : false );
    List<int> _ttt = List.generate( 9 , (i) => kNONE , growable : false );
    int over = kNONE;

    List<int> get cell => _cell;
    List<int> get ttt => _ttt;

    void set cell( List<int> c ) => this._cell = List.generate( c.length ,
    (i) => this._cell[i] = c[i] , growable : false );

    void set ttt( List<int> t ) => this._ttt = List.generate( t.length ,
    (i) => this._ttt[i] = t[i] , growable : false );

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

    int readConsole() {
        List inputs = read().split(' ');
        int oRow = int.parse(inputs[0]);
        int oCol = int.parse(inputs[1]);
        int validActionCount = int.parse(read());
        for (int i = 0; i < validActionCount; i++) {
            inputs = read().split(' ');
            int row = int.parse(inputs[0]);
            int col = int.parse(inputs[1]);
        }
        if( oRow == -1 )    return -1;
        return k_.cellFromYX[oRow][oCol];
    }

    int isLine( int base , List<List<int>> list , int isMine )
    {
        for( final i in list )
        {
            if( this.cell[base] == this.cell[base + i[1] ] && this.cell[base + 0] == this.cell[base + i[2] ] )
            {
                this.ttt[ base ~/ 9 ] = isMine;
                for( int i = 0 ; i < 9 ; i++ )
                {
                    this._memento[i] = this.cell[base + i];
                    this.cell[base + i] = kNONE;
                }
                return isMine;
            }
        }
        return kNONE;
    }

    int isEnd( int base , List<int> list , int isMine )
    {
        for( int i = 0 ; i < 9 ; i++ )
        {
            if( list[i] == kNONE )  return kNONE;
        }
        return isMine;
    }

    void play( int c , int isMine )
    {
        this.cell[c] = isMine;
        int base = (c ~/ 9) * 9;
        int index = ( c % 9);
        if( index == 0 )
            isLine( base , [ [ 0 , 1 , 2 ] , [ 0 , 4 , 8 ] , [ 0 , 3 , 6 ] ] , isMine );
        if( index == 1 )
            isLine( base , [ [ 0 , 1 , 2 ] , [ 1 , 4 , 7 ] ] , isMine );
        if( index == 2 )
            isLine( base , [ [ 0 , 1 , 2 ] , [ 6 , 4 , 2 ] , [ 2 , 5 , 8 ] ] , isMine );
        if( index == 3 )
            isLine( base , [ [ 0 , 3 , 6 ] , [ 3 , 4 , 5 ] ] , isMine );
        if( index == 4 )
            isLine( base , [ [ 0 , 4 , 8 ] , [ 6 , 4 , 2 ] , [ 3 , 4 , 5 ] , [ 1 , 4 , 7 ] ] , isMine );
        if( index == 5 )
            isLine( base , [ [ 3 , 4 , 5 ] , [ 2 , 5 , 8 ] ] , isMine );
        if( index == 6 )
            isLine( base , [ [ 0 , 3 , 6 ] , [ 6 , 4 , 2 ] , [ 6 , 7 , 8 ] ] , isMine );
        if( index == 7 )
            isLine( base , [ [ 6 , 7 , 8 ] , [ 1 , 4 , 7 ] ] , isMine );
        if( index == 8 )
            isLine( base , [ [ 6 , 7 , 8 ] , [ 0 , 4 , 8 ] , [ 2 , 5 , 8 ] ] , isMine );

        if( isEnd( base , List.generate( 9 , (i) => this.cell[base + i] , growable : false ) , kNEVER ) == kNEVER )
        {
            this.ttt[ base ~/ 9 ] = kNEVER;
            for( int i = 0 ; i < 9 ; i++ )
            {
                this._memento[i] = this.cell[base + i];
                this.cell[base + i] = kNONE;
            }
        }


    }

    int hashing()
    {
        int crc = 0;
        for( int i = 0 , shift = 0; i < 81 ; i++ , (shift + 2) & 0x6 )
        {
            crc = crc24q( k_.kCRC24Q , (this.cell[i] << shift) , crc);
        }
        for( int i = 0 , shift = 0; i < 9 ; i++ , (shift + 2) & 0x6 )
        {
            crc = crc24q( k_.kCRC24Q , (this.ttt[i] << shift) , crc);
        }
        return crc;
    }

    void backward(int c , int isMine )
    {
        if( this.cell[c] == kNONE )
        {
            int base = (c ~/ 9) * 9;
            int upper = c ~/ 9;
            this.ttt[upper] = kNONE;
            for( int i = 0; i < 9 ; i++ )
                this.cell[ base + i ] = this._memento[ i ];
            this.cell[ c ] = kNONE;
        }
        else
            this.cell[c] = kNONE;
    }

    List<int> validAction(int c , int isMine )
    {
        List<int> r = [];
        int base = (c ~/ 9) * 9;
        int upper = c ~/ 9;
        if( this.ttt[upper] == kNONE )
            for( int i = 0 ; i < 81 ; i++ )
                if( this.cell[i] == kNONE )         r.add(i);
        else
            for( int i = 0 ; i < 9 ; i++ )
                if( this.cell[base + i] == kNONE )  r.add(base + i);
        return r;
    }

    int end()
    {
        if( this.ttt[0] == this.ttt[1] && this.ttt[0] == this.ttt[2] )  return this.ttt[0];
        if( this.ttt[3] == this.ttt[4] && this.ttt[3] == this.ttt[5] )  return this.ttt[3];
        if( this.ttt[6] == this.ttt[7] && this.ttt[6] == this.ttt[8] )  return this.ttt[6];
        if( this.ttt[0] == this.ttt[3] && this.ttt[0] == this.ttt[6] )  return this.ttt[0];
        if( this.ttt[1] == this.ttt[4] && this.ttt[1] == this.ttt[7] )  return this.ttt[1];
        if( this.ttt[2] == this.ttt[5] && this.ttt[2] == this.ttt[8] )  return this.ttt[2];
        if( this.ttt[0] == this.ttt[4] && this.ttt[0] == this.ttt[8] )  return this.ttt[0];
        if( this.ttt[2] == this.ttt[4] && this.ttt[2] == this.ttt[6] )  return this.ttt[2];
        if( isEnd( 0 , this.ttt , kNEVER ) == kNEVER )                  return kNEVER;
        return kNONE;
    }
}

class MCTS
{
    final int W = 0 , N = 1 ;

    //  Link with UTTT (Board)
    int crc = 0;

    //  Link with parent
    int i1 = 0 , i2 = 0;

    //  Tree
    MCTS? p;
    List<List<MCTS>> child = [];

    //  Result
    List<int> w1 = [] ;
    List<int> n1 = [] ;

    //  Action played
    int playedMine = 0;
    int playedOpp = 0;

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

    MCTS selection( double c )
    {
        MCTS _ = this;
        int i2 = 0;
        while( _.n1.length > 0 )
        {
            for( int i1 = 0 ; i1 < _.n1.length ; i1++ )
                if( _.n1[i1] == 0 )
                {
                    i2 = Random().nextInt( child[i1].length );
                    return this.child[i1][i2];
                }

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

            i2 = Random().nextInt( child[iMax].length );
            _ = this.child[iMax][i2];
        }
        return _;
    }

    MCTS expansion()
    {
        MCTS _ = this;
        List<int> nextMine = [];

        if( this.playedOpp == -1 )  nextMine = [ 40 ];
        else
            nextMine = this.info.validAction( this.playedOpp , kMINE );

        _.w1 = List.generate( nextMine.length , (i) => 0 , growable : false );
        _.n1 = List.generate( nextMine.length , (i) => 0 , growable : false );
        _.child = List.generate( nextMine.length , (i) => [] , growable : false );

        int i1 = 0;
        for( final int playedMine in nextMine )
        {
            UTTT next = new UTTT()..over = this.info.over..ttt = this.info.ttt..cell = this.info.cell;
            next.play( playedMine , kMINE );

            List<int> nextOpp = next.validAction( playedMine , kOPP );

            int i2 = 0, crc = 0;
            bool find = false;
            for( final int playedOpp in nextOpp )
            {
                next.play( playedOpp , kOPP );
                crc = next.hashing();
                if( g_map.containsKey( crc ) )
                    for( final UTTT existing in g_map[crc] ?? [] )
                        if( existing == next )
                        {
                            _.child[i1].add( new MCTS()..info = existing..crc = crc
                            ..i1 = i1..i2 = i2..playedMine = playedMine..playedOpp = playedOpp..p = _ );
                            find = true;
                            break;
                        }

                if( find == false )
                {
                    UTTT existing = new UTTT()..cell = next.cell..ttt = next.ttt..over = next.over;

                    _.child[i1].add( new MCTS()..info = existing..crc = crc
                    ..i1 = i1..i2 = i2..playedMine = playedMine..playedOpp = playedOpp..p = _ );

                    if( g_map.containsKey( crc ) )  g_map[crc]?.add( existing );
                    else                            g_map[crc] = [ existing ];
                }
                next.backward( playedOpp , kOPP);
            }
        }
        return _.child[0][0];
    }

    int simulation()
    {
        UTTT roll = new UTTT()..cell = this.info.cell..ttt = this.info.ttt..over =this.info.over;
        int playedMine = this.playedMine, playedOpp = this.playedOpp;
        while( roll.end() != kNONE )
        {
            List<int> nextMine = roll.validAction( playedOpp , kMINE );
            playedMine = nextMine[ Random().nextInt( nextMine.length ) ];
            roll.play( playedMine , kMINE );

            if( roll.end() != kNONE )   break;

            List<int> nextOpp = roll.validAction( playedMine , kOPP );
            playedOpp = nextOpp[ Random().nextInt( nextOpp.length ) ];
            roll.play( playedOpp , kOPP );
        }
        return roll.end();
    }

    void backpropagation( int result )
    {
        MCTS child = this;
        MCTS? _ = this.p;

        while( _ != null )
        {
            if( result == kMINE )   _.w1[ child.i1 ]++;
            _.n1[ child.i1 ]++;
            child = _;
            _ = _.p;
        }
    }
}

class Board {

    final List<int> kCRC24Q = List.generate( 256 , (i) => 0 , growable : false );
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

    Stopwatch stopwatch = new Stopwatch();
    stopwatch.start();

    int rtTime = kTIME_START;
    k_.memoization();
    memoization_crc24q(k_.kCRC24Q);

    error("cellFromYX");
    for( int row = 0 ; row < 9 ; row++ )
        error(k_.cellFromYX[row]);

    error("x");
    error(k_.x);

    error("y");
    error(k_.y);

    // game loop
    while (true) {

        // Write an action using print()
        // To debug: stderr.writeln('Debug messages...');
        int playedOpp = uttt.readConsole();

        if( iMine != -1 )
            for( final MCTS _ in mcts.child[iMine] )
                if( _.playedOpp == playedOpp )
                {
                    mcts = _;
                    uttt = _.info;
                    break;
                }
        else
        if( _ != -1 )
        {
            uttt.play( playedOpp , kOPP );
            g_map[uttt.hashing()] = [ uttt ];
            mcts.playedOpp = playedOpp;
        }

        //  Missing link between action and here...
        while( stopwatch.elapsedMilliseconds < rtTime )
        {
            //  Best child
            MCTS _ = mcts.selection( 1.41 );

            _ = _.expansion();

            int k = _.simulation();

            _.backpropagation( k );
        }

        error("stopwatch ${stopwatch.elapsedMilliseconds} $rtTime");
        //print('0 0');

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

        error("stopwatch ${stopwatch.elapsedMilliseconds} $rtTime");
        int yRow = k_.y[ mcts.child[iMine][0].playedMine ];
        int xCol = k_.x[ mcts.child[iMine][0].playedMine ];

        print("$yRow $xCol");

        stopwatch.reset();
        rtTime = kTIME_TURN;

    }
}
