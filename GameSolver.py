import math
import random

from ConnectFour import ConnectFour


class TreeNode:
	def __init__(self, state, parent=None, root=None):
		self.state = state
		self.wins = 0  # win time
		self.score = 0  # win +1 lose -1 draw 0
		self.visits = 0  # simulation time
		self.parent = parent
		self.root = root
		self.children = []

	def best_child(self):
		if not self.children:
			return None

		best_child = max(self.children, key=calUcb)
		return best_child

	def __str__(self):
		return f"score/wins/visits:{self.score}/{self.wins}/{self.visits}, children:{self.children}, parent:{id(self.parent)}"


def calUcb(node: TreeNode):
	if node.visits == 0:
		return math.inf
	if node.parent is None:
		return 0
	exploitation = node.score / node.visits
	exploration = math.sqrt(2 * math.log(node.parent.visits) / node.visits)
	ucb_score = exploitation + exploration
	return ucb_score


class MCTS:
	def __init__(self, player, game: ConnectFour = ConnectFour()):
		self.player = player
		self.game = game
		self.root = TreeNode(game.board)
		self.root.root = self.root

	# @staticmethod
	def select(self, node: TreeNode):
		while node.children:
			cur_player = ConnectFour.cur_player(node.state)
			if cur_player == self.player:
				node = node.best_child()
			else:
				node = random.choice(node.children)

		return node

	@staticmethod
	def expanse(node: TreeNode):
		terminated, _ = ConnectFour.is_terminal(node.state)
		actions = ConnectFour.actions(node.state)
		if not actions or terminated:
			return node
		for action in actions:
			state = node.state.copy()  # numpy deepcopy
			new_state = ConnectFour.move(state, action)
			child = TreeNode(state=new_state, parent=node, root=node.root)
			node.children.append(child)
		# print("child:", child)
		# print("root:", node)
		return node.children[0]  # randomly return a child

	@staticmethod
	def simulate(node: TreeNode):
		sim_board = node.state.copy()
		winner = None
		while True:
			terminated, winner = ConnectFour.is_terminal(chessboard=sim_board)
			if terminated:
				break
			actions = ConnectFour.actions(sim_board)
			if not actions:
				print(sim_board)
			action = random.choice(actions)
			ConnectFour.move(sim_board, action)

		return winner

	def back_track(self, node: TreeNode, result):
		while node is not None:
			node.visits += 1
			if result == self.player:
				node.wins += 1
				node.score += 1
			elif result == -self.player:
				node.score -= 1

			node = node.parent

	def search(self):
		# if len(node.children) == len(ConnectFour.actions(node.state)):
		# 	return node.best_child()
		node = self.select(self.root)
		print("select:", node)
		node = self.expanse(node)
		print("expanse:", node)
		# print(node.state)
		res = self.simulate(node)
		print("res:", res)
		self.back_track(node, res)
