from PawnElement import PawnElement
from typing import List
from Board import Board

class PopulationMember:

    def __init__(self, board: Board):
        self.board = board
        self.fitness = self.fitnessFunction()

    def getBoard(self):
        return self.board
    
    def getFitness(self):
        return self.fitness

    # Fitness function non-attacking-same-colour + attacking-different-colour pawns
    def fitnessFunction(self):
        attackDif, attackSame = self.getBoard().calculatePawnAttack()
        nonAttackSame = self.getBoard().getLength() - attackSame
        return nonAttackSame + attackDif
    
