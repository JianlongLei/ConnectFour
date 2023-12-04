import numpy as np

import GameSolver
from ConnectFour import ConnectFour
from GameSolver import MCTS

game = ConnectFour()
a = game.actions(game.board)
#
# board = np.array([
# 	[0, 1, 0, 0, 0, 0, 0],
# 	[0, -1, 0, 0, 0, 0, 0],
# 	[0, 1, 0, 0, 0, 0, 0],
# 	[0, -1, -1, 0, 0, 0, 0],
# 	[0, 1, 1, 1, 1, 0, 0],
# 	[-1, 1, -1, -1, -1, 1, -1],
# ])
# game = ConnectFour(board=board)
# print(game.board)
# print(game.actions(board))
# game.move(board, (5, 1))
# print(game.board)
# print(ConnectFour.is_terminal(board))

board2 = np.array([[-1, 1, -1, -1, 1, -1, -1],
                   [1, 1, 1, -1, -1, 1, 1],
                   [1, -1, -1, -1, 1, -1, -1],
                   [-1, 1, 1, 1, -1, 1, 1],
                   [-1, 1, -1, -1, 1, -1, 1],
                   [-1, 1, 1, 1, -1, -1, 1]])
print("res:",ConnectFour.is_terminal(board2))

board = np.array([
	[0, 1, -1, -1, 1, -1, 0],
	[0, 1, 1, -1, -1, 1, 0],
	[0, -1, -1, -1, 1, -1, 0],
	[0, 1, 1, 1, -1, 1, 0],
	[0, 1, -1, -1, 1, -1, 0],
	[-1, 1, 1, 1, -1, -1, 1],
])
game = ConnectFour(board=board)

mcts = MCTS(ConnectFour.PLAYER1, game)
print(ConnectFour.is_terminal(board))

for _ in range(1600):
	mcts.search()

print("root", mcts.root)

for c in mcts.root.children:
	print(c, GameSolver.calUcb(c))
