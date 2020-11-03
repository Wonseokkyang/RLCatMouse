"""
#####################################################
##                  RL Cat and Mouse               ##
#####################################################
#   
#   Name: Won Seok Yang
#   
##  Create a game of cat and mouse where each agent learns
#   from previous lives/cycles.
#   
#   Questions:
#   Continuous cheese vs single static run
#       If the cheese spawns in the same spot, the mouse would have a better time of learning
#   as it can relate each state with a static direction (direction of the cheese)
#       How do we overlay all the information (cat, mouse, cheese) so that the mouse
#   can learn properly? if we have a qvalue for every cat position in relation to the
#   mouse and random cheese location, thats envArea^3 values?
#   things the mouse would have to keep track of, -cat pos -cheese pos -curr pos
#   
#
#####################################################
##                  Resources                      ##
#####################################################
#
######################################################
"""
import time
from env import Maze
from consts import FILE_NAME

def main():
    env = Maze(FILE_NAME)
    
main()
print('after main')