class grid:
    def __init__(self, row, col, obstacles, reward, end):
        self.row = row
        self.col = col
        self.obstacles = obstacles
        self.reward = {}
        for i in range(row):
            for j in range(col):
                self.reward[(i,j)] = -1
        
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

    def printWorld(self,start,goal):
            print("╔",end="")
            for j in range(self.col-1):
                print("═══╦",sep="",end="")
           
            print("═══╗",end="")
            for i in range(self.row-1):
                print("\n║",end="")
                for j in range(self.col):
                    if (self.row - i-1,j) in self.obstacles:
                        print("║║║║",sep="",end="")
                    elif (self.row-i-1,j) == start:
                        print(" ☺ ║",sep="",end="")
                    elif (self.row-i-1,j) in goal:
                        print(" ¤ ║",sep="",end="")    
                    else:
                        print("   ║",sep="",end="")
                print("\n║",end="")
                for j in range(self.col):
                    print("═══║",sep="",end="")
            print("\n║",end="")
            for j in range(self.col):
                    if (0,j) in self.obstacles:
                            print("║║║║",sep="",end="")
                    elif (0,j) == start:
                        print(" ☺ ║",sep="",end="")
                    elif (0,j) in goal:
                        print(" ¤ ║",sep="",end="")    
                    else:
                        print("   ║",sep="",end="")
            print("\n╚",end="")
            for i in range(self.col-1):
                print("═══╩",end="")
            print("═══╝")

    def printPolicySequence(self,start,goal,actionSequence):
        self.printWorld(start,goal)
        state = start
        for a in actionSequence:
            state=self.nextState(state,a)
            self.printWorld(state,goal)

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

        

             