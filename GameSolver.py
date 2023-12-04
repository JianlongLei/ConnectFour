import math

from ConnectFour import ConnectFour


class TreeNode:
	def __init__(self, state, parent=None):
		self.state = state
		self.wins = 0  # win time
		self.score = 0  # win +1 lose -1 draw 0
		self.visits = 0  # simulation time
		self.parent = parent
		self.children = []

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
	def __init__(self, player, game: ConnectFour = ConnectFour()):
		self.player = player
		self.game = game
		self.root = TreeNode(game.board)

	@staticmethod
	def select(node: TreeNode):
		while not node.children:
			node = node.best_child()

		return node

	@staticmethod
	def expanse(node: TreeNode):
		actions = ConnectFour.actions(node.state)
		for action in actions:
			state = node.state.copy()  # numpy deepcopy
			new_state = ConnectFour.move(state, action)
			child = TreeNode(state=new_state, parent=node)
			node.children.append(child)
		return node.children[0]  # randomly return a child

	@staticmethod
	def simulate(node: TreeNode):
		sim_board = node.state.copy()
		sim_game = ConnectFour(sim_board)
		while not sim_game.end:
			actions = ConnectFour.actions(sim_game.board)
			sim_game.doAction(actions[0])
		# if sim_game.endStatus == ConnectFour.PLAYER1:

		return sim_game.endStatus

	def back_track(self, node: TreeNode, result):
		while node != self.root:
			node.visits += 1
			node.wins += 1 if result == self.player else 0
			node.score += result
			node = node.parent

	def search(self):
		# if len(node.children) == len(ConnectFour.actions(node.state)):
		# 	return node.best_child()
		node = self.select(self.root)
		node = self.expanse(node)
		res = self.simulate(node)
		self.back_track(node, res)
