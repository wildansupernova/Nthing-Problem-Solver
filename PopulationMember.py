from PawnElement import PawnElement
from typing import List
import Board

class PopulationMember:

    def __init__(self, listOfPawn: List[PawnElement], board: Board):
        self.listOfPawn = listOfPawn
        self.board = board
        self.fitness = self.fitnessFunction(listOfPawn)

    # Fitness function non-attacking-same-colour + attacking-different-colour pawns
    def fitnessFunction(self, listOfPawn: List[PawnElement]):
        attackDif, attackSame = self.board.calculatePawnAttack(listOfPawn)
        nonAttackSame = len(listOfPawn) - attackSame
        return nonAttackSame + attackDif
    
