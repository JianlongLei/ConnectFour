import numpy as np

import GameSolver
from ConnectFour import ConnectFour
from GameSolver import MCTS

game = ConnectFour()
a = game.actions(game.board)

board2 = np.array([[-1, 1, -1, -1, 1, -1, -1],
                   [1, 1, 1, -1, -1, 1, 1],
                   [1, -1, -1, -1, 1, -1, -1],
                   [-1, 1, 1, 1, -1, 1, 1],
                   [-1, 1, -1, -1, 1, -1, 1],
                   [-1, 1, 1, 1, -1, -1, 1]])
print("res:", ConnectFour.is_terminal(board2))

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

for _ in range(1000):
	mcts.search()

print("root", mcts.root)

# for c in mcts.root.children:
# 	print(c, GameSolver.cal_ucb(c))
# 	print(c.state)
	# print(ConnectFour.cur_player(c.state))
	# next_node = c.worst_child()
	# print(next_node)
	# print(next_node.state)


node = mcts.root
while node is not None:
	print(node)
	print(node.state)
	if ConnectFour.cur_player(node.state) == mcts.player:
		node = node.best_child()
		# print(GameSolver.cal_ucb())
	else:
		node = node.best_child(True)
	# print(node, GameSolver.cal_cb(node))

	# node = node.best_child()

# mcts = MCTS(ConnectFour.PLAYER1, game)
# for _ in range(1000):
# 	mcts.search()
# for c in mcts.root.children:
# 	print(c, GameSolver.calUcb(c))
# 	print(c.state)