from PawnElement import PawnElement
from typing import List
from Board import Board
import copy

class PopulationMember:

    def __init__(self, board: Board):
        self.board = copy.deepcopy(board)
        self.fitness = self.fitnessFunction()

    def getBoard(self):
        return self.board

    def setBoard(self, board):
        self.board = copy.deepcopy(board)
        self.fitness = self.fitnessFunction()
    
    def getFitness(self):
        return self.fitness

    # Fitness function non-attacking-same-colour + attacking-different-colour pawns
    def fitnessFunction(self):
        """
        attackDiff, attackSame = self.getBoard().calculatePawnAttack()
        nonAttackSame = self.getBoard().getLength() - attackSame
        return nonAttackSame + attackDiff
        """
        return self.board.scoringListOfPawnWithColor()