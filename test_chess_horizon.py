# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from AlphaBetaAINoHash import AlphaBetaAINoHash
from ChessGame import ChessGame
from MinimaxAI import MinimaxAI

import sys


player1 = HumanPlayer()
player2 = AlphaBetaAI(4)

game = ChessGame(player1, player2)
game.board.set_fen('r1b1kb1r/pppp1pp1/4p3/2n5/2Q1BN1q/3P4/PP2PP2/RNB1K2R b KQkq - 0 1')
while not game.is_game_over():
    print(game)
    game.make_move()


#print(hash(str(game.board)))
