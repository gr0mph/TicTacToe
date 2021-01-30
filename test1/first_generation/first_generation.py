import sys
import math
import random, copy
import numpy as np
sys.path.append('../../')

# Global variables

# Class
from TicTacToe3 import Neuron
from TicTacToe3 import TicTacToe
from TicTacToe3 import MonteCarloTreeSearch

# Global
from TicTacToe3 import DRAW, NEITHER, MINE, OPP
from TicTacToe3 import TYPE_TURN
from TicTacToe3 import NB_RAND_FIRST
from TicTacToe3 import NB_RAND_AFTER
from TicTacToe3 import TYPE_STR1, TYPE_STR2, TYPE_STR3
from TicTacToe3 import SIMPLEST_STR
from TicTacToe3 import TUPLE_WIN

# Function
from TicTacToe3 import f_row, f_col, f_prop
from TicTacToe3 import f_win, f_all
from TicTacToe3 import victory_check2, victory_check3
from TicTacToe3 import coord_upAndLeft, coord_pToIndex, coord_indexToP
from TicTacToe3 import mcts_generate

import unittest

class _first_generation(unittest.TestCase):

    def test_first_turn(self):
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

        #   FIRST TURN GE NERATION
        _ = {}
        for i2 in range(9):
            _[ 4 , i2 ] = __mine__action__[ (4,i2) ]

        # MONTE-CARLO TREE SEARCH INITIALIZATION
        __mine__mcts__ = MonteCarloTreeSearch(None)
        __mine__mcts__._state = __mine__

        __mine__mcts__.generate( _ )

        print(__mine__)


    def test_no(self):
        print("===========================================================")
        print("== HamiltonSolver class has been replaced by PathSolving ==")
        print("===========================================================")

if __name__ == '__main__':
    unittest.main()
