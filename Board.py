from PawnElement import PawnElement
from PopulationMember import PopulationMember
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
        self.listOfPawn = listOfPawn

    # Check if element on Idx is unique (the coordinate) in list or not
    def isIdxthElementUniqueInList(self, idx, listOfPawn):
        found = False
        for i in range(0,len(listOfPawn)):
            if i != idx:
                if listOfPawn[i].isInTheSamePlace(listOfPawn[idx]):
                    found = True
        return not(found)

    # Randomize the location of pawns, every pawn in unique coordinate
    def initRandomState(self, listOfPawn):
        n = len(listOfPawn)
        randomizedPawn = listOfPawn

        for i in range(0, n):
            randomizedPawn[i].randomizeRowColumn()
            while not(self.isIdxthElementUniqueInList(i, randomizedPawn)):
                randomizedPawn[i].randomizeRowColumn()
        

    # Make population
    def initPopulation(self, N, listOfPawn: List[PawnElement]) -> List[PopulationMember]: 
        randPopulations = []
        for i in range(0,N):
            newListOfPawn = copy.deepcopy(listOfPawn)
            self.initRandomState(newListOfPawn)
            randPop = PopulationMember(newListOfPawn, self)
            randPopulations.append(randPop)
            #self.printBoard(randPopulations[i].listOfPawn)

        return randPopulations
    
    # Survival functin
    def survivalFunction(self, populationMember: PopulationMember, population: List[PopulationMember]):
        n = len(population)
        totalFit = 0
        for x in population:
            totalFit += x.fitness
        return populationMember.fitness/totalFit

    # sort
    def sortPopulation(self, initPopulation: List[PopulationMember]):
        n = len(initPopulation)
        sortedPopulation = initPopulation
        for i in range(0,n-1):
            max = i
            for j in range(i+1,n):
                #survivalFitnessI = self.survivalFunction(sortedPopulation[i], sortedPopulation)
                #survivalFitnessJ = self.survivalFunction(sortedPopulation[j], sortedPopulation)
                #if (survivalFitnessJ > survivalFitnessI):
                if (sortedPopulation[j].fitness > sortedPopulation[max].fitness):
                    max = j
            temp = sortedPopulation[i]
            sortedPopulation[i] = sortedPopulation[max]
            sortedPopulation[max] = temp
    
    # One point crossover
    def onePointCrossOver(self, parentA: PopulationMember, parentB: PopulationMember):
        childA = []
        childB = []
        parentAPawn = parentA.listOfPawn
        parentBPawn = parentB.listOfPawn
        crossPoint = random.randint(1, len(parentAPawn)-1)

        for i in range(0, crossPoint):
            childA.append(parentAPawn[i])
            childB.append(parentBPawn[i])
        for i in range(crossPoint, len(parentAPawn)):
            childA.append(parentBPawn[i])
            childB.append(parentAPawn[i])

        return PopulationMember(childA, self), PopulationMember(childB, self)

    # Mutation of a population
    def mutation(self, population: PopulationMember):
        maxColAttack = 0
        idxMax = 0
        listOfPawn = population.listOfPawn
        # search the max attacking pawn w/ the same color
        for i in range(0, len(listOfPawn)):
            _, sameColAttack = self.countPawnElementAttack(i, listOfPawn)
            if maxColAttack < sameColAttack:
                idxMax = i
                maxColAttack = sameColAttack
        # Mutation in element idxMax: switch pawn
        mutatedPopulation = population
        rowMax = mutatedPopulation.listOfPawn[idxMax].row
        colMax = mutatedPopulation.listOfPawn[idxMax].column
        idxSwitch = self.findElementWithCoordinate(rowMax, colMax, listOfPawn)
        
        rowTemp = mutatedPopulation.listOfPawn[idxMax].row
        colTemp = mutatedPopulation.listOfPawn[idxMax].column
        mutatedPopulation.listOfPawn[idxMax].row = mutatedPopulation.listOfPawn[idxSwitch].row
        mutatedPopulation.listOfPawn[idxMax].column = mutatedPopulation.listOfPawn[idxSwitch].column
        mutatedPopulation.listOfPawn[idxSwitch].row = rowMax
        mutatedPopulation.listOfPawn[idxSwitch].row = colMax
        return mutatedPopulation

    # Generate child populations
    def evolvePopulations(self, probCross, probMuta, populations: List[PopulationMember]):
        childPopulations = []
        parentA = populations[0]
        for i in range(1, len(populations)):
            parentB = populations[i]
            # Cross Over
            if random.random() < probCross:
                childA, childB = self.onePointCrossOver(parentA, parentB)
            else:
                childA, childB = parentA, parentB
            # Mutation
            
            if random.random() < probMuta:
                childA = self.mutation(childA)
                childB = self.mutation(childB)
            
            childPopulations += [childA, childB]
        return childPopulations



    def geneticAlgorithm(self, listOfPawn: List[PawnElement], probCross, probMuta, numOfGeneration):
        N = 50
        populations = self.initPopulation(N, listOfPawn)

        self.sortPopulation(populations)

        count = 0
        while True:
            childPopulations = self.evolvePopulations(probCross, probMuta, populations)
            populations = childPopulations
            self.sortPopulation(populations)
            cutChildPopulations = []
            for i in range(0,N):
                cutChildPopulations.append(populations[i])
            
            populations = cutChildPopulations
            count += 1
            if count == numOfGeneration or len(populations) <= 2:
                break
        lastListOfPawn = childPopulations[0].listOfPawn
        return lastListOfPawn

    # Hill Climbing Algorithm
    def hillClimbing(self, listOfPawn: List[PawnElement]) -> List[PawnElement]:
        newStateListPawn = copy.deepcopy(listOfPawn)
        neighbor = self.chooseNextStatesFromListWithHighestScore(listOfPawn, self.compareListOfPawnWithColor)
        while self.compareListOfPawnWithColor(neighbor, newStateListPawn) > 0:
            newStateListPawn = neighbor
            neighbor = self.chooseNextStatesFromListWithHighestScore(newStateListPawn, self.compareListOfPawnWithColor)
        return newStateListPawn

    # Simulated Annealing Algorithm
    def simulatedAnnealing(self, listOfPawn: List[PawnElement], t, desRate, desStep) -> List[PawnElement]:
        stateListPawn = copy.deepcopy(listOfPawn)
        totalNeighbor = self.countNeighbor(stateListPawn)
        step = 0
        while True:
            if t <= 0:
                return stateListPawn
            idx = random.randint(1, totalNeighbor)
            newStateListPawn = self.selectNeighbor(stateListPawn, idx)
            delta = self.scoringListOfPawnWithColor(newStateListPawn) - self.scoringListOfPawnWithColor(stateListPawn)
            if delta > 0:
                stateListPawn = newStateListPawn
            else:
                probability = math.pow(math.e, delta/t)
                if probability > random.random():
                    stateListPawn = newStateListPawn

            step += 1
            t = self.descentTemperature(t, desRate, desStep, step)

    # Decrease temperature
    def descentTemperature(self, t, desRate, desStep, step):
        if step % desStep == 0:
            return t - desRate
        else:
            return t

    # Count the Neighbor
    def countNeighbor(self, listOfPawn: List[PawnElement]):
        n = len(listOfPawn)
        count = 0
        for i in range(0, n):
            for j in range(1,9):
                for k in range(1,9):
                    if self.isEmptyCell(j,k,listOfPawn):
                        count += 1

        return count

    # Select random neighbor at idx
    def selectNeighbor(self, listOfPawn: List[PawnElement], idx):
        n = len(listOfPawn)
        count = 0

        for i in range(0, n):
            for j in range(1,9):
                for k in range(1,9):
                    if self.isEmptyCell(j,k,listOfPawn):
                        count += 1

                        if count == idx:
                            tempState = copy.deepcopy(listOfPawn)
                            tempState[i].row = j
                            tempState[i].column = k

                            return tempState
    # Check if row, column empty
    def isEmptyCell(self, row, column, listOfPawn):
        found = False
        for element in listOfPawn:
            if element.isTheSameCoordinate(row, column):
                found = True
                break
        return not(found)
    
    # Check if coordinate in 8x8 chess
    def isValidCoordinate(self, row, column):
        return row >= 1 and row <= 8 and column >= 1 and column <= 8 

    # Choose from list of enumerated states that has highest score
    def chooseNextStatesFromListWithHighestScore(self, listOfPawn: List[PawnElement], compareFunction):
        n = len(listOfPawn)
        highestScoreState = None
        for i in range(0, n):
            for j in range(1,9):
                for k in range(1,9):
                    if self.isEmptyCell(j,k,listOfPawn):
                        tempState = copy.deepcopy(listOfPawn)
                        tempState[i].row = j
                        tempState[i].column = k

                        if highestScoreState == None:
                            highestScoreState = tempState
                        elif compareFunction(tempState, highestScoreState) > 0:
                            highestScoreState = tempState
        return highestScoreState

    # Choose next state from list randomly
    def chooseNextStatesFromListRandomly(self, listOfPawn: List[PawnElement], compareFunction):
        n = len(listOfPawn)
        chosenState = None
        while True:
            i = random.randint(0,n-1)
            j = random.randint(1,8)
            k = random.randint(1,8)
            if self.isEmptyCell(j,k,listOfPawn) and self.isValidCoordinate(j,k):
                tempState = copy.deepcopy(listOfPawn)
                tempState[i].row = j
                tempState[i].colom = k
                chosenState = tempState
                break
        return chosenState

    # Return 1 if A > B, 0 if A == B and -1 if A < B
    def compareListOfPawnWithColor(self, listOfPawnA: List[PawnElement], listOfPawnB: List[PawnElement]):
        scoreA = self.scoringListOfPawnWithColor(listOfPawnA)
        scoreB = self.scoringListOfPawnWithColor(listOfPawnB)
        if scoreA > scoreB:
            result = 1
        elif scoreA == scoreB:
            result = 0
        else:
            result = -1
        return result

    # Making list of scores from all pawns
    def scoringListOfPawnWithColor(self, listOfPawn: List[PawnElement]) -> int:
        n = len(listOfPawn)
        scoreIntersectingDifferentColor = 0
        scoreIntersectingSameColor = 0
        for i in range(0, n):
            tempScoreIntersectingDifferentColor = 0
            tempScoreIntersectingSameColor = 0
            
            tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor = self.countPawnElementAttack(i, listOfPawn)

            scoreIntersectingDifferentColor += tempScoreIntersectingDifferentColor
            scoreIntersectingSameColor += tempScoreIntersectingSameColor 

        return abs(scoreIntersectingDifferentColor - scoreIntersectingSameColor)

    # Making neighbours' score for knights
    def scoringKnightWithColor(self, listOfPawn: List[PawnElement], idx) -> (int, int):
        scoreIntersectingDifferentColor = 0
        scoreIntersectingSameColor = 0
        rowTransition = [-1, -1, 1, 1, -2, 2, -2, 2]
        columnTransition = [-2, 2, -2, 2, -1, -1, 1, 1]
        nPossibility = len(rowTransition)

        for i in range(0,nPossibility):
            rowMove = listOfPawn[idx].row + rowTransition[i]
            columnMove = listOfPawn[idx].column + columnTransition[i]

            if self.isValidCoordinate(rowMove, columnMove):
                searchResult = self.findElementWithCoordinate(rowMove, columnMove, listOfPawn)
                if searchResult != self.NOT_FOUND:
                    if listOfPawn[searchResult].pawnColor == listOfPawn[idx].pawnColor:
                        scoreIntersectingSameColor += 1
                    else:
                        scoreIntersectingDifferentColor += 1


        return scoreIntersectingDifferentColor, scoreIntersectingSameColor

    # Making neighbours' scores for bishop break if found
    def scoringBishopWithColor(self, listOfPawn: List[PawnElement], idx) -> (int, int):
        rowTransition = [-1, -1, 1, 1]
        columnTransition = [-1, 1, -1, 1]
        nDirection = len(rowTransition)
        scoreIntersectingDifferentColor = 0
        scoreIntersectingSameColor = 0

        for i in range(0, nDirection):
            rNow = listOfPawn[idx].row
            cNow = listOfPawn[idx].column
            while True:
                rNow = rNow + rowTransition[i]
                cNow = cNow + columnTransition[i]
                if self.isValidCoordinate(rNow,cNow):
                    searchResult = self.findElementWithCoordinate(rNow, cNow, listOfPawn)
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
    def scoringRookWithColor(self, listOfPawn: List[PawnElement], idx) -> (int, int):
        rowTransition = [-1, 0, 0, 1]
        columnTransition = [0, -1, 1, 0]
        nDirection = len(rowTransition)
        scoreIntersectingDifferentColor = 0
        scoreIntersectingSameColor = 0

        for i in range(0, nDirection):
            rNow = listOfPawn[idx].row
            cNow = listOfPawn[idx].column
            while True:
                rNow = rNow + rowTransition[i]
                cNow = cNow + columnTransition[i]
                if self.isValidCoordinate(rNow,cNow):
                    searchResult = self.findElementWithCoordinate(rNow, cNow, listOfPawn)
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

    # Count pawns attacking pawnIdx
    def countPawnElementAttack(self, pawnIdx, listOfPawn: List[PawnElement]) -> (int, int):
        if listOfPawn[pawnIdx].pawnElement == PawnType.KNIGHT :
            tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor = self.scoringKnightWithColor(listOfPawn, pawnIdx)
        elif listOfPawn[pawnIdx].pawnElement == PawnType.BISHOP:
            tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor = self.scoringBishopWithColor(listOfPawn, pawnIdx)
        elif listOfPawn[pawnIdx].pawnElement == PawnType.ROOK:
            tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor = self.scoringRookWithColor(listOfPawn, pawnIdx)
        elif listOfPawn[pawnIdx].pawnElement == PawnType.QUEEN:
            tempScoreIntersectingDifferentColor1, tempScoreIntersectingSameColor1 = self.scoringRookWithColor(listOfPawn, pawnIdx)
            tempScoreIntersectingDifferentColor2, tempScoreIntersectingSameColor2 = self.scoringBishopWithColor(listOfPawn, pawnIdx)
            
            tempScoreIntersectingDifferentColor = tempScoreIntersectingDifferentColor1 + tempScoreIntersectingDifferentColor2
            tempScoreIntersectingSameColor = tempScoreIntersectingSameColor1 + tempScoreIntersectingSameColor2
        return tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor

    # Calculate numbers of Pawn Attack
    def calculatePawnAttack(self, listOfPawn: List[PawnElement]) -> (int, int):
        n = len(listOfPawn)
        scoreIntersectingDifferentColor = 0
        scoreIntersectingSameColor = 0
        for i in range(0, n):
            tempScoreIntersectingDifferentColor = 0
            tempScoreIntersectingSameColor = 0
            tempScoreIntersectingDifferentColor, tempScoreIntersectingSameColor = self.countPawnElementAttack(i, listOfPawn)
            if tempScoreIntersectingDifferentColor != 0 :
                scoreIntersectingDifferentColor += 1
            if tempScoreIntersectingSameColor != 0 :
                # print(tempScoreIntersectingSameColor)
                # print(listOfPawn[i].__dict__)
                scoreIntersectingSameColor += 1
        return scoreIntersectingDifferentColor, scoreIntersectingSameColor

    # Find in listOfPawn in specific row and column
    def findElementWithCoordinate(self, row, column, listOfPawn: List[PawnElement]):
        n = len(listOfPawn)
        for i in range(0, n):
            if listOfPawn[i].isTheSameCoordinate(row, column):
                return i
        return self.NOT_FOUND
