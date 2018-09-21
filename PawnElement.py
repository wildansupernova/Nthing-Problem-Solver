import random

class PawnElement:

    def __init__(self, pawnElement, pawnColor):
        self.pawnElement = pawnElement
        self.pawnColor = pawnColor
        self.row = -1
        self.column = -1

    def randomizeRowColumn(self):
        self.row = random.randint(1,8)
        self.column = random.randint(1,8)

    # Check if this pawn is on the same place with element
    def isInTheSamePlace(self, element):
        """
        element: PawnElement
        """
        return element.row == self.row and element.column == self.column

    def isTheSameCoordinate(self, row, column):
        return self.row == row and self.column == column
