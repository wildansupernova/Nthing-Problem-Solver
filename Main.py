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

def printList(listOfPawn: List[PawnElement]):
    for element in listOfPawn:
        print(element.__dict__)
listOfPawn = []
makingInput(listOfPawn)
board = Board(listOfPawn)

board.initRandomState(board.listOfPawn)
board.printBoard(board.listOfPawn)

