# Use Monte Carlo Tree Search (MCTS) algorithm for Connect Four Game.

The project is a connect four game.  The rules for this game can check [here](https://en.wikipedia.org/wiki/Connect_Four).
This document will introduce the project in two sections.


# How to play

There are five actions total:
1. New Game: Clean the board and start a new game. Blue always play first.
2. Solver: MCTS algorithm will give an estimation of all actions in [0,6], including **n** for visited times and **p** for average score.
![img.png](figures%2Fimg.png)
3. Save: Save the current board.
4. Load: Load the last saved board.
5. AIPlayer: Play with our AI! It will start play whenever you click the button.

**NOTE**: Can only save one game! We have a default game saved.

# Project structure
ConnectFour.py is the class represents a connect four game.
GameSolver.py is the class represents the MCTS algorithm. It takes any ConnectFour game and give the estimation for all available actions.
GameUI.py is the class renders the UI.
main.py is where we start the application.