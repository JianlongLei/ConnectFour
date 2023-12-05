import copy
import math
import random
import time

from ConnectFour import ConnectFour


class TreeNode:
    def __init__(self, game: ConnectFour):
        self.game = copy.deepcopy(game)
        self.weight = 0
        self.n = 0
        self.parent = None
        self.children = []
        self.action = []

    def isLeaf(self):
        return not self.children

    def update(self, node):
        self.weight += node.weight
        self.n += 1

    def visited(self):
        return self.n != 0


class MCTS:
    const = 2
    timeLimit = 10000

    def __init__(self, game: ConnectFour = ConnectFour()):
        self.root = TreeNode(game)
        self.player = game.currentPlayer
        self.expansion(self.root)

    def calUcb(self, node: TreeNode):
        if not node.visited():
            return math.inf
        else:
            value_estimate = node.weight / node.n
            exploration = math.sqrt(self.const * math.log(self.root.n) / node.n)
            ucb_score = value_estimate + exploration
            return ucb_score

    def selection(self, node: TreeNode):
        while node.children:
            selected = -1
            maxUcb = -math.inf
            for child in node.children:
                ucb = self.calUcb(node)
                if ucb > maxUcb and not child.game.end:
                    maxUcb = maxUcb
                    selected = child
            node = selected
        return node

    def expansion(self, node: TreeNode):
        if not node.isLeaf():
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
        if game.endStatus == self.player:
            # win, get score 1
            node.weight = 1
        elif game.endStatus == -1:
            # draw, get score 0
            node.weight = 0
        else:
            # lose, get score -1
            node.weight = -1
        node.n = 1
        return 0

    def backpropagation(self, node: TreeNode):
        current = node
        while current.parent:
            current.parent.update(current)
            current = current.parent
        return 0

    def doSearch(self):
        startTime = time.time()
        node = self.root
        self.expansion(node)
        while time.time() - startTime < self.timeLimit:
            node = self.selection(node)
            if node.game.end:
                break
            if node.visited() and self.expansion(node):
                node = node.children[0]
            if node.visited():
                break
            self.simulation(node)
            self.backpropagation(node)
        root = self.root
        visitResult = []
        valueResult = []
        actionResult = []
        for i in range(len(root.children)):
            child = root.children[i]
            actionResult.append(root.action[i])
            visitResult.append(child.n / root.n)
            valueResult.append(child.weight / root.weight)
        return visitResult, valueResult, actionResult
