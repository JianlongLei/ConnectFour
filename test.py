import numpy as np

from ConnectFour import ConnectFour
from GameSolver import MCTS

game = ConnectFour()
a = game.actions(game.board)

board = np.array([
	[0, 1, 0, 0, 0, 0, 0],
	[0, -1, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0],
	[0, -1, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0],
	[0, 1, -1, 0, -1, 1, 0],
])
game = ConnectFour(board=board)
print(game.board)
print(game.actions(board))
game.move(board, (5, 0))
print(game.board)


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

for _ in range(30):
	mcts.search()

print("root", mcts.root)

for c in mcts.root.children:
	print(c)