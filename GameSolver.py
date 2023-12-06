import copy
import math
import random

import numpy as np

from ConnectFour import *


class TreeNode:
    def __init__(self, game: ConnectFour):
        self.game = copy.deepcopy(game)
        self.score = 0
        self.n = 0
        self.parent = None
        self.children = []
        self.action = []

    def isLeaf(self):
        return not self.children

    def update(self, status):
        player = self.game.currentPlayer
        if player == status:
            self.score += 1
        elif status > 0:
            self.score -= 1
        self.n += 1

    def visited(self):
        return self.n != 0


class MCTS:
    const = 2
    timeLimit = 0.08

    def __init__(self, game: ConnectFour = ConnectFour()):
        self.root = TreeNode(game)
        self.player = game.currentPlayer
        self.expansion(self.root)

    def calUcb(self, node: TreeNode):
        if not node.visited():
            return math.inf
        else:
            value_estimate = -node.score / node.n
            exploration = math.sqrt(self.const * math.log(self.root.n) / node.n)
            ucb_score = value_estimate + exploration
            return ucb_score

    def selection(self, node: TreeNode):
        while node and node.children:
            selected = None
            maxUcb = -math.inf
            for child in node.children:
                ucb = self.calUcb(child)
                if ucb > maxUcb:
                    maxUcb = ucb
                    selected = child
            node = selected
        return node

    def expansion(self, node: TreeNode):
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

    def simulation(self, node: TreeNode):
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

    def backpropagation(self, node: TreeNode, status):
        current = node
        while current.parent:
            current.parent.update(status)
            current = current.parent
        return 0

    def doSearch(self, iterations=None):
        if iterations is None:
            empty = np.count_nonzero(self.root.game.board == 0)
            iterations = int(2 ** empty / 10)
            iterations = min(iterations, 2500)
            iterations = max(iterations, 100)
        for i in range(iterations):
            node = self.selection(self.root)
            if node.visited() and self.expansion(node):
                node = node.children[0]
            status = self.simulation(node)
            self.backpropagation(node, status)
        root = self.root
        visitResult = []
        valueResult = []
        actionResult = []
        for i in range(len(root.children)):
            child = root.children[i]
            actionResult.append(root.action[i])
            visitResult.append(child.n)
            valueResult.append(-child.score)
        return visitResult, valueResult, actionResult
