import copy
from operator import is_not
from functools import partial
import json
import numpy as np


class Kalaha(object):
    playerIndex = 0
    player1Hole = 7
    player2Hole = 0
    anotherTurn = False

    def printBoard(self, board):
        print("-----------------")
        print("  [13]  [12]  [11]  [10]  [9]  [8]")
        print("  ", board[13], "   ", board[12], "   ", board[11], "   ", board[10], "   ", board[9], "   ", board[8])
        print(board[0], "                                 ", board[7])
        print("  ", board[1], "   ", board[2], "   ", board[3], "   ", board[4], "   ", board[5], "   ", board[6])
        print("  [1]   [2]   [3]   [4]   [5]  [6]")
        print("-----------------")


    def createBoard(self, numberOfBalls):
        boardCreated = [0, numberOfBalls, numberOfBalls, numberOfBalls, numberOfBalls, numberOfBalls, numberOfBalls, 0, numberOfBalls, numberOfBalls, numberOfBalls, numberOfBalls, numberOfBalls, numberOfBalls]
        return boardCreated


    def getInput(self):
        print("Vælg hul")
        kugler = int(input())
        return kugler


    def playGame(self):
        board = self.createBoard(6)
        while not self.terminalTest(board):
            self.printBoard(board)
            #move = self.getInput()
            path = []
            #playerPoints = self.getPlayerPoints(board)
            #boardStates = [self.results(board, self.action(board))]
            boardStatesDeep = [self.pathResults(board, self.getPlayerPoints(board), path, 2)]
            path.append(boardStatesDeep)
            #print("players move:", boardStatesDeep[0][0]+1, " otherplayers move:", boardStatesDeep[0][1]+1)
            #self.anotherTurn = self.move(board, boardStatesDeep[0][0]+1)
            #if not self.anotherTurn:
            #    self.playerIndex = (self.playerIndex + 1) % 2


    def getPlayerPoints(self, board):
        if self.player() == 0:
            playerHole = self.player1Hole
        else:
            playerHole = self.player2Hole
        return board[playerHole]


    def player(self):
        return self.playerIndex


    def action(self, board):
        actions = []
        if self.player() == 0:
            start = 1
            end = 7
        else:
            start = 8
            end = 14
        for i in range(start, end):
            if board[i] != 0:
                actions.append(i)
        return actions


    def anotherTurnCheck(self, board, playerPoints, currentPath):
        pathsAndUtil = []
        for index, a in enumerate(self.action(board)):
            path = list(currentPath)
            boardPass = list(board)
            anotherTurn = self.move(boardPass, a)
            path.append(a)
            if anotherTurn:
                pathsAndUtil.append(self.anotherTurnCheck(boardPass, playerPoints, path))
            else:
                if self.player() == 0:
                    listToAdd = [path, self.utility(boardPass, playerPoints)]
                else:
                    listToAdd = [path, -self.utility(boardPass, playerPoints)]
                pathsAndUtil.append(listToAdd)
        return pathsAndUtil

    def pathResults(self, startBoard, playerPoints, currentPath, depth):
        pathsAndUtil = list(currentPath)
        fullyNewPath = []
        currentPlayer = self.player()
        originalPath = []

        if not currentPath:
            replacementBoard = list(startBoard)
            path = self.anotherTurnCheck(replacementBoard, playerPoints, pathsAndUtil)
            pathsAndUtil.append(path)
        else:
            for paths in currentPath[0]:
                originalPath = list(paths)
                self.playerIndex = 0
                currentBoard = list(startBoard)
                while isinstance(originalPath[0], list):
                    originalPath = originalPath[0]
                for i in range(0, len(originalPath)):
                    print(originalPath)
                    anotherTurn = self.move(currentBoard, originalPath[i])
                    if not anotherTurn:
                        self.changePlayer()

                newPaths = self.anotherTurnCheck(currentBoard, playerPoints, originalPath)
                originalPath = list(paths)
                while isinstance(originalPath[0][0], list):
                    originalPath = originalPath[0]
                for newpath in newPaths:
                    newpath[1] += originalPath[1]
                    fullyNewPath.append(newpath)

        if depth-1 == 0:
            return pathsAndUtil
        else:
            self.changePlayer()
            return self.pathResults(startBoard, playerPoints, pathsAndUtil, depth-1)

    def changePlayer(self):
        self.playerIndex = (self.playerIndex + 1) % 2

    def minmax(self, results):
        path = []
        currentMin = 10000
        for index, states in enumerate(results):
            for state in range(14, len(states[0])):
                if currentMin > (states[0][state][1] - states[1]):
                    currentMin = (states[0][state][1] - states[1])
                    if self.playerIndex == 0:
                        path = [index, state - 14+7]
                    else:
                        path = [index+7, state-14]
        return path


    def move(self, board, action):
        if self.player() == 0:
            otherHole = self.player2Hole
            playerHole = self.player1Hole
        else:
            otherHole = self.player1Hole
            playerHole = self.player2Hole
        numberOfBalls = board[action]
        board[action] = 0
        otherGoalCount = 0
        for i in range(0, numberOfBalls):
            if (action+i+1+otherGoalCount) % 14 != otherHole:
                board[(action+i+1+otherGoalCount) % 14] += 1
            else:
                otherGoalCount += 1
                board[(action+i+1+otherGoalCount) % 14] += 1
            if i+1 == numberOfBalls:
                if (action+i+1) % 14 == playerHole:
                    return True
        return False


    def terminalTest(self, board):
        for place in board:
            if place != self.player1Hole and place != self.player2Hole:
                if place != 0:
                    return 0
        return 1


    def utility(self, state, startPoints):
        if self.player() == 0:
            hole = self.player1Hole
        else:
            hole = self.player2Hole
        return state[hole]-startPoints


if __name__ == "__main__":
    game = Kalaha()
    game.playGame()
