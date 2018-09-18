import random

class PawnElement:

    def __init__(self, pawnElement, pawnColor):
        self.pawnElement = pawnElement
        self.pawnColor = pawnColor
        self.row = -1
        self.colom = -1

    def isPawnUnassigned(self):
        return self.row == -1 and self.colom == -1

    def randomizeRowColom(self):
        self.row = random.randint(1,9)
        self.colom = random.randint(1,9)

    def isInTheSamePlace(self, element: PawnElement):
        return element.row == self.row and element.colom == self.colom

    def isTheSameCoordinate(self, row, colom):
        return self.row == row and self.colom == colom
