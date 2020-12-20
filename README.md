# Model Free Reinforcement Learning for Agent in Grid World
Simple python implementation of TD(λ) Q learning for pathfinding in a grid world of any size with or without obstacles.

Uses ε-greedy policy for behaviour and tries to learn about the optimal greedy policy.

## How to use
Run the agent.py script.

### Arguments:
--rows : number of rows in grid world 

--cols : number of coloumns in grid world

--start : the starting position of the agent in grid world : e.g 0,0

--obstacles : the obstacles in grid world : e.g 3,0 2,4 5,4

--rewards : the rewards for transitioning into a state : e.g 9,9,100 0,9,-100

--ends : the terminal states of grid world : e.g 9,9 0,9

--actions : the actions the agent can take. From the list of chars where "u" = Up, "r" = Right, "l" = Left, "d" = Down : e.g l r

--discount : discount factor for future rewards i.e how much weight does the agent take the future into account.

--learningRate : Learning rate for the agent i.e how much does the agent take the learning error into account each step.

--epsilon : Epsilon value for the epsilon greedy policy i.e how much does the agent try to explore.

--adaptiveEpsilon : Choice to use Adaptive epsilon value i.e the exploratory nature of the agent decreases as the number of episodes played increases.

--numberOfEpisodes : Number of episodes that the agent will play to learn optimal policy.

--lambdaValue : The lambda value for the agent i.e the weighting given to future steps in the sampled run i.e λ in TD(λ)

--printPolicy : Choice of whether or not to print policy after simulated

--printVisualisation : Choice of whether or not to print the visualisation of the policy in the world
