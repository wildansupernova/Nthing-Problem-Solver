from PawnElement import PawnElement
# from PopulationMember import PopulationMember
from typing import List
from PawnType import PawnType
import random
import numpy as np
import copy
import random
import math
"""
    Start index from 1-8
"""

class Board:

    NOT_FOUND = -1

    def __init__(self, listOfPawn):
        self.listOfPawn = copy.deepcopy(listOfPawn)

    def getListOfPawn(self):
        return self.listOfPawn
    
    def setListOfPawn(self, listOfPawn):
        self.listOfPawn = copy.deepcopy(listOfPawn)

    def getLength(self):
        return len(self.getListOfPawn())
    # Check if element on Idx is unique (the coordinate) in list or not
    def isIdxthElementUniqueInList(self, idx):
        found = False
        for i in range(0,self.getLength()):
            if i != idx:
                if self.getListOfPawn()[i].isInTheSamePlace(self.getListOfPawn()[idx]):
                    found = True
        return not(found)

    # Randomize the location of pawns, every pawn in unique coordinate
    def initRandomState(self):
        n = self.getLength()
        randomizedPawn = self.getListOfPawn()

        for i in range(0, n):
            randomizedPawn[i].randomizeRowColumn()
            while not(self.isIdxthElementUniqueInList(i)):
                randomizedPawn[i].randomizeRowColumn()
        
    # Count the Neighbor
    def countNeighbor(self):
        n = self.getLength()
        count = 0
        for i in range(0, n):
            for j in range(1,9):
                for k in range(1,9):
                    if self.isEmptyCell(j,k):
                        count += 1
        return count

    # Select random neighbor at idx
    def selectNeighbor(self, idx):
        n = self.getLength()
        count = 0
        listOfPawn = self.getListOfPawn()
        for i in range(0, n):
            for j in range(1,9):
                for k in range(1,9):
                    if self.isEmptyCell(j,k):
                        count += 1

                        if count == idx:
                            tempState = copy.deepcopy(self)
                            newBoardList = tempState.getListOfPawn()
                            newBoardList[i].row = j
                            newBoardList[i].column = k

                            return tempState
    # Check if row, column empty
    def isEmptyCell(self, row, column):
        found = False
        for element in self.getListOfPawn():
            if element.isTheSameCoordinate(row, column):
                found = True
                break
        return not(found)
    
    # Check if coordinate in 8x8 chess
    def isValidCoordinate(self, row, column):
        return row >= 1 and row <= 8 and column >= 1 and column <= 8 

    # Choose from list of enumerated states that has highest score
    def chooseNextStatesFromListWithHighestScore(self):
        n = self.getLength()
        highestScoreState = None
        for i in range(0, n):
            for j in range(1,9):
                for k in range(1,9):
                    if self.isEmptyCell(j,k):
                        tempState = copy.deepcopy(self)
                        tempStateList = tempState.getListOfPawn()
                        tempStateList[i].row = j
                        tempStateList[i].column = k

                        if highestScoreState == None:
                            highestScoreState = tempState
                        elif tempState.compareListOfPawnWithColor(highestScoreState) > 0:
                            highestScoreState = tempState
        return highestScoreState

    # Choose next state from list randomly
    def chooseNextStatesFromListRandomly(self, compareFunction):
        n = self.getLength()
        chosenState = None
        while True:
            i = random.randint(0,n-1)
            j = random.randint(1,8)
            k = random.randint(1,8)
            if self.isEmptyCell(j,k) and self.isValidCoordinate(j,k):
                tempState = copy.deepcopy(self.getListOfPawn())
                tempState[i].row = j
                tempState[i].colom = k
                chosenState = tempState
                break
        return chosenState

    # Return 1 if A > B, 0 if A == B and -1 if A < B
    def compareListOfPawnWithColor(self, otherBoard):
        scoreA = self.scoringListOfPawnWithColor()
        scoreB = otherBoard.scoringListOfPawnWithColor()
        if scoreA > scoreB:
            result = 1
        elif scoreA == scoreB:
            result = 0
        else:
            result = -1
        return result

    # Making list of scores from all pawns
    def scoringListOfPawnWithColor(self) -> int:
        n = self.getLength()
        scoreIntersectingDifferentColor = 0
        scoreIntersectingSameColor = 0
        for i in range(0, n):
            tempScoreIntersectingDifferentColor = 0
            tempScoreIntersectingSameColor = 0
            
            tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor = self.countPawnElementAttack(i)

            scoreIntersectingDifferentColor += tempScoreIntersectingDifferentColor
            scoreIntersectingSameColor += tempScoreIntersectingSameColor 

        return abs(scoreIntersectingDifferentColor - scoreIntersectingSameColor)

    # Making neighbours' score for knights
    def scoringKnightWithColor(self, idx) -> (int, int):
        scoreIntersectingDifferentColor = 0
        scoreIntersectingSameColor = 0
        rowTransition = [-1, -1, 1, 1, -2, 2, -2, 2]
        columnTransition = [-2, 2, -2, 2, -1, -1, 1, 1]
        nPossibility = len(rowTransition)
        listOfPawn = self.getListOfPawn()
        for i in range(0,nPossibility):
            rowMove = listOfPawn[idx].row + rowTransition[i]
            columnMove = listOfPawn[idx].column + columnTransition[i]

            if self.isValidCoordinate(rowMove, columnMove):
                searchResult = self.findElementWithCoordinate(rowMove, columnMove)
                if searchResult != self.NOT_FOUND:
                    if listOfPawn[searchResult].pawnColor == listOfPawn[idx].pawnColor:
                        scoreIntersectingSameColor += 1
                    else:
                        scoreIntersectingDifferentColor += 1


        return scoreIntersectingDifferentColor, scoreIntersectingSameColor

    # Making neighbours' scores for bishop break if found
    def scoringBishopWithColor(self, idx) -> (int, int):
        rowTransition = [-1, -1, 1, 1]
        columnTransition = [-1, 1, -1, 1]
        nDirection = len(rowTransition)
        scoreIntersectingDifferentColor = 0
        scoreIntersectingSameColor = 0
        listOfPawn = self.getListOfPawn()

        for i in range(0, nDirection):
            rNow = listOfPawn[idx].row
            cNow = listOfPawn[idx].column
            while True:
                rNow = rNow + rowTransition[i]
                cNow = cNow + columnTransition[i]
                if self.isValidCoordinate(rNow,cNow):
                    searchResult = self.findElementWithCoordinate(rNow, cNow)
                    if searchResult != self.NOT_FOUND:
                        if listOfPawn[searchResult].pawnColor == listOfPawn[idx].pawnColor:
                            scoreIntersectingSameColor += 1
                        else:
                            scoreIntersectingDifferentColor += 1
                        break                     
                else:
                    break
        return scoreIntersectingDifferentColor, scoreIntersectingSameColor

    # Making neighbours' scores for Rook, break if found
    def scoringRookWithColor(self, idx) -> (int, int):
        rowTransition = [-1, 0, 0, 1]
        columnTransition = [0, -1, 1, 0]
        nDirection = len(rowTransition)
        scoreIntersectingDifferentColor = 0
        scoreIntersectingSameColor = 0
        listOfPawn = self.getListOfPawn()   
        for i in range(0, nDirection):
            rNow = listOfPawn[idx].row
            cNow = listOfPawn[idx].column
            while True:
                rNow = rNow + rowTransition[i]
                cNow = cNow + columnTransition[i]
                if self.isValidCoordinate(rNow,cNow):
                    searchResult = self.findElementWithCoordinate(rNow, cNow)
                    if searchResult != self.NOT_FOUND:
                        if listOfPawn[searchResult].pawnColor == listOfPawn[idx].pawnColor:
                            scoreIntersectingSameColor += 1
                        else:
                            scoreIntersectingDifferentColor += 1   
                        break                     
                else:
                    break
        return scoreIntersectingDifferentColor, scoreIntersectingSameColor

    # Print the board
    def printBoard(self):
        resultString = ""
        listOfPawn = self.getListOfPawn()
        for i in range(1, 9):
            for j in range(1, 9):
                result = self.findElementWithCoordinate(i, j)
                if result == self.NOT_FOUND:
                    resultString += "."
                elif listOfPawn[result].pawnElement == PawnType.KNIGHT:
                    resultChar = "K"
                    if listOfPawn[result].pawnColor == PawnType.BLACK :
                        resultChar = "k"
                    resultString += resultChar
                elif listOfPawn[result].pawnElement == PawnType.BISHOP:
                    resultChar = "B"
                    if listOfPawn[result].pawnColor == PawnType.BLACK :
                        resultChar = "b"
                    resultString += resultChar
                elif listOfPawn[result].pawnElement == PawnType.ROOK:
                    resultChar = "R"
                    if listOfPawn[result].pawnColor == PawnType.BLACK :
                        resultChar = "r"   
                    resultString += resultChar 
                elif listOfPawn[result].pawnElement == PawnType.QUEEN:
                    resultChar = "Q"
                    if listOfPawn[result].pawnColor == PawnType.BLACK :
                        resultChar = "q"      
                    resultString += resultChar
            resultString += "\n"              
        print(resultString)

    # Count pawns attacking pawnIdx
    def countPawnElementAttack(self, pawnIdx) -> (int, int):
        listOfPawn = self.getListOfPawn()
        if listOfPawn[pawnIdx].pawnElement == PawnType.KNIGHT :
            tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor = self.scoringKnightWithColor(pawnIdx)
        elif listOfPawn[pawnIdx].pawnElement == PawnType.BISHOP:
            tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor = self.scoringBishopWithColor(pawnIdx)
        elif listOfPawn[pawnIdx].pawnElement == PawnType.ROOK:
            tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor = self.scoringRookWithColor(pawnIdx)
        elif listOfPawn[pawnIdx].pawnElement == PawnType.QUEEN:
            tempScoreIntersectingDifferentColor1, tempScoreIntersectingSameColor1 = self.scoringRookWithColor(pawnIdx)
            tempScoreIntersectingDifferentColor2, tempScoreIntersectingSameColor2 = self.scoringBishopWithColor(pawnIdx)
            
            tempScoreIntersectingDifferentColor = tempScoreIntersectingDifferentColor1 + tempScoreIntersectingDifferentColor2
            tempScoreIntersectingSameColor = tempScoreIntersectingSameColor1 + tempScoreIntersectingSameColor2
        return tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor

    # Calculate numbers of Pawn Attack
    def calculatePawnAttack(self) -> (int, int):
        n = self.getLength()
        scoreIntersectingDifferentColor = 0
        scoreIntersectingSameColor = 0
        for i in range(0, n):
            tempScoreIntersectingDifferentColor = 0
            tempScoreIntersectingSameColor = 0
            tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor = self.countPawnElementAttack(i)
            if tempScoreIntersectingDifferentColor != 0 :
                scoreIntersectingDifferentColor += 1
            if tempScoreIntersectingSameColor != 0 :
                # print(tempScoreIntersectingSameColor)
                # print(listOfPawn[i].__dict__)
                scoreIntersectingSameColor += 1
        return scoreIntersectingDifferentColor, scoreIntersectingSameColor

    # Find in listOfPawn in specific row and column
    def findElementWithCoordinate(self, row, column):
        n = self.getLength()
        listOfPawn = self.getListOfPawn()
        for i in range(0, n):
            if listOfPawn[i].isTheSameCoordinate(row, column):
                return i
        return self.NOT_FOUND
