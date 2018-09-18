from PawnElement import PawnElement
from PawnType import PawnType
from typing import List
import copy
"""
    Start index from 1-9
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