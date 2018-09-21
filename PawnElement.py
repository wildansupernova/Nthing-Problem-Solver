import random

class PawnElement:

    def __init__(self, pawnElement, pawnColor):
        self.pawnElement = pawnElement
        self.pawnColor = pawnColor
        self.row = -1
        self.colom = -1

    # Set row column = -1 jika unassigned
    def isPawnUnassigned(self):
        return self.row == -1 and self.colom == -1

    # Set row column randomly
    def randomizeRowColom(self):
        self.row = random.randint(1,8)
        self.colom = random.randint(1,8)

    # Check if this pawn is on the same place with element
    def isInTheSamePlace(self, element):
        return element.row == self.row and element.colom == self.colom

    # Check if this pawn is on a coordinate
    def isTheSameCoordinate(self, row, colom):
        return self.row == row and self.colom == colom
