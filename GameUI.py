import time
from tkinter import *
from tkinter import messagebox
from ConnectFour import *
from GameSolver import MCTS
import pickle

saveFile = 'saved_game.pkl'


class GameUI:
    p1 = 'Blue'
    p2 = 'Green'
    backgroundColor = "#DFE2E6"
    p1Color = "#2F3E4E"
    p2Color = "#56B89C"
    emptyColor = "#F7F8F9"
    padding = 10
    title = "Connect Four"
    # item
    itemSize = 50
    boardWidth = 0
    boardHeight = 0
    solving = False
    isAiMode = False

    def __init__(self, window, game: ConnectFour = ConnectFour()):
        self.game = game
        self.window = window
        self.boardWidth = (self.itemSize + self.padding * 2) * self.game.width
        self.boardHeight = (self.itemSize + self.padding * 2) * self.game.height
        self.width = self.boardWidth + self.padding * 2
        self.height = self.boardHeight + self.padding * 2
        window.title(self.title)
        topFrame = Frame(window)
        topFrame.pack(side=TOP, fill='both')
        newGame = Button(topFrame, text="New Game", command=self._click_new_game)
        newGame.pack(side=LEFT, padx=10, pady=10)
        solver = Button(topFrame, text="Solver", command=self._click_solve_game)
        solver.pack(side=LEFT, padx=10, pady=10)
        save = Button(topFrame, text="Save", command=self._click_save_game)
        save.pack(side=LEFT, padx=10, pady=10)
        load = Button(topFrame, text="Load", command=self._click_load_game)
        load.pack(side=LEFT, padx=10, pady=10)
        com = Button(topFrame, text="AIPlayer", command=self._click_ai_mode)
        com.pack(side=LEFT, padx=10, pady=10)
        self.canvas = Canvas(window, width=self.width, height=self.height,
                             background=self.backgroundColor,
                             highlightthickness=0)
        self.canvas.pack()
        self.currentPlayerVar = StringVar(self.window, value="")
        self.currentPlayerLabel = Label(self.window, textvariable=self.currentPlayerVar)
        self.currentPlayerLabel.pack(side=BOTTOM)
        self.canvas.bind('<Button-1>', self._board_click)
        self.newGame()

    def _show_current_player(self, game):
        p = self.p1 if game.currentPlayer == 1 else self.p2
        self.currentPlayerVar.set('Current Player: ' + p)

    def itemPosition(self, x, y):
        itemX0 = x * (self.itemSize + self.padding * 2) + self.padding * 2
        itemY0 = y * (self.itemSize + self.padding * 2) + self.padding * 2
        itemX1 = itemX0 + self.itemSize
        itemY1 = itemY0 + self.itemSize
        return itemX0, itemY0, itemX1, itemY1

    def draw(self, game):
        self.canvas.delete(ALL)
        for i in range(game.height):
            for j in range(game.width):
                itemX0, itemY0, itemX1, itemY1 = self.itemPosition(j, i)
                color = self.emptyColor
                item = game.board[i][j]
                if item == 1:
                    color = self.p1Color
                elif item == 2:
                    color = self.p2Color
                self.canvas.create_oval(itemX0, itemY0, itemX1, itemY1, fill=color)
        self._show_current_player(game)
        if self.game.end:
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            if self.game.endStatus != DRAW:
                t = (self.p1 if self.game.endStatus == P1_WIN else self.p2) + " WON!"
            else:
                t = "DRAW!"
            self.canvas.create_text(x, y, text=t, font=("Helvetica", 32), fill="#333")

    def _board_click(self, event):
        if self.solving:
            return
        if self.game.end:
            return
        if event.x < self.padding:
            position = 0
        elif event.x > self.width - self.padding:
            position = self.game.width - 1
        else:
            position = (event.x - self.padding) // (self.itemSize + self.padding * 2)
        if self.game.doAction(position):
            self.draw(self.game)
        if self.isAiMode and not self.game.end:
            self.doAiAction()
        if self.game.end:
            self.isAiMode = False

    def _click_new_game(self):
        self.newGame()

    def mcts_solver(self):
        self.solving = True
        solver = MCTS(self.game)
        visitResult, valueResult, actionResult = solver.doSearch()
        self.solving = False
        return visitResult, valueResult, actionResult

    def _click_solve_game(self):
        visitResult, valueResult, actionResult = self.mcts_solver()
        self.refresh()
        self.draw(self.game)
        for i, action in enumerate(actionResult):
            x = action
            y = self.game.height - self.game.nextStep[action] - 1
            itemX0, itemY0, itemX1, itemY1 = self.itemPosition(x, y)
            text = 'a: ' + str(action) + '\nn: ' + str(visitResult[i]) + '\nv: ' + str(valueResult[i])
            self.canvas.create_text(itemX0 + self.padding * 2, itemY0 + self.padding * 2, text=text, font=("Helvetica", 10), fill="#333")
        return 0

    def _click_save_game(self):
        with open(saveFile, 'wb') as f:
            data = pickle.dumps(self.game)
            pickle.dump(data, f)
            f.close()
            messagebox.showinfo("Save", "Game Saved")
        return 0

    def _click_load_game(self):
        with open(saveFile, 'rb') as f:
            data = pickle.load(f)
            f.close()
            self.game = pickle.loads(data)
            self.refresh()
            self.draw(self.game)
            messagebox.showinfo("Load", "Game Loaded")
        return 0

    def doAiAction(self):
        visitResult, valueResult, actionResult = self.mcts_solver()
        action = actionResult[visitResult.index(max(visitResult))]
        self.game.doAction(action)
        self.draw(self.game)

    def _click_ai_mode(self):
        if self.game.end:
            return
        self.isAiMode = True
        self.doAiAction()

    def newGame(self):
        self.isAiMode = False
        self.game.newGame()
        self.refresh()
        self.draw(self.game)

    def refresh(self):
        self.canvas.delete(ALL)
        self.canvas.config(width=self.width, height=self.height)
        self.window.update()
