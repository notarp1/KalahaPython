class node:

    boardstate = []
    parent = None
    children = []
    path = []
    points = []

    def __init__(self, boardState, parent, path):
        # Andre Node
        self.boardstate = boardState
        self.parent = parent
        self.children = []
        self.path = path

    def player_points(self, player):
        if not player:
            return self.boardstate[0]
        return self.boardstate[7]

    def appendChild(self, child):
        self.children.append(child)

    def setChildren(self, children):
        self.children = children

    def get_boardstate(self):
        return self.boardstate

    def get_childen(self):
        return self.children

    def get_parent(self):
        return self.parent

    def __str__(self, level=0):
        if level % 2 == 0:
            noob = 1
            player = "p2:"
        else:
            noob = 0
            player = "p1:"
        number = self.player_points(noob)
        ret = "\t"*level+ player +repr(number) + " " + repr(self.path) + "\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret
