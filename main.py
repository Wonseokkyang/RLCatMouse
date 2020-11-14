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
# from brain import Brain
from consts import FILE_NAME    #file to pull/gen env from
from consts import DRAW_MAZE    #flag to draw graphically
from consts import ALPHA as alpha, GAMMA as gamma, EPSILON as epsilon

def main():
    number_of_turns = 0
    env = Maze(FILE_NAME)
    # myCat = Brain(env.actions, alpha, gamma, epsilon)
# def __init__(self, name, pos, actions, given_alpha=ALPHA, gamma=GAMMA, epsilon=EPSILON):
    myCat = Brain('Cat', env.cat.pos, env.actions)
    myMouse = Brain('Mouse', env.mouse.pos, env.actions)
    cheesePos = env.cheese.pos
    board = env.mazeList
#lets impliment regular, 1step with both cat and mouse first then apply n-step.
#1-step with cat
    while True:
        mouseAction = myMouse.chooseRandom(board, myCat.pos, myMouse.pos, cheesePos)
        env.moveMouse(mouseAction)
        
        catAction = myCat.chooseRandom(board, myCat.pos, myMouse.pos, cheesePos)
        env.moveCat(catAction)

        env.turnEnd()

        number_of_turns += 1
        if number_of_turns == 100:
            break




main()
print('after main')