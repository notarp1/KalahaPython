import copy
from operator import is_not
from functools import partial
import json
import numpy as np


class Kalaha(object):

    def printBoard(self, board):
        print("-----------------")
        print("  [13]  [12]  [11]  [10]  [9]  [8]")
        print("  ", board[13], "   ", board[12], "   ", board[11], "   ", board[10], "   ", board[9], "   ", board[8])
        print(board[0], "                                 ", board[7])
        print("  ", board[1], "   ", board[2], "   ", board[3], "   ", board[4], "   ", board[5], "   ", board[6])
        print("  [1]   [2]   [3]   [4]   [5]  [6]")
        print("-----------------")

    def isWinner(self, board, kugler, winner, sum1, sum2):
        if board[0] + board[7] == kugler * 12:
            winner = True
            if sum1 < sum2:
                print("Tillykke spiller1")
            else:
                print("Tillykke spiller2")
            return winner
        return winner

    def evalmove(self, board, kugler, winner, limit, sum1, sum2):
        path = []
        path_complete = []
        path_list = []
        candidates = []
        candidates_player2 = []

        for i in range(1, 7):
            boardPass = list(board)
            path_send = list(path_complete)
            path_list.append(
                self.recursive(boardPass, kugler, i, limit, winner, path, path_send, sum1, sum2, 1, 7, i, 1))
        while None in path_list:
            path_list.remove(None)

        self.getCandidates(candidates, path_list)
        print("----------------------------------------------------------------")
        print("-----------------CANDIDATES PLAYER 1 ---------------------------")
        print("----------------------------------------------------------------")
        for p in candidates:
            print(p)

        path_list = []

        for p in candidates:
            path = []
            path_complete = []

            for i in range(8, 14):
                boardPass = list(p[4])
                path_send = list(path_complete)

                path_list.append(
                    self.recursive(boardPass, kugler, i, limit, winner, path, path_send, sum1, sum2, 8, 14, i, 0))
            while None in path_list:
                path_list.remove(None)

            sumcandidates = []
            self.getCandidates(sumcandidates, path_list)
            candidates_player2.append(sumcandidates)
            path_list = []
            print("----------------------------------------------------------------")
            print("-----------------CANDIDATES PLAYER 2 ---------------------------")
            print("---------------------------------------------------------------")
            for x in sumcandidates:
                print(x)

        path_list = []
        candidates_player1 = []
        for p in candidates_player2:
            for m in p:
                path = []
                path_complete = []

                for i in range(1, 7):
                    boardPass = list(m[4])
                    path_send = list(path_complete)

                    path_list.append(
                        self.recursive(boardPass, kugler, i, limit, winner, path, path_send, sum1, sum2, 1, 7, i, 1))
                while None in path_list:
                    path_list.remove(None)

                sum_candidates = []
                self.getCandidates(sum_candidates, path_list)
                candidates_player1.append(sum_candidates)

                path_list = []

        for p in candidates_player1:
            print("----------------------------------------------------------------")
            print("-----------------CANDIDATES PLAYER 1 ---------------------------")
            print("----------------------------------------------------------------")
            for m in p:
                print(m)

    def getCandidates(self, candidates, path_list):
        for p in path_list:
            length = len(p)

            if length < 2:
                candidates.append(p[0])
            else:
                j = -1
                prev = None
                for a in p:
                    if a[0] > j:
                        j = a[0]
                        if prev is not None:
                            candidates.remove(prev)
                            candidates.append(a)
                            prev = a
                        else:
                            candidates.append(a)
                            prev = a

    def recursive(self, boardPass, kugler, iteration, limit, winner, path, path_complete, sum1, sum2, x1, x2, current,
                  player1):
        if limit == 0:
            path = []

        if limit > 5:
            return path_complete

        path.append(iteration)
        switch = -1
        if player1 == 1:
            switch = 7
        else:
            switch = 0

        selection = iteration
        value = int(boardPass[selection])

        if boardPass[selection] == 0:
            return None

        boardPass[selection] = 0
        a = 0
        for i in range(1, (value + 1)):
            new_selection = selection + i

            if new_selection > 13:
                new_selection = new_selection - 14

            if player1:
                if new_selection == 0:
                    a = a + 1
            else:
                if new_selection == 7:
                    a = a + 1

            boardPass[new_selection + a] += 1

            if i == value:

                if self.isWinner(boardPass, kugler, winner, sum1, sum2) == 0:

                    if new_selection == switch:
                        limit = limit + 1
                        for j in range(x1, x2):
                            boardsend = list(boardPass)
                            pathsend = list(path)

                            self.recursive(boardsend, kugler, j, limit, winner, pathsend, path_complete, sum1, sum2, x1,
                                           x2, current, player1)

                        return path_complete
                    else:
                        if player1 == 1:
                            path_complete.append((boardPass[7], path, limit, 0, boardPass, current))
                        else:
                            path_complete.append((boardPass[0], path, limit, 0, boardPass, current))

                        while None in path_complete:
                            path_complete.remove(None)
                        return path_complete
                else:
                    if player1 == 1:
                        path_complete.append((boardPass[7], path, limit, 1, boardPass, current))
                    else:
                        path_complete.append((boardPass[0], path, limit, 1, boardPass, current))

                    return path_complete

    def playGame(self):
        print("Vælg antal kugler")
        kugler = int(input())
        sum1 = 0
        sum2 = 0
        board = [sum1, kugler, kugler, kugler, kugler, kugler, kugler, sum2, kugler, kugler, kugler, kugler, kugler,
                 kugler]

        winner = False
        player1 = True
        player2 = False

        while winner == 0:

            self.printBoard(board)
            if player1:
                self.evalmove(board, kugler, winner, 0, sum1, sum2)
            print("Vælg række")

            selection = int(input())
            value = int(board[selection])
            board[selection] = 0
            a = 0
            for i in range(1, (value + 1)):
                new_selection = selection + i

                if new_selection > 13:
                    new_selection = new_selection - 14

                if player1:
                    if new_selection == 0:
                        a = a + 1
                if player2:
                    if new_selection == 7:
                        a = a + 1

                board[new_selection + a] += 1

                if i == value:

                    if self.isWinner(board, kugler, winner, sum1, sum2) == 0:

                        if player1:
                            if new_selection == 7:
                                print("Ektra tur til spiller 1")

                            else:
                                print("Player 2 tur")
                                player1 = False
                                player2 = True
                        else:
                            if new_selection == 0:
                                print("Ektra tur til spiller 2 ")
                            else:
                                print("Player 1 tur")
                                player1 = True
                                player2 = False




game = Kalaha()
game.playGame()
