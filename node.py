class node:

    def __init__(self, boardState, parent):
        # Andre Node
        self._boardState = boardState
        self._parent = parent
        self._children = [node]

    def player_points(self, player):
        if player == 1:
            return self._boardState[0]
        return self._boardState[7]

    def appendChild(self, child):
        self._children.append(child)

    def setChildren(self, children):
        self._children = children

    def get_boardstate(self):
        return self._boardState

    def get_childen(self):
        return self._children

    def get_parent(self):
        return self._parent
