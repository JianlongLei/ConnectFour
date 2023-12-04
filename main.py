from tkinter import *

from ConnectFour import ConnectFour
from GameUI import GameUI

if __name__ == '__main__':
    window = Tk()
    game = ConnectFour()
    app = GameUI(window, game)
    window.mainloop()

