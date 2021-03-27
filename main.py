class Kalaha(object):
    playerIndex = 0
    player1Hole = 7
    player2Hole = 0
    anotherTurn = False
    turnCounter = 0

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
        path = []
        while not self.terminalTest(board):
            self.printBoard(board)
            if self.player() == 0:
                boardStatesDeep = [self.pathResults(self.getPlayerPoints(board), path, 4)]
                tempPath = []
                if path:
                    while isinstance(path[0], list):
                        path = path[0]
                    for moves in path:
                        tempPath.append(moves)
                while isinstance(boardStatesDeep[0], list):
                    boardStatesDeep = boardStatesDeep[0]
                print("AI moved with ", boardStatesDeep)
                for move in boardStatesDeep:
                    self.move(board, move)
                    tempPath.append(move)
                path = tempPath
                self.playerIndex = 0
                self.changePlayer()
                self.turnCounter += 1

            else:
                move = self.getInput()
                tempPath = []
                while isinstance(path[0], list):
                    path = path[0]
                for moves in path:
                    tempPath.append(moves)
                tempPath.append(move)
                print("You moved with ", move)
                path = tempPath
                extraTurn = self.move(board, move)
                self.turnCounter += 1
                if not extraTurn:
                    self.changePlayer()


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
                for p in self.anotherTurnCheck(boardPass, playerPoints, path):
                    pathsAndUtil.append(p)
            else:
                if self.player() == 0:
                    listToAdd = [path, self.utility(boardPass, playerPoints)]
                else:
                    listToAdd = [path, -self.utility(boardPass, playerPoints)]
                pathsAndUtil.append(listToAdd)
        return pathsAndUtil

    def pathResults(self, playerPoints, currentPath, depth):
        startBoard = self.createBoard(6)
        pathsAndUtil = list(currentPath)
        fullyNewPath = []
        currentBoard = []

        if not currentPath:
            currentBoard = list(startBoard)
            path = self.anotherTurnCheck(currentBoard, playerPoints, pathsAndUtil)
            pathsAndUtil.append(path)
        else:
            if isinstance(currentPath[0], list):
                while isinstance(currentPath[0][0][0], list):
                    currentPath = currentPath[0]
                for paths in currentPath:
                    originalPath = list(paths)
                    self.playerIndex = 0
                    currentBoard = list(startBoard)
                    while isinstance(originalPath[0], list):
                        originalPath = originalPath[0]
                    for i in range(0, len(originalPath)):
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
                pathsAndUtil = fullyNewPath

            else:
                self.playerIndex = 0
                currentBoard = list(startBoard)
                for i in range(0, len(currentPath)):
                    anotherTurn = self.move(currentBoard, currentPath[i])
                    if not anotherTurn:
                        self.changePlayer()
                self.playerIndex = 0
                newPaths = self.anotherTurnCheck(currentBoard, playerPoints, currentPath)
                for newpath in newPaths:
                    fullyNewPath.append(newpath)
                pathsAndUtil = fullyNewPath

        if depth-1 == 0:
            return self.minmax(pathsAndUtil)
        else:
            self.changePlayer()
            return self.pathResults(self.getPlayerPoints(currentBoard), pathsAndUtil, depth-1)

    def changePlayer(self):
        self.playerIndex = (self.playerIndex + 1) % 2

    def minmax(self, currentPath):
        path = []
        returnPath = []
        currentMax = -10000
        while isinstance(currentPath[0][0][0], list):
            currentPath = currentPath[0]

        for paths in currentPath:
            if paths[1] > currentMax:
                currentMax = paths[1]
                path = paths[0]
        tempBoard = self.createBoard(6)
        self.playerIndex = 0
        currentTurnCounter = 0
        for moves in path:
            if not currentTurnCounter == self.turnCounter:
                if not self.move(tempBoard, moves):
                    currentTurnCounter += 1
            else:
                if not self.move(tempBoard, moves):
                    returnPath.append(moves)
                    break
                else:
                    returnPath.append(moves)
        return returnPath


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
