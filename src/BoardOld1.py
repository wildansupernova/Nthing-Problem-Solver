from PawnElement import PawnElement
from typing import List
from PawnType import PawnType
import copy

"""
    Start index from 1-8
"""

class Board:

    NOT_FOUND = -1

    def __init__(self, listOfPawn):
        self.listOfPawn = listOfPawn
        
    def isIdxthElementUniqueInList(self, idx, listOfPawn):
        found = False
        for i in range(0,len(listOfPawn)):
            if i != idx:
                if listOfPawn[i].isInTheSamePlace(listOfPawn[idx]):
                    found = True
        return not(found)

    def initRandomState(self, listOfPawn):
        n = len(listOfPawn)

        for i in range(0, n):
            listOfPawn[i].randomizeRowColom()
            while not(self.isIdxthElementUniqueInList(i, listOfPawn)):
                listOfPawn[i].randomizeRowColom()

    def hillClimbing(self, listOfPawn: List[PawnElement]) -> List[PawnElement]:
        newStateListPawn = copy.deepcopy(listOfPawn)
        neighbor = self.chooseNextStatesFromListWithHighestScore(listOfPawn, self.compareListOfPawnWithColorDifferenceWay)
        while self.compareListOfPawnWithColorDifferenceWay(neighbor, newStateListPawn) > 0:
            newStateListPawn = neighbor
            neighbor = self.chooseNextStatesFromListWithHighestScore(newStateListPawn, self.compareListOfPawnWithColorDifferenceWay)
        return newStateListPawn

    def hillClimbingNotAttackSameColor(self, listOfPawn: List[PawnElement]) -> List[PawnElement]:
        newStateListPawn = copy.deepcopy(listOfPawn)
        neighbor = self.chooseNextStatesFromListWithHighestScore(listOfPawn, self.compareListOfPawnWithColorNotAttackSameColor)
        while self.compareListOfPawnWithColorNotAttackSameColor(neighbor, newStateListPawn) > 0:
            newStateListPawn = neighbor
            neighbor = self.chooseNextStatesFromListWithHighestScore(newStateListPawn, self.compareListOfPawnWithColorNotAttackSameColor)
        return newStateListPawn

    def isEmptyCell(self, row, colom, listOfPawn):
        found = False
        for element in listOfPawn:
            if element.isTheSameCoordinate(row, colom):
                found = True
                break
        return not(found)

    def isValidCoordinate(self, row, colom):
        return row >= 1 and row <= 8 and colom >= 1 and colom <=8 

    def chooseNextStatesFromListWithHighestScore(self, listOfPawn: List[PawnElement], compareFunction):
        n = len(listOfPawn)
        highestScoreState = None
        for i in range(0, n):
            for j in range(1,9):
                for k in range(1,9):
                    if self.isEmptyCell(j,k,listOfPawn):
                        tempState = copy.deepcopy(listOfPawn)
                        tempState[i].row = j
                        tempState[i].colom = k

                        if highestScoreState == None:
                            highestScoreState = tempState
                        elif compareFunction(tempState, highestScoreState) > 0:
                            highestScoreState = tempState
        return highestScoreState

    def compareListOfPawnWithColorDifferenceWay(self, listOfPawnA: List[PawnElement], listOfPawnB: List[PawnElement]):
        scoreA = self.scoringListOfPawnWithColorDifferenceWay(listOfPawnA)
        scoreB = self.scoringListOfPawnWithColorDifferenceWay(listOfPawnB)
        if scoreA > scoreB:
            result = 1
        elif scoreA == scoreB:
            result = 0
        else:
            result = -1
        return result

    def compareListOfPawnWithColorNotAttackSameColor(self, listOfPawnA: List[PawnElement], listOfPawnB: List[PawnElement]):
        scoreAAttackDifferentColor = self.scoringListOfPawnWithColorNotAttackSameColor(listOfPawnA)
        scoreBAttackDifferentColor = self.scoringListOfPawnWithColorNotAttackSameColor(listOfPawnB)
        if scoreAAttackDifferentColor > scoreBAttackDifferentColor:
            result = 1
        elif scoreAAttackDifferentColor == scoreBAttackDifferentColor:
            result = 0
        else:
            result = -1
        return result

    def scoringListOfPawnWithColorDifferenceWay(self, listOfPawn: List[PawnElement]) -> int:
        n = len(listOfPawn)
        scoreIntersectionDifferentColor = 0
        scoreIntersectionSameColor = 0
        for i in range(0, n):
            tempScoreIntersectionDifferentColor = 0
            tempScoreIntersectionSameColor = 0
            if listOfPawn[i].pawnElement == PawnType.KNIGHT :
                tempScoreIntersectionDifferentColor, tempScoreIntersectionSameColor = self.scoringKnightWithColor(listOfPawn, i)
            elif listOfPawn[i].pawnElement == PawnType.BISHOP:
                tempScoreIntersectionDifferentColor, tempScoreIntersectionSameColor = self.scoringBishopWithColor(listOfPawn, i)
            elif listOfPawn[i].pawnElement == PawnType.ROOK:
                tempScoreIntersectionDifferentColor, tempScoreIntersectionSameColor = self.scoringRookWithColor(listOfPawn, i)
            elif listOfPawn[i].pawnElement == PawnType.QUEEN:
                tempScoreIntersectionDifferentColor1, tempScoreIntersectionSameColor1 = self.scoringRookWithColor(listOfPawn, i)
                tempScoreIntersectionDifferentColor2, tempScoreIntersectionSameColor2 = self.scoringBishopWithColor(listOfPawn, i)
                
                tempScoreIntersectionDifferentColor = tempScoreIntersectionDifferentColor1 + tempScoreIntersectionDifferentColor2
                tempScoreIntersectionSameColor = tempScoreIntersectionSameColor1 + tempScoreIntersectionSameColor2
            scoreIntersectionDifferentColor += tempScoreIntersectionDifferentColor
            scoreIntersectionSameColor += tempScoreIntersectionSameColor 
        return abs(scoreIntersectionDifferentColor - scoreIntersectionSameColor)

    def scoringListOfPawnWithColorNotAttackSameColor(self, listOfPawn: List[PawnElement]) -> int:
        n = len(listOfPawn)
        scoreIntersectionDifferentColor = 0
        scoreIntersectionEmptySuccessor = 0
        for i in range(0, n):
            tempScoreIntersectionDifferentColor = 0
            tempScoreIntersectionEmptySuccessor = 0
            if listOfPawn[i].pawnElement == PawnType.KNIGHT :
                tempScoreIntersectionDifferentColor = self.scoringKnightWithDifferentColor(listOfPawn, i)
                tempScoreIntersectionEmptySuccessor = self.scoringKnightWithEmptySuccessor(listOfPawn, i)
            elif listOfPawn[i].pawnElement == PawnType.BISHOP:
                tempScoreIntersectionDifferentColor = self.scoringBishopWithDifferentColor(listOfPawn, i)
                tempScoreIntersectionEmptySuccessor = self.scoringBishopWithEmptySuccessor(listOfPawn, i)
            elif listOfPawn[i].pawnElement == PawnType.ROOK:
                tempScoreIntersectionDifferentColor = self.scoringRookWithDifferentColor(listOfPawn, i)
                tempScoreIntersectionEmptySuccessor = self.scoringRookWithEmptySuccessor(listOfPawn, i)
            elif listOfPawn[i].pawnElement == PawnType.QUEEN:
                tempScoreIntersectionDifferentColor1 = self.scoringBishopWithDifferentColor(listOfPawn, i)
                tempScoreIntersectionEmptySuccessor1 = self.scoringBishopWithEmptySuccessor(listOfPawn, i)

                tempScoreIntersectionDifferentColor2 = self.scoringRookWithDifferentColor(listOfPawn, i)
                tempScoreIntersectionEmptySuccessor2 = self.scoringRookWithEmptySuccessor(listOfPawn, i)

                tempScoreIntersectionDifferentColor = tempScoreIntersectionDifferentColor1 + tempScoreIntersectionDifferentColor2
                tempScoreIntersectionEmptySuccessor = tempScoreIntersectionEmptySuccessor1 + tempScoreIntersectionEmptySuccessor2
            scoreIntersectionDifferentColor += tempScoreIntersectionDifferentColor
            scoreIntersectionEmptySuccessor += tempScoreIntersectionEmptySuccessor 
        print(scoreIntersectionDifferentColor + scoreIntersectionEmptySuccessor)
        return scoreIntersectionDifferentColor + scoreIntersectionEmptySuccessor

    def scoringKnightWithColor(self, listOfPawn: List[PawnElement], idx) -> (int, int):
        scoreIntersectionDifferentColor = 0
        scoreIntersectionSameColor = 0
        rowTransition = [-1, -1, 1, 1, -2, 2, -2, 2]
        colomTransition = [-2, 2, -2, 2, -1, -1, 1, 1]
        nPossibility = len(rowTransition)

        for i in range(0,nPossibility):
            rowMove = listOfPawn[idx].row + rowTransition[i]
            colomMove = listOfPawn[idx].colom + colomTransition[i]

            if self.isValidCoordinate(rowMove, colomMove):
                searchResult = self.findElementWithCoordinate(rowMove, colomMove, listOfPawn)
                if searchResult != self.NOT_FOUND:
                    if listOfPawn[searchResult].pawnColor == listOfPawn[idx].pawnColor:
                        scoreIntersectionSameColor += 1
                    else:
                        scoreIntersectionDifferentColor += 1
        return scoreIntersectionDifferentColor, scoreIntersectionSameColor

    def scoringBishopWithColor(self, listOfPawn: List[PawnElement], idx) -> (int, int):
        rowTransition = [-1, -1, 1, 1]
        colomTransition = [-1, 1, -1, 1]
        nDirection = len(rowTransition)
        scoreIntersectionDifferentColor = 0
        scoreIntersectionSameColor = 0

        for i in range(0, nDirection):
            rNow = listOfPawn[idx].row
            cNow = listOfPawn[idx].colom
            while True:
                rNow = rNow + rowTransition[i]
                cNow = cNow + colomTransition[i]
                if self.isValidCoordinate(rNow,cNow):
                    searchResult = self.findElementWithCoordinate(rNow, cNow, listOfPawn)
                    if searchResult != self.NOT_FOUND:
                        if listOfPawn[searchResult].pawnColor == listOfPawn[idx].pawnColor:
                            scoreIntersectionSameColor += 1
                        else:
                            scoreIntersectionDifferentColor += 1
                        break                     
                else:
                    break
        return scoreIntersectionDifferentColor, scoreIntersectionSameColor
    
    def scoringRookWithColor(self, listOfPawn: List[PawnElement], idx) -> (int, int):
        rowTransition = [-1, 0, 0, 1]
        colomTransition = [0, -1, 1, 0]
        nDirection = len(rowTransition)
        scoreIntersectionDifferentColor = 0
        scoreIntersectionSameColor = 0

        for i in range(0, nDirection):
            rNow = listOfPawn[idx].row
            cNow = listOfPawn[idx].colom
            while True:
                rNow = rNow + rowTransition[i]
                cNow = cNow + colomTransition[i]
                if self.isValidCoordinate(rNow,cNow):
                    searchResult = self.findElementWithCoordinate(rNow, cNow, listOfPawn)
                    if searchResult != self.NOT_FOUND:
                        if listOfPawn[searchResult].pawnColor == listOfPawn[idx].pawnColor:
                            scoreIntersectionSameColor += 1
                        else:
                            scoreIntersectionDifferentColor += 1   
                        break                     
                else:
                    break
        return scoreIntersectionDifferentColor, scoreIntersectionSameColor

    def scoringKnightWithDifferentColor(self, listOfPawn: List[PawnElement], idx) -> int:
        scoreIntersectionDifferentColor = 0
        rowTransition = [-1, -1, 1, 1, -2, 2, -2, 2]
        colomTransition = [-2, 2, -2, 2, -1, -1, 1, 1]
        nPossibility = len(rowTransition)

        for i in range(0,nPossibility):
            rowMove = listOfPawn[idx].row + rowTransition[i]
            colomMove = listOfPawn[idx].colom + colomTransition[i]

            if self.isValidCoordinate(rowMove, colomMove):
                searchResult = self.findElementWithCoordinate(rowMove, colomMove, listOfPawn)
                if searchResult != self.NOT_FOUND:
                    if listOfPawn[searchResult].pawnColor != listOfPawn[idx].pawnColor:
                        scoreIntersectionDifferentColor += 1
        return scoreIntersectionDifferentColor

    def scoringBishopWithDifferentColor(self, listOfPawn: List[PawnElement], idx) -> int:
        rowTransition = [-1, -1, 1, 1]
        colomTransition = [-1, 1, -1, 1]
        nDirection = len(rowTransition)
        scoreIntersectionDifferentColor = 0

        for i in range(0, nDirection):
            rNow = listOfPawn[idx].row
            cNow = listOfPawn[idx].colom
            while True:
                rNow = rNow + rowTransition[i]
                cNow = cNow + colomTransition[i]
                if self.isValidCoordinate(rNow,cNow):
                    searchResult = self.findElementWithCoordinate(rNow, cNow, listOfPawn)
                    if searchResult != self.NOT_FOUND:
                        if listOfPawn[searchResult].pawnColor != listOfPawn[idx].pawnColor:
                            scoreIntersectionDifferentColor += 1
                        break                     
                else:
                    break
        return scoreIntersectionDifferentColor

    def scoringRookWithDifferentColor(self, listOfPawn: List[PawnElement], idx) -> int:
        rowTransition = [-1, 0, 0, 1]
        colomTransition = [0, -1, 1, 0]
        nDirection = len(rowTransition)
        scoreIntersectionDifferentColor = 0
        
        for i in range(0, nDirection):
            rNow = listOfPawn[idx].row
            cNow = listOfPawn[idx].colom
            while True:
                rNow = rNow + rowTransition[i]
                cNow = cNow + colomTransition[i]
                if self.isValidCoordinate(rNow,cNow):
                    searchResult = self.findElementWithCoordinate(rNow, cNow, listOfPawn)
                    if searchResult != self.NOT_FOUND:
                        if listOfPawn[searchResult].pawnColor != listOfPawn[idx].pawnColor:
                            scoreIntersectionDifferentColor += 1   
                        break                     
                else:
                    break
        return scoreIntersectionDifferentColor

    def scoringKnightWithEmptySuccessor(self, listOfPawn: List[PawnElement], idx) -> int:
        scoreEmptySuccessor = 0
        rowTransition = [-1, -1, 1, 1, -2, 2, -2, 2]
        colomTransition = [-2, 2, -2, 2, -1, -1, 1, 1]
        nPossibility = len(rowTransition)

        for i in range(0,nPossibility):
            rowMove = listOfPawn[idx].row + rowTransition[i]
            colomMove = listOfPawn[idx].colom + colomTransition[i]

            if self.isValidCoordinate(rowMove, colomMove):
                searchResult = self.findElementWithCoordinate(rowMove, colomMove, listOfPawn)
                if searchResult == self.NOT_FOUND:
                    scoreEmptySuccessor += 1
        return scoreEmptySuccessor  

    def scoringBishopWithEmptySuccessor(self, listOfPawn: List[PawnElement], idx) -> int:
        rowTransition = [-1, -1, 1, 1]
        colomTransition = [-1, 1, -1, 1]
        nDirection = len(rowTransition)
        scoreEmptySuccessor = 0

        for i in range(0, nDirection):
            rNow = listOfPawn[idx].row
            cNow = listOfPawn[idx].colom
            while True:
                rNow = rNow + rowTransition[i]
                cNow = cNow + colomTransition[i]
                if self.isValidCoordinate(rNow,cNow):
                    searchResult = self.findElementWithCoordinate(rNow, cNow, listOfPawn)
                    if searchResult != self.NOT_FOUND:
                        break
                    else:
                        scoreEmptySuccessor += 1
                else:
                    break
        return scoreEmptySuccessor
    
    def scoringRookWithEmptySuccessor(self, listOfPawn: List[PawnElement], idx) -> int:
        rowTransition = [-1, 0, 0, 1]
        colomTransition = [0, -1, 1, 0]
        nDirection = len(rowTransition)
        scoreEmptySuccessor = 0
        
        for i in range(0, nDirection):
            rNow = listOfPawn[idx].row
            cNow = listOfPawn[idx].colom
            while True:
                rNow = rNow + rowTransition[i]
                cNow = cNow + colomTransition[i]
                if self.isValidCoordinate(rNow,cNow):
                    searchResult = self.findElementWithCoordinate(rNow, cNow, listOfPawn)
                    if searchResult != self.NOT_FOUND: 
                        break
                    else:
                        scoreEmptySuccessor += 1
                else:
                    break
        return scoreEmptySuccessor

    def printBoard(self, listOfPawn: List[PawnElement]):
        resultString = ""
        for i in range(1, 9):
            for j in range(1, 9):
                result = self.findElementWithCoordinate(i, j, listOfPawn)
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

    def calculatePawnThatAttackSameOrDifferentColor(self, listOfPawn: List[PawnElement]) -> (int, int):
        n = len(listOfPawn)
        scoreIntersectionDifferentColor = 0
        scoreIntersectionSameColor = 0
        for i in range(0, n):
            tempScoreIntersectionDifferentColor = 0
            tempScoreIntersectionSameColor = 0
            if listOfPawn[i].pawnElement == PawnType.KNIGHT :
                tempScoreIntersectionDifferentColor, tempScoreIntersectionSameColor = self.scoringKnightWithColor(listOfPawn, i)
            elif listOfPawn[i].pawnElement == PawnType.BISHOP:
                tempScoreIntersectionDifferentColor, tempScoreIntersectionSameColor = self.scoringBishopWithColor(listOfPawn, i)
            elif listOfPawn[i].pawnElement == PawnType.ROOK:
                tempScoreIntersectionDifferentColor, tempScoreIntersectionSameColor = self.scoringRookWithColor(listOfPawn, i)
            elif listOfPawn[i].pawnElement == PawnType.QUEEN:
                tempScoreIntersectionDifferentColor1, tempScoreIntersectionSameColor1 = self.scoringRookWithColor(listOfPawn, i)
                tempScoreIntersectionDifferentColor2, tempScoreIntersectionSameColor2 = self.scoringBishopWithColor(listOfPawn, i)

                tempScoreIntersectionDifferentColor = tempScoreIntersectionDifferentColor1 + tempScoreIntersectionDifferentColor2
                tempScoreIntersectionSameColor = tempScoreIntersectionSameColor1 + tempScoreIntersectionSameColor2
            if tempScoreIntersectionDifferentColor != 0 :
                scoreIntersectionDifferentColor += 1
            if tempScoreIntersectionSameColor != 0 :
                scoreIntersectionSameColor += 1
        return scoreIntersectionDifferentColor, scoreIntersectionSameColor

    def findElementWithCoordinate(self, row, colom, listOfPawn: List[PawnElement]):
        n = len(listOfPawn)
        for i in range(0, n):
            if listOfPawn[i].isTheSameCoordinate(row, colom):
                return i
        return self.NOT_FOUND
