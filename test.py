import numpy as np

from ConnectFour import ConnectFour

game = ConnectFour()
a = game.actions(game.board)

board = np.array([
	[0, 1, 0, 0, 0, 0, 0],
	[0, 2, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0],
	[0, 2, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0],
	[0, 1, 2, 0, 2, 1, 0],
])
game = ConnectFour(board=board)
print(game.board)
print(game.actions(board))
game.move(board, (5, 0))
print(game.board)
