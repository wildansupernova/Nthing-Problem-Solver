from Board import Board
from PawnElement import PawnElement
from typing import List
from HillClimbing import HillClimbing
from SimulatedAnnealing import SimulatedAnnealing
from GeneticAlgorithm import GeneticAlgorithm
import copy

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

def menu():
    print("Which algorithm do you prefer?")
    print("1. Hill Climbing")
    print("2. Simulated Annealing")
    print("3. Genetic Algorithm")

def inputMenu() -> int:
    x = int(input("Input choosen menu (1 or 2 or 3) : "))
    while (x < 1) or (x > 3):
        print("Please input integer 1 or 2 or 3 only.")
        x = input("Input choosen menu (1 or 2 or 3) : ")
    return x

def menuSetting() -> int:
    print("Do you want to edit algorithm configuration?")
    print("1. Yes, I want.")
    print("2. No, use default.")
    choice = int(input("Input your choice (1 or 2) : "))
    while (choice < 1) or (choice>2):
        print("Please input integer 1 or 2only.")
        choice = int(input("Input your choice (1 or 2) : "))
    return choice

def inputSettingSimulatedAnnealing() -> (int, int, int):
    x = int(input("Input Temperature : "))
    y = int(input("Input Descent Rate : "))
    z = int(input("Input Delay Step : "))
    return x,y,z

def inputSettingGeneticAlgorithm() -> (int,int,int,int):
    w = int(input("Input Number of Population Member : "))
    x = int(input("Input Probability of Crossover : "))
    y = int(input("Input Probability of Mutation : "))
    z = int(input("Input Number of Generations Generated : "))
    return w,x,y,z
    
'''
def printList(listOfPawn: List[PawnElement]):
    for element in listOfPawn:
        print(element.__dict__)
'''
def main():
    print("Please input your pawns")
    listOfPawn = []
    makingInput(listOfPawn)
    board = Board(listOfPawn)

    board.initRandomState()
    # board.printBoard()
    menu()
    a = inputMenu()
    if (a == 1):
        # print("Ini hill climbing")
        useHillClimbing = HillClimbing(board)
        newBoard = useHillClimbing.algorithm()
        newBoard.printBoard()
        differentColor, sameColor = newBoard.calculatePawnAttack()
        print(str(sameColor) + " " + str(differentColor))
        print(newBoard.scoringListOfPawnWithColor())
    elif (a == 2):
        # print("\n")
        # print("Ini Simulated Annealing")
        choice = menuSetting()
        if (choice == 1):
            t,desRate,desStep = inputSettingSimulatedAnnealing()
        else: # choice == 2
            t = 1000
            desRate = 10
            desStep = 10
        useSimulatedAnnealing = SimulatedAnnealing(t, desRate, desStep, board)
        newBoard = useSimulatedAnnealing.algorithm()
        newBoard.printBoard()
        differentColor, sameColor = newBoard.calculatePawnAttack()
        print(str(sameColor) + " " + str(differentColor))
        print(newBoard.scoringListOfPawnWithColor())
    else: # a == 3
    # print("\n")
    # print("Ini GA")
        choice = menuSetting()
        if (choice == 1):
            n,probCross,probMuta,generations = inputSettingGeneticAlgorithm()
        else: #choice == 2
            generations = 50
            probCross = 1
            probMuta = 1
            N = 50
        useGeneticAlgorithm = GeneticAlgorithm(board,N,probCross,probMuta,generations)
        geneticAlgorithmResult = useGeneticAlgorithm.algorithm()
        board = copy.deepcopy(geneticAlgorithmResult)
        board.printBoard()
        differentColor, sameColor = board.calculatePawnAttack()
        print(str(sameColor) + " " + str(differentColor))
        print(board.scoringListOfPawnWithColor())

if __name__== "__main__":
    main()