from Board import Board
from typing import List
from PawnElement import PawnElement
import numpy as np
import copy
import random
import math

class SimulatedAnnealing:

    def __init__(self, t, desRate, desStep, board: Board):
        self.t = t
        self.desRate = desRate
        self.desStep = desStep
        self.board = board

    def getT(self):
        return self.t

    def getDesRate(self):
        return self.desRate

    def getDesStep(self):
        return self.desStep
    
    def getBoard(self):
        return self.board

    def setT(self, t):
        self.t = t

    def setDesRate(self, desRate):
        self.desRate = desRate
    
    def setDesStep(self, desStep):
        self.desStep = desStep
    
    def setBoard(self, board):
        self.board = copy.deepcopy(board)


    
    # Simulated Annealing Algorithm
    def algorithm(self) -> Board:
        stateListPawn = self.getBoard().getListOfPawn()
        totalNeighbor = self.getBoard().countNeighbor()
        
        step = 0
        while True:
            if self.getT() <= 0:
                break
            idx = random.randint(1, totalNeighbor)
            newStateListPawn = self.getBoard().selectNeighbor(idx)
            delta = newStateListPawn.scoringListOfPawnWithColor() - self.getBoard().scoringListOfPawnWithColor()
            if delta > 0:
                self.setBoard(newStateListPawn)
            else:
                probability = math.pow(math.e, delta/self.getT())
                if probability > random.random():
                    self.setBoard(newStateListPawn)

            step += 1
            self.setT(self.descentTemperature(step))
        return self.getBoard()

    # Decrease temperature
    def descentTemperature(self, step):
        if step % self.getDesStep() == 0:
            return self.getT() - self.getDesRate()
        else:
            return self.getT()
