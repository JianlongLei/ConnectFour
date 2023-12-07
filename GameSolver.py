import copy
import math
import random

import matplotlib.pyplot as plt

from ConnectFour import *


class TreeNode:
	def __init__(self, game: ConnectFour):
		self.game = copy.deepcopy(game)
		self.score = 0
		self.n = 0
		self.win = 0
		self.lose = 0
		self.draw = 0
		self.parent = None
		self.children = []
		self.action = []

	def isLeaf(self):
		return not self.children

	def update(self, status):
		player = self.game.currentPlayer
		if player == status:
			self.score += 1
			self.win += 1
		elif status > 0:
			self.score -= 1
			self.lose += 1
		else:
			self.draw += 1
		self.n += 1

	def visited(self):
		return self.n != 0


def calUcb(node: TreeNode, const=2):
	if not node.visited():
		return math.inf
	else:
		value_estimate = -node.score / node.n
		exploration = math.sqrt(const * math.log(node.parent.n) / node.n)
		ucb_score = value_estimate + exploration
		return ucb_score


class MCTS:
	# const = 2
	# timeLimit = 0.08

	def __init__(self, game: ConnectFour = ConnectFour()):
		self.root = TreeNode(game)
		self.player = game.currentPlayer
		self.expansion(self.root)

	@staticmethod
	def selection(node: TreeNode):
		while node and node.children:
			selected = None
			maxUcb = -math.inf
			for child in node.children:
				ucb = calUcb(child)
				if ucb > maxUcb:
					maxUcb = ucb
					selected = child
			node = selected
		return node

	@staticmethod
	def expansion(node: TreeNode):
		if not node.isLeaf():
			return False
		if node.game.end:
			return False
		availableActions = node.game.availableActions()
		for i in availableActions:
			newNode = TreeNode(node.game)
			newNode.game.doAction(i)
			node.children.append(newNode)
			node.action.append(i)
			newNode.parent = node
		return True

	@staticmethod
	def simulation(node: TreeNode):
		game = copy.deepcopy(node.game)
		terminate = game.end
		while not terminate:
			# get all available actions
			availableActions = game.availableActions()
			if availableActions:
				# random actions
				action = random.choice(availableActions)
				game.doAction(action)
				terminate = game.end
			else:
				# no available actions
				terminate = True
		node.update(game.endStatus)
		return game.endStatus

	@staticmethod
	def backpropagation(node: TreeNode, status):
		current = node
		while current.parent:
			current.parent.update(status)
			current = current.parent
		return 0

	def doSearch(self, iterations=5000, span=0.000001):
		avg_score = []
		for i in range(iterations):
			node = self.selection(self.root)
			if node.visited() and self.expansion(node):
				node = node.children[0]
			status = self.simulation(node)
			self.backpropagation(node, status)
			avg_score.append(self.root.score / self.root.n)
			if i > 100 and np.abs(np.average(avg_score[-10:]) - np.average(avg_score[-100:])) <= span:
				break  # converge condition

		root = self.root
		visitResult = []
		valueResult = []
		actionResult = []
		winResult = []
		for i in range(len(root.children)):
			child = root.children[i]
			actionResult.append(root.action[i])
			visitResult.append(child.n)
			valueResult.append(-child.score)
			winResult.append(child.lose / child.n)
		plt.plot(avg_score)
		plt.show()
		return visitResult, valueResult, actionResult, winResult
