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
			return self

		best_child = max(self.children, key=calUcb)
		return best_child

	def __str__(self):
		return f"wins/visits:{self.wins}/{self.visits}, children:{self.children}, parent:{id(self.parent)}"


def calUcb(node: TreeNode):
	if node.visits == 0:
		return math.inf

	exploitation = node.score / node.visits
	exploration = math.sqrt(2 * math.log(node.root.visits) / node.visits)
	ucb_score = exploitation + exploration
	return ucb_score


class MCTS:
	def __init__(self, player, game: ConnectFour = ConnectFour()):
		self.player = player
		self.game = game
		self.root = TreeNode(game.board)
		self.root.root = self.root

	@staticmethod
	def select(node: TreeNode):
		while node.children:
			node = node.best_child()

		return node

	@staticmethod
	def expanse(node: TreeNode):
		actions = ConnectFour.actions(node.state)
		if not actions:
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
		sim_game = ConnectFour(board=sim_board)
		while not sim_game.end:
			print(sim_game.board)
			print(sim_game.endStatus)
			actions = ConnectFour.actions(sim_game.board)
			if not actions:
				break
			action = random.choice(actions)
			sim_game.doAction(action[1])
			print(action)
			print(sim_game.end)
		# print(sim_game.board)

		return sim_game.endStatus

	def back_track(self, node: TreeNode, result):
		while node is not None:
			node.visits += 1
			# node.wins += 1 if result == self.player else 0
			if result == self.player:
				node.wins += 1
				node.score += 1
			elif result == -self.player:
				node.score -= 1

			# node.score += result
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
		print(res)
		self.back_track(node, res)
		print(self.root)
