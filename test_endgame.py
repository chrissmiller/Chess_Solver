# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
from MinimaxAI import MinimaxAI

import sys


player1 = HumanPlayer()
player2 = MinimaxAI(3)

game = ChessGame(player1, player2)

# Sets to black one move from victory
#game.board.set_fen('1K6/8/qk6/8/8/8/8/8 b - - 0 1')
game.board.set_fen('6nk/6pp/3N2pr/8/8/8/7P/7K b - - 0 1')
while not game.is_game_over():
    print(game)
    game.make_move()


#print(hash(str(game.board)))
