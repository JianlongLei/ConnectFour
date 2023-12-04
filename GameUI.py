from tkinter import *

from ConnectFour import ConnectFour


class GameUI:
    p1 = 'Green'
    p2 = 'Blue'
    backgroundColor = "#DFE2E6"
    p1Color = "#56B89C"
    p2Color = "#2F3E4E"
    emptyColor = "#F7F8F9"
    padding = 10
    title = "Connect Four"
    # item
    itemSize = 50
    boardWidth = 0
    boardHeight = 0

    def __init__(self, window, game: ConnectFour = ConnectFour()):
        self.game = game
        self.window = window
        self.boardWidth = (self.itemSize + self.padding * 2) * self.game.width
        self.boardHeight = (self.itemSize + self.padding * 2) * self.game.height
        self.width = self.boardWidth + self.padding * 2
        self.height = self.boardHeight + self.padding * 2
        window.title(self.title)
        button = Button(window, text="New Game!", command=self._click_new_game)
        button.grid(row=0)
        solver = Button(window, text="Solver!", command=self._click_solve_game)
        solver.grid(row=1)
        self.canvas = Canvas(window, width=self.width, height=self.height,
                             background=self.backgroundColor,
                             highlightthickness=0)
        self.canvas.grid(row=2)
        self.currentPlayerVar = StringVar(self.window, value="")
        self.currentPlayerLabel = Label(self.window, textvariable=self.currentPlayerVar)
        self.currentPlayerLabel.grid(row=3)
        self.canvas.bind('<Button-1>', self._board_click)
        self.newGame()

    def _show_current_player(self):
        p = self.p1 if self.game.currentPlayer == 1 else self.p2
        self.currentPlayerVar.set('Current Player: ' + p)

    def draw(self):
        for i in range(self.game.height):
            for j in range(self.game.width):
                itemX0 = j * (self.itemSize + self.padding * 2) + self.padding * 2
                itemY0 = i * (self.itemSize + self.padding * 2) + self.padding * 2
                itemX1 = itemX0 + self.itemSize
                itemY1 = itemY0 + self.itemSize
                color = self.emptyColor
                item = self.game.board[i][j]
                if item == ConnectFour.PLAYER1:
                    color = self.p1Color
                elif item == ConnectFour.PLAYER2:
                    color = self.p2Color
                self.canvas.create_oval(itemX0, itemY0, itemX1, itemY1, fill=color)
        self._show_current_player()

    def _board_click(self, event):
        if self.game.end:
            return
        if event.x < self.padding:
            position = 0
        elif event.x > self.width - self.padding:
            position = self.game.width - 1
        else:
            position = (event.x - self.padding) // (self.itemSize + self.padding * 2)
        if self.game.doAction(position):
            self.draw()
        if self.game.end:
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            if self.game.endStatus != -1:
                t = (self.p1 if self.game.endStatus == 1 else self.p2) + " WON!"
            else:
                t = "DRAW!"
            self.canvas.create_text(x, y, text=t, font=("Helvetica", 32), fill="#333")

    def _click_new_game(self):
        self.newGame()

    def _click_solve_game(self):
        return 0

    def newGame(self):
        self.game.newGame()
        self.canvas.delete(ALL)
        self.canvas.config(width=self.width, height=self.height)
        self.window.update()
        self.draw()
