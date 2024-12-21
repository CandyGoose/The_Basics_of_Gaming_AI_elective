import numpy as np
import random

Chessboard_NONE = 0
Chessboard_MAX = 1
Chessboard_MIN = 2
Chessboard_FIVE_TYPE = 1
Chessboard_SFOUR_TYPE = 2
Chessboard_FOUR_TYPE = 3
Chessboard_STHREE_TYPE = 4
Chessboard_THREE_TYPE = 5
Chessboard_STWO_TYPE = 6
Chessboard_TWO_TYPE = 7

Chessboard_MAX_VALUE = 100000
Chessboard_MIN_VALUE = -100000
Chessboard_FOUR_W = 5000
Chessboard_THREE_W = 1000
Chessboard_TWO_W = 200
Chessboard_ONE_W = 10
Infinity = 99999999

class AI:
    def __init__(self, rowNum, colNum):
        self.data = np.zeros((rowNum, colNum), dtype=int)
        self.row = rowNum
        self.column = colNum
        self.wins = [[[] for _ in range(colNum)] for _ in range(rowNum)]
        self.count = 0

        for i in range(self.row):
            for j in range(self.column - 5 + 1):
                for k in range(5):
                    self.wins[i][j + k].append(self.count)
                self.count += 1

        for i in range(self.column):
            for j in range(self.row - 5 + 1):
                for k in range(5):
                    self.wins[j + k][i].append(self.count)
                self.count += 1

        for i in range(self.row - 5 + 1):
            for j in range(self.column - 5 + 1):
                for k in range(5):
                    self.wins[i + k][j + k].append(self.count)
                self.count += 1

        for i in range(self.row - 5 + 1):
            for j in range(self.column - 1, 3, -1):
                for k in range(5):
                    self.wins[i + k][j - k].append(self.count)
                self.count += 1

        self.maxWin = [{"max": 0, "min": 0} for _ in range(self.count)]
        self.minWin = [{"max": 0, "min": 0} for _ in range(self.count)]
        self.stack = []
        self.is_ended = False

    def put(self, row, column, type):
        if self.data[row][column] == Chessboard_NONE:
            self.data[row][column] = type
        self.stack.append({"row": row, "column": column, "type": type})

        for i in self.wins[row][column]:
            if type == Chessboard_MAX:
                self.maxWin[i]["max"] += 1
                self.minWin[i]["max"] += 1
            else:
                self.minWin[i]["min"] += 1
                self.maxWin[i]["min"] += 1

        if len(self.stack) == self.row * self.column:
            self.is_ended = True

    def rollback(self, n):
        for _ in range(n):
            step = self.stack.pop()
            row = step["row"]
            column = step["column"]
            type = step["type"]
            self.data[row][column] = Chessboard_NONE

            for j in self.wins[row][column]:
                if type == Chessboard_MAX:
                    self.maxWin[j]["max"] -= 1
                    self.minWin[j]["max"] -= 1
                else:
                    self.minWin[j]["min"] -= 1
                    self.maxWin[j]["min"] -= 1

        self.is_ended = False

    def isValid(self, row, column):
        return (
            0 <= row < self.row and
            0 <= column < self.column and
            self.data[row][column] == Chessboard_NONE
        )

    def getNearPoints(self, row, column):
        points = []
        for i in range(-2, 3):
            for delta in [i, -i]:
                r, c = row + delta, column + i
                if self.isValid(r, c):
                    points.append({"row": r, "column": c})

                r, c = row + i, column + delta
                if self.isValid(r, c):
                    points.append({"row": r, "column": c})

        return points

    def availableSteps(self):
        availableSteps = []
        centerRow = (self.row - 1) // 2
        centerColumn = (self.column - 1) // 2

        if not self.stack or (len(self.stack) == 1 and self.data[centerRow][centerColumn] == Chessboard_NONE):
            availableSteps.append({"row": centerRow, "column": centerColumn})
            return availableSteps

        if len(self.stack) == 1:
            nextRow = centerRow + (-1 if random.random() < 0.5 else 1)
            nextColumn = centerColumn + (-1 if random.random() < 0.5 else 1)
            availableSteps.append({"row": nextRow, "column": nextColumn})
            return availableSteps

        sign = np.zeros((self.row, self.column), dtype=int)
        for lastPoint in self.stack:
            nearPoints = self.getNearPoints(lastPoint["row"], lastPoint["column"])
            for point in nearPoints:
                r, c = point["row"], point["column"]
                if sign[r][c] == 0:
                    availableSteps.append({"row": r, "column": c})
                    sign[r][c] = 1

        return availableSteps

    def evaluate(self):
        maxW = minW = 0
        maxGroup = {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}
        minGroup = {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}

        for i in range(self.count):
            if self.maxWin[i]["max"] == 5 and not self.maxWin[i]["min"]:
                return Chessboard_MAX_VALUE
            if self.minWin[i]["min"] == 5 and not self.minWin[i]["max"]:
                return Chessboard_MIN_VALUE

            if self.maxWin[i]["max"] == 4 and not self.maxWin[i]["min"]:
                maxGroup["4"] += 1
            if self.minWin[i]["min"] == 4 and not self.minWin[i]["max"]:
                minGroup["4"] += 1

            if self.maxWin[i]["max"] == 3 and not self.maxWin[i]["min"]:
                maxGroup["3"] += 1
            if self.minWin[i]["min"] == 3 and not self.minWin[i]["max"]:
                minGroup["3"] += 1

            if self.maxWin[i]["max"] == 2 and not self.maxWin[i]["min"]:
                maxGroup["2"] += 1
            if self.minWin[i]["min"] == 2 and not self.minWin[i]["max"]:
                minGroup["2"] += 1

        maxW = maxGroup["4"] * Chessboard_FOUR_W + maxGroup["3"] * Chessboard_THREE_W + maxGroup["2"] * Chessboard_TWO_W
        minW = minGroup["4"] * Chessboard_FOUR_W + minGroup["3"] * Chessboard_THREE_W + minGroup["2"] * Chessboard_TWO_W
        return maxW - minW

    def isMaxWin(self):
        return self.evaluate() == Chessboard_MAX_VALUE

    def isMinWin(self):
        return self.evaluate() == Chessboard_MIN_VALUE

    def end(self):
        self.is_ended = True

    def max(self, depth, beta=Infinity):
        alpha = -Infinity
        row = column = -Infinity

        if depth == 0:
            return {"w": self.evaluate()}

        steps = self.availableSteps()
        for step in steps:
            self.put(step["row"], step["column"], Chessboard_MAX)

            if self.isMaxWin():
                alpha = Chessboard_MAX_VALUE
                row = step["row"]
                column = step["column"]
                self.rollback(1)
                break

            res = self.min(depth - 1, alpha)
            self.rollback(1)

            if res["w"] > alpha:
                alpha = res["w"]
                row = step["row"]
                column = step["column"]

            if alpha >= beta:
                break

        return {"w": alpha, "row": row, "column": column}

    def min(self, depth, alpha=-Infinity):
        beta = Infinity
        row = column = Infinity

        if depth == 0:
            return {"w": self.evaluate()}

        steps = self.availableSteps()
        for step in steps:
            self.put(step["row"], step["column"], Chessboard_MIN)

            if self.isMinWin():
                beta = Chessboard_MIN_VALUE
                row = step["row"]
                column = step["column"]
                self.rollback(1)
                break

            res = self.max(depth - 1, beta)
            self.rollback(1)

            if res["w"] < beta:
                beta = res["w"]
                row = step["row"]
                column = step["column"]

            if beta <= alpha:
                break

        return {"w": beta, "row": row, "column": column}
