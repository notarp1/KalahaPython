import copy
from operator import is_not
from functools import partial
import json

from node import node


class Kalaha(object):

    def printBoard(self, board):
        print("-----------------")
        print("  [13]  [12]  [11]   [10]   [9]   [8]")
        print("  ", board[13], "   ", board[12], "   ", board[11], "   ", board[10], "   ", board[9], "   ", board[8])
        print(board[0], "                                      ", board[7])
        print("  ", board[1], "   ", board[2], "   ", board[3], "   ", board[4], "   ", board[5], "   ", board[6])
        print("  [1]    [2]    [3]    [4]    [5]    [6]")
        print("-----------------")

    def isWinner(self, board, kugler, winner):
        if board[0] + board[7] == kugler * 12:
            winner = True
            if board[0] < board[7]:
                print("Tillykke spiller1")
            else:
                print("Tillykke spiller2")
            return winner
        return winner

    def evalmove(self, board, kugler, winner, limit, maxDepth):

        path = []
        path_complete = []
        path_list = []
        candidates = []

        for i in range(1, 7):
            boardPass = list(board)
            path_send = list(path_complete)
            path_list.append(
                self.recursive(boardPass, kugler, i, limit, winner, path, path_send, 1, 7, i, 1))
        while None in path_list:
            path_list.remove(None)

        self.getCandidates(candidates, path_list)

        first_node = node(board, None, None)

        for p in candidates:
            first_node.appendChild(node(p[1], first_node, p[3]))

        node_final = self.depth_search(candidates, first_node, maxDepth, 1, kugler, limit, winner)
        print("din mor")
        print(first_node.get_childen()[0])
        return node_final

    #####ØHHHHHHHHHHHHH?????? mangler minimax implementation
    def minimax(self, dept, currnode, maximize, pointIdex):
        values = []
        if (not currnode.get_childen()):
            return currnode.get_boardstate()[pointIdex]

        for n in currnode.get_childen():
            values.append(self.minimax(dept + 1, n, not maximize, pointIdex))
        if (dept == 0):
            return values.index(max(values)) +1
        if (maximize == True):
            return max(values)

        return min(values)

    def depth_search(self, candidates, parentNode, maxDepth, k, kugler, limit, winner):
        if k == maxDepth:
            return

        path_list = []

        start = 8
        end = 14
        printnummber = 2
        if k % 2 == 0:
            start = 1
            end = 7
            printnummber = 1
        k += 1

        for currentNode in parentNode.get_childen():
            path = []
            path_complete = []

            for i in range(start, end):
                board_pass = list(currentNode.boardstate)
                path_send = list(path_complete)
                path_list.append(
                    self.recursive(board_pass, kugler, i, limit, winner, path, path_send, start, end, i, 0))

            while None in path_list:
                path_list.remove(None)

            temp_candidates = []
            self.getCandidates(temp_candidates, path_list)
            candidates.append(temp_candidates)
            path_list = []

            for x in temp_candidates:
                currentNode.appendChild(node(x[1], currentNode, x[3]))

            self.depth_search(candidates, currentNode, maxDepth, k, kugler, limit, winner)
        return parentNode

    def print_candidates(self, printnummber):
        print("----------------------------------------------")
        print("-----------CANDIDATES PLAYER ", printnummber, "-----------------")
        print("----------------------------------------------")

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

    def recursive(self, boardPass, kugler, iteration, limit, winner, path, path_complete, x1, x2, current,
                  player1):

        if limit == 0:
            path = []
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
            eval = new_selection + a
            while eval > 13:
                if eval > 13:
                    eval = eval - 14
            boardPass[eval] += 1

            if i == value:

                if self.isWinner(boardPass, kugler, winner) == 0:

                    if new_selection == switch:
                        limit = limit + 1
                        for j in range(x1, x2):
                            boardsend = list(boardPass)
                            pathsend = list(path)

                            self.recursive(boardsend, kugler, j, 1, winner, pathsend, path_complete, x1,
                                           x2, current, player1)

                        return path_complete
                    else:
                        if player1 == 1:
                            path_complete.append((boardPass[7], boardPass, 0, path))
                        else:
                            path_complete.append((boardPass[0], boardPass, 0, path))

                        while None in path_complete:
                            path_complete.remove(None)
                        return path_complete
                else:
                    if player1 == 1:
                        path_complete.append((boardPass[7], boardPass, 1, path))
                    else:
                        path_complete.append((boardPass[0], boardPass, 1, path))

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

            selection = 0;
            if player1:
                node1 = self.evalmove(board, kugler, winner, 0, 3)
                index = self.minimax(0,node1, True,7)
                i = 1
                while(True):
                    if(board[i] == 0):
                        index+=1
                    if(i==index):
                        selection = i;
                        print(selection)
                        break
                    i+= 1
            if player2:
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

                    if self.isWinner(board, kugler, winner) == 0:

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
