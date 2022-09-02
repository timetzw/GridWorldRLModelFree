# Experiment Goal(s)
# 1) Assess how different values of lambda impact agent performance in both an obstacle-free and obstacle-present world

# Helpful tips on running a module's main function: https://stackoverflow.com/questions/14500183/in-python-can-i-call-the-main-of-an-imported-module

import agent
import numpy as np

# List params to loop over
lamdas = np.linspace(0, 1, 5)

# Test out different params
for lamda in lamdas:
    print('lambda =', round(lamda,2))
    # TODO: Review how to pass boolean to argparser. Not working as I expected it. Used an int argument to control debugging, instead.
    performance = agent.main(['-n','10','--rows', '10', '-l', '0.5', '-la', str(lamda), '-db', '0', '-o', '8,8'])

    # TODO: implement performance metrics
    # 1) Number of steps taken in end-resulting policy
    # 2) Was an end state ever reached? Seem to be running into this issue... might be a bug.

