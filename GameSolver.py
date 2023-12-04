import copy
import math
import random

from ConnectFour import ConnectFour


class TreeNode:
    def __init__(self, game: ConnectFour):
        self.game = copy.deepcopy(game)
        self.weight = 0
        self.n = 0
        self.parent = None
        self.children = []

    def isLeaf(self):
        return not self.children

    def update(self, node):
        self.weight += node.weight
        self.n += 1

    def visited(self):
        return self.n != 0


class MCTS:
    const = 2

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
        selected = -1
        maxUcb = -math.inf
        for i in node.children:
            ucb = self.calUcb(node)
            if ucb > maxUcb:
                maxUcb = maxUcb
                selected = i
        return selected

    def expansion(self, node: TreeNode):
        availableActions = node.game.availableActions()
        for i in availableActions:
            newNode = TreeNode(node.game)
            newNode.game.doAction(i)
            node.children.append(newNode)
            newNode.parent = node
        return 0

    def simulation(self, node: TreeNode):
        game = copy.deepcopy(node.game)
        terminate = game.end
        while not terminate:
            # get all available actions
            availableActions = game.availableActions()
            if availableActions:
                # random actions
                action = random.randint(0, len(availableActions) - 1)
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
            current.parent.update()
            current = current.parent
        return 0

    def doSearch(self, node: TreeNode):
        current = node
        while current:
            if current.isLeaf():
                if not node.visited():
                    self.simulation(node)
                    self.backpropagation(node)
                else:
                    self.expansion(node)
                current = self.root
            else:
                nextNode = self.selection(node)
                if nextNode >= 0:
                    current = node.children[nextNode]
                else:
                    current = self.root
