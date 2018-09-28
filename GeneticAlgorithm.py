from PawnElement import PawnElement
from PopulationMember import PopulationMember
from typing import List
from Board import Board
import collections
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
        #self.population = copy.deepcopy(population)
        self.population = population

    def getPopulationLength(self):
        return len(self.getPopulation())

    # Make population
    def initPopulation(self) -> List[PopulationMember]: 
        randPopulations = []
        for i in range(0,self.getN()):
            self.getBoard().initRandomState()
            randPop = PopulationMember(self.getBoard())
            randPopulations.append(randPop)
        return randPopulations
    """
    # Survival functin
    def survivalFunction(self, populationMember: PopulationMember):
        n = self.getPopulationLength()
        totalFit = 0
        for x in self.getPopulation():
            totalFit += x.getFitness()
        return populationMember.getFitness()/totalFit
    """
    # sort
    def sortPopulation(self):
        n = self.getPopulationLength()
        sortedPopulation = self.getPopulation()
        for i in range(0,n-1):
            max = i
            for j in range(i+1,n):
                if (sortedPopulation[j].getFitness() > sortedPopulation[max].getFitness()):
                    max = j
            temp = sortedPopulation[i]
            sortedPopulation[i] = sortedPopulation[max]
            sortedPopulation[max] = temp
    
    def getListOfPawnCoord(self, listOfPawn: List[PawnElement]):
        listOfPawnCoord = []
        for pawn in listOfPawn:
            listOfPawnCoord.append((pawn.row, pawn.column))
        return listOfPawnCoord

    # Check is there any overlapping pawn
    def isPawnOverlapping(self, listOfPawn: List[PawnElement]):
        setOfPawn = set(listOfPawn)
        return len(listOfPawn) != len(setOfPawn)

    def isPawnSaveToPlace(self, pawn: PawnElement, listOfPawn: List[PawnElement]):
        listOfPawnCoord = self.getListOfPawnCoord(listOfPawn)
        return (pawn.row, pawn.column) not in listOfPawnCoord
    
    # Place pawn randomly on save coordinate
    def placePawnRandomly(self, pawnCheck: PawnElement, listOfPawn: List[PawnElement]) -> PawnElement:
        replacedPawn = copy.deepcopy(pawnCheck)
        listOfPawnCoord = self.getListOfPawnCoord(listOfPawn)

        while True:
            replacedPawn.randomizeRowColumn()
            randRow, randCol = replacedPawn.row, replacedPawn.column
            if (randRow, randCol) not in listOfPawnCoord:
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
            if self.isPawnSaveToPlace(parentBPawn[i], childA):
                childAPawn = parentBPawn[i]
            else:
                childAPawn = self.placePawnRandomly(parentBPawn[i], childA)
            if self.isPawnSaveToPlace(parentAPawn[i], childB):
                childBPawn = parentAPawn[i]
            else:
                childBPawn = self.placePawnRandomly(parentAPawn[i], childB)
            childA.append(childAPawn)
            childB.append(childBPawn)
        """
        # Avoid overlapping pawn position
        if self.isPawnOverlapping(childA):
            listOfPawnCoord = self.getListOfPawnCoord(childA)
            for 
        """
        boardA = Board(childA)
        boardB = Board(childB)
        return PopulationMember(boardA), PopulationMember(boardB)

    # Mutation of a population
    def mutation(self, populationMember: PopulationMember) -> PopulationMember:
        mutatedPopulation = copy.deepcopy(populationMember)
        mutatedBoard = copy.deepcopy(populationMember.getBoard())
        """
        maxColAttack = 0
        idxMax = 0
        # search the max attacking pawn w/ the same color
        for i in range(0, len(listOfPawn)):
            _, sameColAttack = populationMember.getBoard().countPawnElementAttack(i)
            if maxColAttack < sameColAttack:
                idxMax = i
                maxColAttack = sameColAttack
        """
        idx = random.randint(0, len(mutatedPopulation.board.listOfPawn)-1)
        listOfPawn = mutatedPopulation.getBoard().getListOfPawn()

        mutatedPawn = self.placePawnRandomly(listOfPawn[idx], listOfPawn)    
        mutatedPopulation.getBoard().getListOfPawn()[idx].setPawnCoordinate(mutatedPawn)

        return mutatedPopulation

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
        self.sortPopulation()
        print()

        #allTimeBestPop = self.getPopulation()[0]
        for i in range(0, self.numOfGeneration):
            self.evolvePopulations()
            self.sortPopulation()

            cutChildPopulations = []     
            for idx in range(0, self.getN()):
                cutChildPopulations.append(self.getPopulation()[idx])
            self.setPopulation(cutChildPopulations)

            #currBestPop = self.getPopulation()[0]
            #if currBestPop.getFitness() > allTimeBestPop.getFitness():
            #   allTimeBestPop = currBestPop
            
        bestBoardState = self.getPopulation()[0].getBoard()
        listOfPawnCoord = []
        for pawn in bestBoardState.listOfPawn:
            listOfPawnCoord.append((pawn.row, pawn.column))
        print(listOfPawnCoord)
        """
        For debugging purpose
        for pop in self.getPopulation():
            print((pop.getFitness(), pop.board.scoringListOfPawnWithColor()))
        #self.getPopulation()[0].getBoard().printBoard()
        #print(self.getPopulation()[0].getFitness())
        """
        allTimeBestPop = self.getPopulation()[0]
        return allTimeBestPop.getBoard()