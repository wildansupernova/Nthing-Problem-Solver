import random

class PawnElement:

    def __init__(self, pawnElement, pawnColor):
        self.pawnElement = pawnElement
        self.pawnColor = pawnColor
        self.row = -1
        self.column = -1

    def isPawnUnassigned(self):
        return self.row == -1 and self.column == -1

    def randomizeRowcolumn(self):
        self.row = random.randint(1,8)
        self.column = random.randint(1,8)

    def isInTheSamePlace(self, element):
        return element.row == self.row and element.column == self.column

    def isTheSameCoordinate(self, row, column):
        return self.row == row and self.column == column
