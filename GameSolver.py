import math

from ConnectFour import ConnectFour


class TreeNode:
	def __init__(self, state, parent=None):
		self.state = state
		self.wins = 0  # win time
		self.visits = 0  # simulation time
		self.parent = parent
		self.children = []

	# self.visited = False

	def best_child(self):
		if not self.children:
			return self

		best_child = max(self.children, key=calUcb)
		return best_child


def calUcb(node: TreeNode):
	if node.visits == 0:
		return math.inf

	exploitation = node.wins / node.visits
	exploration = math.sqrt(2 * math.log(node.parent.visits) / node.visits)
	ucb_score = exploitation + exploration
	return ucb_score


class MCTS:
	def __init__(self, game: ConnectFour = ConnectFour()):
		self.game = game
		self.root = TreeNode(game.board)

	def select(self, node: TreeNode):
		while not node.children:
			node = node.best_child()

		return node

	def expanse(self, node: TreeNode):
		temp_state = node.state.copy()  # numpy deepcopy
		temp_state

		return

	def simulate(self, node: TreeNode):
		return 0

	def back_track(self, node: TreeNode):
		return 0

	def search(self, node: TreeNode):
		# for _ in range(iterations):
		# 	# while not self.root.state.
		# 	pass
		legal_moves = 2
		if len(node.children) == legal_moves:
			return node.best_child()
		# elif len(node.children) > 0:  # leaf node
		node = self.select(node)
		self.expanse(node)
		self.simulate(node)
		self.back_track(node)
