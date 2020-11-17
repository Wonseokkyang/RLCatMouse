"""#####################################################################
##                RL Cat and Mouse - global consts                    ##
########################################################################
#   
#   Name: Won Seok Yang
#   
##  All global 'constant' variables for easy manipulation
#  
########################################################################
##                          Resources                                 ##
########################################################################
#   Style guide:
#   https://www.python.org/dev/peps/pep-0008/#multiline-if-statements
#
########################################################################
##                          Notes                                     ##
########################################################################
#
########################################################################
"""

# Name of txt file to create the learning environment
# Located in ./mazetxt
FILE_NAME = 'blank3x3'

# Draw the graphical window to show the agent(s) in action.
DRAW_MAZE = True
# Print agent's moves in terminal
ANNOUNCE_AGENT_MOVES = True
# Number of seconds to pause after drawing (refresh rate)
SPEED = 0.5

# Pixel size of individual squares in the environment
UNIT = 30

# The number of times 
CYCLES = 1

# Reward values:
OUT_OF_FRAME = -100.0   #out of bounds penalty
WALL = -10.0            #hitting a wall penalty
MOVE = -0.1             #moving into a square penalty
TARGET = 100.0          #finding the end of the maze reward
CAUGHT = TARGET         #reward for mouse reaching cheese and/or cat reaching mouse

# Math values
ALPHA = 0.9             #how heavily the learning algorithm gets changed toward a positive reward (learning rate)
GAMMA = 0.9             #the discount factor of future rewards (0 nearsighted vs 1 farsighted)
EPSILON = 0.9           #the weight of the algo's 'greediness', less greedy = explore, more greedy = exploit

# Agent Values
VIEW_DISTANCE = 1
# LOOK_AHEAD_DEPTH = 2    #0 for greedy algo only, else LOOK_AHEAD_DEPTH = 'n'