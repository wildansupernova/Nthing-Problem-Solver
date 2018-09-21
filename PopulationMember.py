from PawnElement import PawnElement
from typing import List

class PopulationMember:

    def __init__(self,listOfPawn: List[PawnElement]):
        self.listOfPawn = listOfPawn
        self.fitness = self.fitnessFunction(listOfPawn)

    # Fitness function non-attacking-same-colour + attacking-different-colour pawns
    def fitnessFunction(self, listOfPawn: List[PawnElement]):
        attackDif, attackSame = self.calculatePawnAttack(listOfPawn)
        nonAttackSame = len(listOfPawn) - attackSame
        return nonAttackSame + attackDif
    
