import numpy as np

P1_WIN = 1
P2_WIN = 2
DRAW = -1
NOT_END = 0


class ConnectFour:
	p1 = 1
	p2 = 2
	empty = 0
	end = False
	# 0: not end
	# 1 player 1 win
	# 2 player 2 win
	# -1 draw
	endStatus = NOT_END
	currentPlayer = 1

	def __init__(self, width=7, height=6):
		self.width = width
		self.height = height
		self.board = np.zeros((height, width))
		self.nextStep = np.zeros(width)

	def newGame(self):
		self.board = np.zeros((self.height, self.width))
		self.nextStep = np.zeros(self.width)
		self.end = False
		self.endStatus = 0
		self.currentPlayer = 1

	def availableActions(self):
		actions = []
		for i in range(len(self.nextStep)):
			if self.nextStep[i] < self.height:
				actions.append(i)
		return actions

	def nextPlayer(self, playerId):
		if playerId == 1:
			self.currentPlayer = 2
		else:
			self.currentPlayer = 1

	def doAction(self, position):
		playerId = self.currentPlayer
		if playerId < 1 or playerId > 2:
			return False
		if position >= self.width:
			return False
		if self.nextStep[position] >= self.height:
			return False
		x = position
		y = int(self.height - self.nextStep[position] - 1)
		self.board[y][x] = playerId
		self.nextStep[position] += 1
		self.endStatus = self.checkEnd(x, y)
		self.end = self.endStatus != NOT_END
		self.nextPlayer(playerId)
		return True

	def checkEnd(self, x, y):
		result = self.checkHorizontally(x, y)
		if result != 0:
			return result
		result = self.checkVertically(x, y)
		if result != 0:
			return result
		result = self.checkDiagonallyDownRight(x, y)
		if result != 0:
			return result
		result = self.checkDiagonallyDownLeft(x, y)
		if result != 0:
			return result
		return self.checkDraw()

	def checkHorizontally(self, x, y):
		# horizontally
		for i in range(4):
			start = x - i
			end = start + 4
			if start < 0 or end > self.width:
				continue
			item = self.board[y][x]
			allSame = True
			for j in range(4):
				if item != self.board[y][start + j]:
					allSame = False
					break
			if allSame:
				return item
		return 0

	def checkVertically(self, x, y):
		# vertically
		for i in range(4):
			start = y - i
			end = start + 4
			if start < 0 or end > self.height:
				continue
			item = self.board[y][x]
			allSame = True
			for j in range(4):
				if item != self.board[start + j][x]:
					allSame = False
					break
			if allSame:
				return item
		return 0

	def checkDiagonallyDownRight(self, x, y):
		# diagonally down-right
		for i in range(4):
			startX = x - i
			startY = y - i
			endX = startX + 4
			endY = startY + 4
			if startX < 0 or startY < 0 or endX > self.width or endY > self.height:
				continue
			item = self.board[y][x]
			allSame = True
			for j in range(4):
				if self.board[startY + j][startX + j] != item:
					allSame = False
					break
			if allSame:
				return self.board[y][x]
		return 0

	def checkDiagonallyDownLeft(self, x, y):
		# diagonally down-left
		for i in range(4):
			startX = x - i
			startY = y + i
			endX = startX + 4
			endY = startY - 4
			if startX < 0 or endY < 0 or endX > self.width or startY >= self.height:
				continue
			item = self.board[y][x]
			allSame = True
			for j in range(4):
				if self.board[startY - j][startX + j] != item:
					allSame = False
					break
			if allSame:
				return self.board[y][x]
		return 0

	def checkDraw(self):
		# Has rooms, not draw game
		for i in range(self.width):
			if self.nextStep[i] < self.height:
				return 0

		# No room left, draw game
		return -1
