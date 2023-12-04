import numpy as np

PLAYER1 = 1
PLAYER2 = -1
EMPTY = 0


class ConnectFour:
	PLAYER1 = PLAYER1
	PLAYER2 = PLAYER2
	end = False
	# 0: not end
	# 1 player 1 win
	# -1 player 2 win
	# 2 draw
	endStatus = 0
	currentPlayer = PLAYER1

	def __init__(self, width=7, height=6, board=None):
		if board is None:
			board = np.zeros((height, width))

		self.width = width
		self.height = height
		self.board = board

		self.nextStep = np.sum(board != 0, axis=0)
		self.currentPlayer = ConnectFour.cur_player(self.board)

	def newGame(self):
		self.board = np.zeros((self.height, self.width))
		self.nextStep = np.zeros(self.width)
		self.end = False
		self.endStatus = 0
		self.currentPlayer = PLAYER1

	def nextPlayer(self):
		self.currentPlayer = -self.currentPlayer

	# if player == PLAYER1:
	# 	self.currentPlayer =
	# else:
	# 	self.currentPlayer = 1

	def doAction(self, position):
		player = self.currentPlayer
		if np.abs(player) != 1:
			return False
		if position >= self.width:
			return False
		if self.nextStep[position] >= self.height:
			return False
		x = position
		y = int(self.height - self.nextStep[position] - 1)
		self.board[y][x] = player
		self.nextStep[position] += 1
		self.endStatus = self.checkEnd(x, y)
		self.end = self.endStatus != 0
		self.nextPlayer()
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
		return 2

	@staticmethod
	def cur_player(chessboard):
		x = np.sum(chessboard)
		return PLAYER1 if x % 2 == 0 else PLAYER2

	@staticmethod
	def actions(chessboard):
		actions = []
		cols = len(chessboard)
		rows = len(chessboard[0])

		for y in range(rows):
			for x in range(cols - 1, -1, -1):
				pos = (x, y)
				if chessboard[pos] == EMPTY:
					actions.append(pos)
					break
		return actions

	@staticmethod
	def move(chessboard, pos):
		if chessboard[pos] == EMPTY:
			chessboard[pos] = ConnectFour.cur_player(chessboard)
		return chessboard

	@staticmethod
	def is_terminal(chessboard):
		m, n = len(chessboard), len(chessboard[0])

		def check_line(start_row, start_col, delta_row, delta_col):
			player = chessboard[start_row][start_col]
			if player == 0:
				return False

			for step in range(1, 4):
				row = start_row + step * delta_row
				col = start_col + step * delta_col

				if row < 0 or row >= m or col < 0 or col >= n or chessboard[row][col] != player:
					return False

			return True

		for row in range(m):
			for col in range(n):
				for delta_row, delta_col in [(0, 1), (1, 0), (1, 1), (1, -1)]:
					if check_line(row, col, delta_row, delta_col):
						return True, chessboard[row][col]

		empty_pos = np.where(chessboard==EMPTY)
		empty_pos = list(zip(empty_pos[0], empty_pos[1]))
		# print(empty_pos)
		# print(len(empty_pos))
		if len(empty_pos) == 0:
			return True, 0

		return False, 0
