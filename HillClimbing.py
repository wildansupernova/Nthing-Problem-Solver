from Board import Board
from typing import List
from PawnElement import PawnElement
import copy

class HillClimbing:
    def __init__(self, board: Board):
        self.board = board
    # Getter
    def getBoard(self) -> Board:
        return self.board
    def setBoard(self, newBoard):   
        self.board = copy.deepcopy(newBoard)

    # Hill Climbing Algorithm
    def algorithm(self) -> Board:
        neighbor = self.getBoard().chooseNextStatesFromListWithHighestScore()
        while neighbor.compareListOfPawnWithColor(self.getBoard()) > 0:
            self.setBoard(neighbor)
            # self.getBoard().printBoard()
            neighbor = self.getBoard().chooseNextStatesFromListWithHighestScore()
        return self.getBoard()
