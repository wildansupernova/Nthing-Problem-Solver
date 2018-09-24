from Board import Board
from PawnElement import PawnElement
from typing import List

def makingInput(listOfPawn: List[PawnElement]):
    n = int(input())
    while n>0: 
        inp: str = input()
        splitResult = inp.split(" ")
        numberOfThisPawn = int(splitResult[2])
        while numberOfThisPawn>0: 
            newElementPawn = PawnElement(splitResult[1], splitResult[0])
            listOfPawn.append(newElementPawn)
            numberOfThisPawn -= 1
        n -= 1
'''
def printList(listOfPawn: List[PawnElement]):
    for element in listOfPawn:
        print(element.__dict__)
'''

listOfPawn = []
makingInput(listOfPawn)
board = Board(listOfPawn)

board.initRandomState(listOfPawn)
board.printBoard(listOfPawn)

print("Ini hill climbing")
hillClimbingResult = board.hillClimbing(board.listOfPawn)
board.printBoard(hillClimbingResult)
differentColor, sameColor = board.calculatePawnAttack(hillClimbingResult)
print(str(sameColor) + " " + str(differentColor))
print(board.scoringListOfPawnWithColor(hillClimbingResult))

print("\n")
print("Ini Simulated Annealing")
simulatedAnnealingResult = board.simulatedAnnealing(board.listOfPawn, 1000, 10, 10)
board.printBoard(simulatedAnnealingResult)
differentColor, sameColor = board.calculatePawnAttack(simulatedAnnealingResult)
print(str(sameColor) + " " + str(differentColor))
print(board.scoringListOfPawnWithColor(simulatedAnnealingResult))

print("\n")
print("Ini GA")
generations = 50
probCross = 1
probMuta = 1
geneticAlgorithmResult = board.geneticAlgorithm(board.listOfPawn, probCross, probMuta, generations)
board.printBoard(geneticAlgorithmResult)
differentColor, sameColor = board.calculatePawnAttack(geneticAlgorithmResult)
print(str(sameColor) + " " + str(differentColor))
print(board.scoringListOfPawnWithColor(geneticAlgorithmResult))
