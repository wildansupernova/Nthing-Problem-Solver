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
        self.populations = self.initPopulation()
        self.allTimeBestPopulation = copy.deepcopy(self.populations[0])

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

    def getPopulations(self):
        return self.populations
    
    def getN(self):
        return self.N

    def setN(self, N):
        self.N = N
    
    def getInitBoard(self):
        return self.initBoard
    
    def setInitBoard(self, board):
        self.initBoard = board

    def setPopulation(self, population):
        self.populations = copy.deepcopy(population)
        #self.populations = population

    def getPopulationsLength(self):
        return len(self.getPopulations())

    def setAllTimeBestPopulation(self, population):
        self.allTimeBestPopulation = copy.deepcopy(population)

    def getAllTimeBestPopulation(self):
        return self.allTimeBestPopulation

    ### TOOLS FOR GENETIC ALGORITHM EXECUTION ###

    # Randomize initial populations
    def initPopulation(self) -> List[PopulationMember]: 
        randPopulations = []
        for i in range(0,self.getN()):
            self.getInitBoard().initRandomState()
            randPop = PopulationMember(self.getInitBoard())
            randPopulations.append(randPop)
        return randPopulations
    
    # Check and set all time best population
    def checkAllTimeBestPopulation(self, currBestPop: PopulationMember):
        if currBestPop.getFitness() >= self.allTimeBestPopulation.getFitness():
            self.setAllTimeBestPopulation(currBestPop)
    
    # Sort population based on fitness value
    def sortPopulations(self):
        n = self.getPopulationsLength()
        sortedPopulation = self.getPopulations()
        for i in range(0,n-1):
            max = i
            for j in range(i+1,n):
                if (sortedPopulation[j].getFitness() > sortedPopulation[max].getFitness()):
                    max = j
            temp = sortedPopulation[i]
            sortedPopulation[i] = sortedPopulation[max]
            sortedPopulation[max] = temp
    
    # Trim result of evolution populations into N pieces
    def trimPopulations(self):
        self.populations = self.populations[:self.getN()]
    
    # Return coordinates of pawn in a listOfPawn
    def getListOfPawnCoord(self, listOfPawn: List[PawnElement]):
        listOfPawnCoord = []
        for pawn in listOfPawn:
            listOfPawnCoord.append((pawn.row, pawn.column))
        return listOfPawnCoord
    
    # Place pawn randomly on empty coordinates
    def placePawnRandomly(self, pawnCheck: PawnElement, listOfPawn: List[PawnElement]) -> PawnElement:
        replacedPawn = copy.deepcopy(pawnCheck)
        listOfPawnCoord = self.getListOfPawnCoord(listOfPawn)

        while True:
            replacedPawn.randomizeRowColumn()
            randRow, randCol = replacedPawn.row, replacedPawn.column
            if (randRow, randCol) not in listOfPawnCoord:
                break
        return replacedPawn

    # Crossover effect: Check is pawn coordinate is empty in listOfPawn
    def isPawnSaveToPlace(self, pawn: PawnElement, listOfPawn: List[PawnElement]):
        listOfPawnCoord = self.getListOfPawnCoord(listOfPawn)
        return (pawn.row, pawn.column) not in listOfPawnCoord

    # One point crossover
    def onePointCrossOver(self, parentA: PopulationMember, parentB: PopulationMember):
        childA, childB = [], []
        parentAPawn = parentA.getBoard().getListOfPawn()
        parentBPawn = parentB.getBoard().getListOfPawn()
        crossPoint = random.randint(1, len(parentAPawn)-2)

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

        boardA = Board(childA)
        boardB = Board(childB)
        return PopulationMember(boardA), PopulationMember(boardB)

    # Mutation: get pawn index which attacking the same color the most
    def getMaxAttackingSameColorPawnIdx(self, population: PopulationMember, listOfPawn: List[PawnElement]) -> int:
        maxAttack = 0
        idx = 0
        for i in range(0, len(listOfPawn)):
            _, sameColorAttack = population.getBoard().countPawnElementAttack(i)
            if maxAttack < sameColorAttack:
                idx = i
                maxAttack = sameColorAttack
        return idx

    # Mutate a population with the most constraining pawn with the same color
    def mutation(self, populationMember: PopulationMember) -> PopulationMember:
        mutatedPopulation = copy.deepcopy(populationMember)
        mutatedBoard = copy.deepcopy(populationMember.getBoard())
        listOfPawn = mutatedPopulation.getBoard().getListOfPawn()
        
        idx = self.getMaxAttackingSameColorPawnIdx(populationMember, listOfPawn)

        mutatedPawn = self.placePawnRandomly(listOfPawn[idx], listOfPawn)    
        mutatedPopulation.getBoard().getListOfPawn()[idx].setPawnCoordinate(mutatedPawn)

        return mutatedPopulation

    # Generate N child populations. Evolve with CROSSOVER and MUTATION.
    def evolvePopulations(self):
        childPopulations = []
        populations = self.getPopulations()
        parentA = populations[0]
        for i in range(0, self.getPopulationsLength()//2):
        #for i in range(0, self.getN()):
            #parentA = populations[random.randint(0, self.getPopulationsLength()-1)]
            #parentB = populations[random.randint(0, self.getPopulationsLength()-1)]
        #while (i < self.getPopulationsLength()-1):
        
            #idx = random.sample(range(len(populations[0].board.listOfPawn)), 2)
            parentA = populations[i]
            parentB = populations[i + self.getPopulationsLength()//2]
            #parentB = populations[i]
            # Crossover
            #childA, childB = self.onePointCrossOver(parentA, parentB)
            #parentB = populations[i]
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

    ## MAIN ALGORITHM ##
    def algorithm(self):
        self.sortPopulations()
        print()

        for i in range(0, self.numOfGeneration):
            # Crossover and Mutation
            self.evolvePopulations()

            # Sort population based on fitness val
            self.sortPopulations()
            
            # Pick only N populations to evolve
            self.trimPopulations()
            #self.getPopulations()[0].board.printBoard()

            currBestPop = self.getPopulations()[0]
            
            # output
            print('== ', i+1, 'th gen')
            print('  Current Best Fitness Value: ', currBestPop.getFitness())
            self.checkAllTimeBestPopulation(currBestPop)

        self.printAllTimeBestPopulation()
            
        return currBestPop.getBoard()
    
    def printAllTimeBestPopulation(self):
        allTimeBest = self.allTimeBestPopulation
        print('===========')
        print('  ** All Time Best Population: ')
        attackDiff, attackSame = allTimeBest.getBoard().calculatePawnAttack()
        allTimeBest.board.printBoard()
        print('  ', attackSame, attackDiff)
        print('  Score: ', allTimeBest.getBoard().scoringListOfPawnWithColor())
        #print('  Fitness Value: ', allTimeBest.getFitness())
        print('===========')

