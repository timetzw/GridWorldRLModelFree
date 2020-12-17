import numpy as np
from gridworld import grid


class agent:
    def __init__(self, start, actions, world, discount, learningRate, epsilon,lamb):
        self.actions = actions
        self.world = world
        self.qtable = {}
        self.eligibility = {}
        for i in range(world.row):
            for j in range(world.col):
                for a in self.actions:
                    self.qtable[(i, j, a)] = 0
                    self.eligibility[(i, j, a)] = 0
        self.start = start
        self.state = start
        self.discount = discount
        self.learningRate = learningRate
        self.epsilon = epsilon
        self.lamb = lamb

    def chooseAction(self):
        if (np.random.uniform(0, 1) < self.epsilon):
            action = np.random.choice(self.actions)
        else:
            action = self.maxAction(self.state)
        return action

    def maxAction(self, state):
        action = np.random.choice(self.actions)
        maxq = self.qtable[state+(action,)]
        for a in self.actions:
            q = self.qtable[state+(a,)]
            if q > maxq:
                maxq = q
                action = a
        return action

    def takeAction(self, action):
        nextState = self.world.nextState(self.state, action)
        nextAction = self.maxAction(nextState)
        delta = (self.world.giveReward(nextState) + self.discount *self.qtable[nextState+(nextAction,)]) - self.qtable[self.state+(action,)]
        self.eligibility[self.state+(action,)]+=1
        for i in range(self.world.row):
            for j in range(self.world.col):
                for a in self.actions:
                    self.qtable[(i, j, a)] += self.learningRate * delta * self.eligibility[(i,j,a)]
                    self.eligibility[(i, j, a)] = self.eligibility[(i, j, a)] * self.discount * self.lamb
        self.state = nextState

    def updateEpsilon(self,episode):
        self.epsilon = 1/episode

    def play(self, episodes):
        currentEp = 1
        while currentEp <= episodes:
            self.updateEpsilon(currentEp)
            if self.world.reachedEnd(self.state):
                self.state = self.start
                print("Episode",currentEp,"Finished...",sep=" ")
                currentEp += 1
            else:
                action = self.chooseAction()
                self.takeAction(action)

    def getPolicySequence(self,start):
        state = start
        a = []
        while(not(self.world.reachedEnd(state))):
            action = self.maxAction(state)
            a.append(action)
            state = self.world.nextState(state, action)
        return a

    def printQtable(self):
        print(self.qtable)

    def printPolicy(self, start):
        print("Policy from start")
        state = start
        while(not(self.world.reachedEnd(state))):
            action = self.maxAction(state)
            print(action, end=" -> ")
            state = self.world.nextState(state, action)
        print("X")


if __name__ == "__main__":
    start = (0,0)
    rows = 10
    cols = 10
    obstacles = [(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(4,7),(6,2),(8,1),(4,2),(4,3),(7,5)]
    rewards = [(9,0,100)]
    ends = [(9,0),(9,9)]

    world = grid(rows, cols, obstacles, rewards,ends)
    
    actions = ["u", "d", "l", "r"]
    discount = 0.9
    learningRate = 0.1
    epsilon = 0.2
    numberOfEpisodes = 1000
    lamb = 0
    a = agent(start,actions, world, discount, learningRate,epsilon,lamb)
    
    a.play(numberOfEpisodes)
    #a.printQtable()
    a.printPolicy(start)
    world.printPolicySequence(start,world.end,a.getPolicySequence(start))
    
