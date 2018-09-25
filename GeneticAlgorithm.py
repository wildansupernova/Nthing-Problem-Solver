"""
    UNDER CONSTRUCTION
"""
from PawnElement import PawnElement
from PopulationMember import PopulationMember
from typing import List
from Board import Board
import copy
import random

class GeneticAlgorithm:

    def __init__(self, initBoard, N, probCross, probMuta, numOfGeneration):
        self.initBoard = initBoard
        self.N = N
        self.probCross = probCross
        self.probMuta = probMuta
        self.numOfGeneration = numOfGeneration
        self.population = self.initPopulation()

    def getProbCross(self):
        return self.probCross

    def setProbCross(self, probCross):
        self.probCross = probCross

    def getProbMuta(self):
        return self.probMuta
    
    def setProbMuta(self,probMuta):
        self.probMuta = probMuta
    
    def getNumOfGeneration(self):
        return self.numOfGeneration
    
    def setNumOfGeneration(self,numOfGeneration):
        self.numOfGeneration = numOfGeneration

    def getPopulation(self):
        return self.population
    
    def getN(self):
        return self.N

    def setN(self, N):
        self.N = N
    
    def getBoard(self):
        return self.initBoard
    
    def setBoard(self, board):
        self.initBoard = board

    def setPopulation(self, population):
        self.population = copy.deepcopy(population)

    def getPopulationLength(self):
        return len(self.getPopulation())
    # Make population
    def initPopulation(self) -> List[PopulationMember]: 
        randPopulations = []
        for i in range(0,self.getN()):
            self.getBoard().initRandomState()
            randPop = PopulationMember(self.getBoard())
            randPopulations.append(randPop)
            #self.printBoard(randPopulations[i].listOfPawn)
        return randPopulations
    
    # Survival functin
    def survivalFunction(self, populationMember: PopulationMember):
        n = self.getPopulationLength()
        totalFit = 0
        for x in self.getPopulation():
            totalFit += x.getFitness()
        return populationMember.getFitness()/totalFit

    # sort
    def sortPopulation(self):
        n = self.getPopulationLength()
        sortedPopulation = self.getPopulation()
        for i in range(0,n-1):
            max = i
            for j in range(i+1,n):
                #survivalFitnessI = self.survivalFunction(sortedPopulation[i], sortedPopulation)
                #survivalFitnessJ = self.survivalFunction(sortedPopulation[j], sortedPopulation)
                #if (survivalFitnessJ > survivalFitnessI):
                if (sortedPopulation[j].getFitness() > sortedPopulation[max].getFitness()):
                    max = j
            temp = sortedPopulation[i]
            sortedPopulation[i] = sortedPopulation[max]
            sortedPopulation[max] = temp
    
    # Check if pawn 
    def isPawnSamePlace(self, pawnA: PawnElement, parentBPawn: List[PawnElement]):
        for pawnB in parentBPawn:
            if pawnA.row == pawnB.row and pawnA.column == pawnB.column:
                return True
        return False
    
    def placePawnRandomly(self, pawn: PawnElement, listOfPawn: List[PawnElement]):
        replacedPawn = pawn
        while True:
            found = False
            randRow = random.randint(1, 8)
            randCol = random.randint(1, 8)
            for pawnCheck in listOfPawn:
                if pawnCheck.row != randRow and pawnCheck.column != randCol:
                    replacedPawn.row = randRow
                    replacedPawn.column = randCol
                    found = True
            if found:
                break

        return replacedPawn

    # One point crossover
    def onePointCrossOver(self, parentA: PopulationMember, parentB: PopulationMember):
        childA = []
        childB = []
        parentAPawn = parentA.getBoard().getListOfPawn()
        parentBPawn = parentB.getBoard().getListOfPawn()
        crossPoint = random.randint(1, len(parentAPawn)-1)

        for i in range(0, crossPoint):
            childA.append(parentAPawn[i])
            childB.append(parentBPawn[i])

        for i in range(crossPoint, len(parentAPawn)):
            if not self.isPawnSamePlace(parentBPawn[i], parentAPawn):
                childAPawn = copy.deepcopy(parentAPawn[i])
            else:
                childAPawn = self.placePawnRandomly(parentBPawn[i], childB)
            if not self.isPawnSamePlace(parentAPawn[i], parentBPawn):
                childBPawn = copy.deepcopy(parentAPawn[i])
            else:
                childBPawn = self.placePawnRandomly(parentAPawn[i], childA)
            childA.append(childAPawn)
            childB.append(childBPawn)

        boardA = Board(childA)
        boardB = Board(childB)
        return PopulationMember(boardA), PopulationMember(boardB)

    # Mutation of a population
    def mutation(self, populationMember: PopulationMember):
        maxColAttack = 0
        idxMax = 0
        listOfPawn = populationMember.getBoard().getListOfPawn()
        # search the max attacking pawn w/ the same color
        for i in range(0, len(listOfPawn)):
            _, sameColAttack = populationMember.getBoard().countPawnElementAttack(i)
            if maxColAttack < sameColAttack:
                idxMax = i
                maxColAttack = sameColAttack
        # Mutation in element idxMax: switch pawn
        mutatedPopulationMember = populationMember
        mutatedList = mutatedPopulationMember.getBoard().getListOfPawn()
        rowMax =mutatedList[idxMax].row
        colMax =mutatedList[idxMax].column
        idxSwitch = random.randint(0, len(populationMember.board.listOfPawn)-1)
        
        rowTemp =mutatedList[idxMax].row
        colTemp =mutatedList[idxMax].column
        mutatedList[idxMax].row =mutatedList[idxSwitch].row
        mutatedList[idxMax].column =mutatedList[idxSwitch].column
        mutatedList[idxSwitch].row = rowMax
        mutatedList[idxSwitch].row = colMax
        return mutatedPopulationMember

    # Generate child populations
    def evolvePopulations(self):
        childPopulations = []
        populations = self.getPopulation()
        parentA = populations[0]
        for i in range(1, self.getPopulationLength()):
            parentB = populations[i]
            # Cross Over
            if random.random() < self.getProbCross():
                childA, childB = self.onePointCrossOver(parentA, parentB)
            else:
                childA, childB = parentA, parentB
            # Mutation
            
            if random.random() < self.getProbMuta():
                childA = self.mutation(childA)
                childB = self.mutation(childB)
            
            childPopulations += [childA, childB]
        self.setPopulation(childPopulations)



    def algorithm(self):
        populations = self.getPopulation()

        self.sortPopulation()

        count = 0
        while True:
            print('aaaa')
            self.evolvePopulations()
            self.sortPopulation()
            cutChildPopulations = []
            self.setPopulation(cutChildPopulations)      
            for i in range(0,self.getN()):
                cutChildPopulations.append(populations[i])
            self.setPopulation(cutChildPopulations)
            count += 1
            if count == self.getNumOfGeneration() or self.getPopulationLength() <= 2:
                break
        lastListOfPawn = populations[0].getBoard()
        return lastListOfPawn