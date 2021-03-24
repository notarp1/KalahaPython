class node:

    boardState = []
    children = []

    def __init__(self, boardState, parent):
        # Andre Node
        self.boardState = boardState
        self.parent = parent
        self.children = []

    def player_points(self, player):
        if player == 1:
            return self.boardState[0]
        return self.boardState[7]

    def appendChild(self, child):
        self.children.append(child)

    def setChildren(self, children):
        self.children = children

    def get_boardstate(self):
        return self.boardState

    def get_childen(self):
        return self.children

    def get_parent(self):
        return self.parent
