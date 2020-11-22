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
from consts import FILE_NAME    #file to pull/generate env from
from consts import DRAW_MAZE    #flag to show graphic window
from consts import ALPHA as alpha, GAMMA as gamma, EPSILON as epsilon
from consts import SPEED

def main():
    DRAW_MAZE = False
    number_of_turns = 0
    catchCount = 0
    env = Maze(FILE_NAME)
    # myCat = Brain(env.actions, alpha, gamma, epsilon)
# def __init__(self, name, pos, actions, given_alpha=ALPHA, gamma=GAMMA, epsilon=EPSILON):
    myCat = Brain('Cat', env.cat.pos, env.actions)
    myMouse = Brain('Mouse', env.mouse.pos, env.actions)
    cheesePos = env.cheese.pos
    board = env.mazeList
    # env.renderWindow = False
#lets impliment regular, 1step with both cat and mouse first then apply n-step.
#1-step with cat
    while True:
        print('==At start of loop, cat and mouse information:==')
        myCat.printInfo()
        myMouse.printInfo()

        # print('Calling mouse.chooseRandom with catpos mousepos cheese pos:', myCat.pos, myMouse.pos, cheesePos)
        mouseAction = myMouse.chooseAction(board, myCat.pos, myMouse.pos, cheesePos)
        mouseImmediateReward = env.moveMouse(mouseAction)
        print('immediate reward:', mouseImmediateReward)
        print('myMouse.q_table:', myMouse.q_table)


        # print('Calling cat.chooseRandom with catpos mousepos cheese pos:', myCat.pos, myMouse.pos, cheesePos)
        catAction = myCat.chooseAction(board, myCat.pos, myMouse.pos, cheesePos)
        catImmediateReward = env.moveCat(catAction)
        print('catAction:', catAction)
        print('immediate reward:', catImmediateReward)

        #get feedback from the environment
        catPos, catReward, mousePos, mouseReward, done = env.turnEnd()

        # Update agent's brains to reflect board positions after move
        myMouse.updateBrain(catPos, catReward, mousePos, mouseReward)
        myCat.updateBrain(catPos, catReward, mousePos, mouseReward)

        #immediate learning of step taken
        myMouse.learnLast(mouseImmediateReward)
        myCat.learnLast(catImmediateReward)

        #if something got caught, execute learning of agents
        if done: 
            # time.sleep(1)
            catchCount += 1
            print('Hit something')
            print('mouse q-table before learnAll')
            print(myMouse.q_table)
            myMouse.learnAll(mouseReward)
            myCat.learnAll(catReward)
            print('=AFTER=')
            # print(myMouse.q_table)
            # print(myCat.q_table)
            myCat.pos, myMouse.pos, cheesePos = env.restart()
        # env.win.getMouse()
        number_of_turns += 1
        # if number_of_turns == 100:
            # break
            
        if catchCount == 1000:
            env.renderWindow = True
            env.win.getMouse()
        if catchCount == 1100:
            break




main()
print('after main')