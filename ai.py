import math

from main import Kalaha
from node import node


class ai:
    nodeArray = []
    def __init__(self):
        x = 1

    def minimax(self, boardState, curDepth, nodeIndex, maxTurn, scores, targetDepth):

        # base case : targetDepth reached
        if (curDepth == targetDepth):
            return scores[nodeIndex]

        if (maxTurn):
            return max(self.minimax(curDepth + 1, nodeIndex * 2,
                                    False, scores, targetDepth),
                       self.minimax(curDepth + 1, nodeIndex * 2 + 1,
                                    False, scores, targetDepth))

        else:
            return min(self.minimax(curDepth + 1, nodeIndex * 2,
                               True, scores, targetDepth),
                       self.minimax(curDepth + 1, nodeIndex * 2 + 1,
                               True, scores, targetDepth))

    def expand_state(boardState):
        childs =[]


        return childs

    def expand_move(boardstate, move, player):
        optimalPoints = []
        extraTurn = False
        start, end = 1, 6
        if(player):
            start, end = 8, 13





        return optimalPoints

    def move(boardstate, move, player):
        # Move
        selection = move
        value = int(boardstate[selection])
        boardstate[selection] = 0
        a = 0
        for i in range(1, (value + 1)):
            new_selection = selection + i

            if new_selection > 13:
                new_selection = new_selection - 14

            if not player:
                if new_selection == 0:
                    a = a + 1
            if player:
                if new_selection == 7:
                    a = a + 1

            boardstate[new_selection + a] += 1

        return boardstate



    # Driver code
    scores = [3, 5, 2, 9, 12, 5, 23, 23]

    treeDepth = math.log(len(scores), 2)

    print("The optimal value is : ", end="")
    print(minimax(0, 0, True, scores, treeDepth))

    # This code is contributed
    # by rootshadow
