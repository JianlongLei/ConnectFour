import math

from ConnectFour import ConnectFour


class TreeNode:
    def __init__(self, state, weight, n):
        self.state = state
        self.weight = weight
        self.n = n
        self.parent = 0
        self.children = []
        self.visited = False


class MCTS:
    def __init__(self, game: ConnectFour = ConnectFour()):
        self.game = game
        self.root = TreeNode(game.board, 0, 0)

    def calUcb(self, node: TreeNode):
        if not node.visited:
            return math.inf
        else:
            value_estimate = node.weight/node.n
            exploration = math.sqrt(2 * math.log(self.root.n) / node.n)
            ucb_score = value_estimate + exploration
            return ucb_score

    def selection(self, node: TreeNode):
        return 0

    def expansion(self, node: TreeNode):
        return 0

    def simulation(self, node: TreeNode):
        return 0

    def backpropagation(self, node: TreeNode):
        return 0

    def doSearch(self, node: TreeNode):
        if not node.children:
            if node.visited:
                self.simulation(node)
                self.backpropagation(node)
            else:
                self.expansion(node)
        self.selection(node)