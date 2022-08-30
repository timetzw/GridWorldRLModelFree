import numpy as np
import sys
import argparse
from gridworld import grid

class agent:
    def __init__(self, start, actions, world, discount, learningRate, epsilon,lamb,adaptiveEpsilon):
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
        self.adaptiveEpsilon = adaptiveEpsilon

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
            print('currEpisode:', currentEp)
            if self.adaptiveEpsilon:
                self.updateEpsilon(currentEp)

            if self.world.reachedEnd(self.state):
                self.state = self.start
                print("Episode",currentEp,"Finished...",sep=" ")
                currentEp += 1
            else:
                action = self.chooseAction()
                print('take', action, ' in', self.state)
                self.takeAction(action)
                print('new state=', self.state)

    def getPolicySequence(self,start):
        state = start
        a = []
        print('getPOlicySeq')
        while(not(self.world.reachedEnd(state))):
            print(state)
            action = self.maxAction(state)
            print(action)
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

def convertPosition(s):
    try:
        row,col = map(int,s.split(","))
        return (row,col)
    except:
        raise argparse.ArgumentTypeError("arguments must be row,col")

def convertReward(s):
    try:
        row,col,value = map(int,s.split(","))
        return (row,col,value)
    except:
        raise argparse.ArgumentTypeError("arguments must be row,col,value")

if __name__ == "__main__":
    #Arguments for world and agent
    parser = argparse.ArgumentParser(description='Train an agent to find the optimal path in a grid world.')
    parser.add_argument('--rows',"-y",default=5,type=int,help='Number of rows in the grid world e.g 10')
    # parser.add_argument('--cols',"-x",default=10,type=int,help='Number of coloumns in the grid world e.g 10')
    parser.add_argument('--start',"-s",default=(0,0),type=convertPosition,help='Starting position of the agent in the grid world. Given as a tuple in the form of row,coloumn e.g -s 0,0')
    parser.add_argument('--obstacles',"-o",default=[],nargs='+',type=convertPosition,help='Obstacles present in the grid world. Given as a list of tuples in the form row,coloumn row,coloumn e.g -o 3,2 5,6')
    # parser.add_argument('--rewards',"-r",default=[(9,9,100)],nargs='+',type=convertReward,help='Rewards given for transition to a state. Given as a list of tuples in the form row,coloumn,reward row,coloumn,reward e.g -r 9,9,100 0,9,-100')
    # parser.add_argument('--ends',"-e",default=[(9,9)],nargs='+',type=convertPosition,help='Terminal states for the grid world i.e the win or loss states. Given as a list of tuples in the form row,coloumn row,coloumn e.g -e 9,9 0,9')
    parser.add_argument('--actions',"-a",default=["u", "d", "l", "r"],nargs='+',type=str,help='List of actions that the agent can perform. Given as a list of chars where "u" = Up, "r" = Right, "l" = Left, "d" = Down. Only actions from these 4 can be selected. e.g -a u d l r')
    parser.add_argument('--discount',"-d",default=0.9,type=float,help='Discount factor for future rewards i.e how much weight does the agent take the future into account. e.g -d 0.9')
    parser.add_argument('--learningRate',"-l",default=0.1,type=float,help='Learning rate for the agent i.e how much does the agent take the learning error into account each step. e.g -l 0.1')
    parser.add_argument('--epsilon',"-ep",default=0.2,type=float,help='Epsilon value for the epsilon greedy policy i.e how much does the agent try to explore. e.g -ep 0.2')
    parser.add_argument('--adaptiveEpsilon',"-ae",default=False,action='store_true',help='Choice to use Adaptive epsilon value i.e the exploratory nature of the agent decreases as the number of episodes played increases')
    parser.add_argument('--numberOfEpisodes',"-n",default=100,type=int,help='Number of episodes that the agent will play to learn optimal policy e.g 100')
    parser.add_argument('--lambdaValue',"-la",default=0.5,type=float,help='The lambda value for the agent i.e the weighting given to future steps in the sampled run e.g 0.5')
    parser.add_argument('--printPolicy',"-pp",default=False,action='store_true',help='Choice of whether or not to print policy after simulated e.g True')
    parser.add_argument('--printVisualisation',"-pe",default=True,action='store_true',help='Choice of whether or not to print the visualisation of the policy in the world e.g True')
    
    args = parser.parse_args()
    
    start = args.start
    rows = args.rows
    cols = rows#args.cols
    obstacles = args.obstacles
    rewards = [(rows-1,rows-1,100)]#args.rewards
    ends = [(rows-1,rows-1)]
    # ends = args.ends

    world = grid(rows, cols, obstacles, rewards,ends)
    
    actions = args.actions
    discount = args.discount
    learningRate = args.learningRate
    epsilon = args.epsilon
    numberOfEpisodes = args.numberOfEpisodes
    lamb = args.lambdaValue
    adaptiveEpsilon = args.adaptiveEpsilon

    a = agent(start,actions, world, discount, learningRate,epsilon,lamb,adaptiveEpsilon)
    
    a.play(numberOfEpisodes)
    # print('done playin')
    if args.printPolicy:
        # print('printPolicy')
        a.printPolicy(start)
    if args.printVisualisation:
        # print('printViz')
        world.printPolicySequence(start,world.end,a.getPolicySequence(start))
    
    
