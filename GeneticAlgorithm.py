"""
    UNDER CONSTRUCTION
"""
from PawnElement import PawnElement
from PopulationMember import PopulationMember
from typing import List
import Board

class GeneticAlgorithm:

    def __init__(self, N: int, listOfPawn: List[PawnElement]):
        self.listOfPawn: listOfPawn
        self.populations: self.initPopulations(N)
    
    # Generate random populations
    def initPopulation(self, N) -> List[PopulationMember]: 
        randPopulations = []
        for i in range(0, N):
            board = Board(listOfPawn)
            board.initRandomState(listOfPawn)
            randPop = PopulationMember(listOfPawn, board)
            randPopulations.append(randPop)
            #self.printBoard(randPopulations[0].listOfPawn)
        self.printBoard(randPopulations[1].listOfPawn)
        self.printBoard(randPopulations[0].listOfPawn)
        """
        for i in range(0,N):
            self.printBoard(populations[i].listOfPawn)
            """
        return randPopulations
    
    # Survival functin
    def survivalFunction(self, populationMember: PopulationMember, population: List[PopulationMember]):
        n = len(population)
        totalFit = 0
        for x in population:
            totalFit += x.fitness
        return populationMember.fitness/totalFit

    # sort populations by survival fitness
    def sortPopulation(self, initPopulation: List[PopulationMember]):
        n = len(initPopulation)
        sortedPopulation = initPopulation
        for i in range(0,n-1):
            max = i
            for j in range(i+1,n):
                survivalFitnessI = self.survivalFunction(sortedPopulation[i], sortedPopulation)
                survivalFitnessJ = self.survivalFunction(sortedPopulation[j], sortedPopulation)
                if (survivalFitnessJ > survivalFitnessI):
                    max = j
            temp = sortedPopulation[i]
            sortedPopulation[i] = sortedPopulation[j]
            sortedPopulation[j] = temp
    
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
        for i in range(1, 10):
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
        populations = self.initPopulation(50, listOfPawn)

        #for i in range(0,5):
        #    self.printBoard(populations[i].listOfPawn)

        self.sortPopulation(populations)

        count = 0
        while True:
            childPopulations = self.evolvePopulations(probCross, probMuta, populations)
            populations = childPopulations
            self.sortPopulation(populations)
            count += 1
            if count == numOfGeneration or len(populations) <= 2:
                break
        lastListOfPawn = childPopulations[0].listOfPawn
        return lastListOfPawn