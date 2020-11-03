"""#####################################################################
##                      RL Cat and Mouse - main body                  ##
########################################################################
#   
#   Name: Won Seok Yang
#   
##  Create a game of cat and mouse where each agent learns
#   from previous lives/cycles.
#   
#   Questions:
#   Continuous cheese vs single static run
#   -If the cheese spawns in the same spot, the mouse would have a better time of learning
#   as it can relate each state with a static direction (direction of the cheese)
#       How do we overlay all the information (cat, mouse, cheese) so that the mouse
#   can learn properly? if we have a qvalue for every cat position in relation to the
#   mouse and random cheese location, thats envArea^3 values?
#   things the mouse would have to keep track of, -cat pos -cheese pos -curr pos
#
########################################################################
##                          Resources                                 ##
########################################################################
#   Style guide:
#   https://www.python.org/dev/peps/pep-0008/#multiline-if-statements
########################################################################
##                          Notes                                     ##
########################################################################
#
########################################################################
"""

import time
from env import Maze
from brain import Brain
from consts import FILE_NAME
from consts import DRAW_MAZE
from consts import ALPHA, GAMMA, EPSILON

def main():
    alpha = ALPHA
    gamma = GAMMA
    epsilon = EPSILON

    env = Maze(FILE_NAME)
    myCat = Brain(env.actions, alpha, gamma, epsilon)

    





main()
print('after main')