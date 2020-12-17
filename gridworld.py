class grid:
    def __init__(self, row, col, obstacles, reward, end):
        self.row = row
        self.col = col
        self.obstacles = obstacles
        self.reward = {}
        for i in range(row):
            for j in range(col):
                self.reward[(i,j)] = 0
        
        for t in reward:
            (row,col,val) = t
            self.reward[(row,col)]=val
        self.end = end
        

    def giveReward(self, state):
        return self.reward[state]

    def reachedEnd(self, state):
        for s in self.end:
            if state==s:
                return True
        return False

    def nextState(self, state, action):
        (row, col) = state
        if action == "u":
            row += 1
            if row > self.row-1 or (row,col) in self.obstacles:
                return state
            else:
                return (row, col)
        if action == "d":
            row -= 1
            if row < 0 or (row,col) in self.obstacles:
                return state
            else:
                return (row, col)
        if action == "l":
            col -= 1
            if col < 0 or (row,col) in self.obstacles:
                return state
            else:
                return (row, col)
        if action == "r":
            col += 1
            if col > self.col-1 or (row,col) in self.obstacles:
                return state
            else:
                return (row, col)
