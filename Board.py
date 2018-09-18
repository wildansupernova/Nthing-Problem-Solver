from PawnElement import PawnElement
from PawnType import PawnType
from typing import List
import copy
"""
    Start index from 1-8
"""

class Board:

    def __init__(self, listOfPawnElement):
        self.listOfPawnElement = listOfPawnElement
        
    def isIdxthElementUniqueInList(self, idx, listOfPawnElement):
        found = False
        for i in range(0,len(listOfPawnElement)):
            if i != idx:
                if listOfPawnElement[i].isInTheSamePlace(listOfPawnElement[idx]):
                    found = True
        return not(found)

    def initRandomState(self):
        n = len(self.listOfPawnElement)

        for i in range(0, n):
            self.listOfPawnElement[i].randomizeRowColom()
            while not(self.isIdxthElementUniqueInList(i, self.listOfPawnElement)):
                self.listOfPawnElement[i].randomizeRowColom()

    def isEmptyCell(self, row, colom, listOfPawnElement):
        found = False
        for element in listOfPawnElement:
            if element.isTheSameCoordinate(row, colom):
                found = True
                break
        return not(found)

    def isValidCoordinate(self, row, colom):
        return row >= 1 and row <= 8 and colom >= 1 and colom <=8 

    def addStateKnight(self, i, states: List[List[PawnElement]], listOfPawnElement: List[PawnElement]):
        rowTransition = [-1, -1, 1, 1, -2, 2, -2, 2]
        colomTransition = [-2, 2, -2, 2, -1, -1, 1, 1]
        nPossibility = len(rowTransition)

        for j in range(0, nPossibility):
            rowNowForIdxI = listOfPawnElement[i].row + rowTransition[j]
            colomNowForIdxI = listOfPawnElement[i].colom + colomTransition[j]

            if self.isEmptyCell(rowNowForIdxI, colomNowForIdxI, listOfPawnElement) and self.isValidCoordinate(rowNowForIdxI,colomNowForIdxI):
                newState = copy.deepcopy(listOfPawnElement)
                newState[i].row = rowNowForIdxI
                newState[i].colom = colomNowForIdxI
                states.append(newState)

    def addStateBishop(self, i, states: List[List[PawnElement]], listOfPawnElement: List[PawnElement]):
        rowTransition = [-1, -1, 1, 1]
        colomTransition = [-1, 1, -1, 1]
        nDirection = len(rowTransition)
        for j in range(0, nDirection):
            rNow = listOfPawnElement[i].row
            cNow = listOfPawnElement[i].colom
            while True:
                rNow = listOfPawnElement[i].row + rowTransition[j]
                cNow = listOfPawnElement[i].colom + colomTransition[j]
                if self.isEmptyCell(rNow, cNow, listOfPawnElement) and self.isValidCoordinate(rNow,cNow):
                    newState = copy.deepcopy(listOfPawnElement)
                    newState[i].row = rNow
                    newState[i].colom = cNow
                    states.append(newState)
                else:
                    break
    def addStateRook(self, i, states: List[List[PawnElement]], listOfPawnElement: List[PawnElement]):
        rowTransition = [-1, 0, 0, 1]
        colomTransition = [0, -1, 1, 0]
        nDirection = len(rowTransition)
        for j in range(0, nDirection):
            rNow = listOfPawnElement[i].row
            cNow = listOfPawnElement[i].colom
            while True:
                rNow = listOfPawnElement[i].row + rowTransition[j]
                cNow = listOfPawnElement[i].colom + colomTransition[j]
                if self.isEmptyCell(rNow, cNow, listOfPawnElement) and self.isValidCoordinate(rNow,cNow):
                    newState = copy.deepcopy(listOfPawnElement)
                    newState[i].row = rNow
                    newState[i].colom = cNow
                    states.append(newState)
                else:
                    break
    def makeNextStatesFromList(self, listOfPawnElement: List[PawnElement]):
        states = []
        n = len(listOfPawnElement)
        for i in range(0, n):
            if listOfPawnElement[i].pawnElement == PawnType.KNIGHT :
                self.addStateKnight(i, states, listOfPawnElement)
            elif listOfPawnElement[i].pawnElement == PawnType.BISHOP:
                self.addStateBishop(i, states, listOfPawnElement)
            elif listOfPawnElement[i].pawnElement == PawnType.ROOK:
                self.addStateRook(i, states, listOfPawnElement)
            elif listOfPawnElement[i].pawnElement == PawnType.QUEEN:
                self.addStateBishop(i, states, listOfPawnElement)
                self.addStateRook(i, states, listOfPawnElement)
        return states