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
#   TODO:
#   maybe the problem is the agent only updating the snapshot upon W/L
#   have the agent regressively reward history along with proxHistory
#   The agents movement towards the reward will be positive. As for
#   the penalty
########################################################################
"""
import time
from env import Maze
from brain import Brain
from consts import FILE_NAME    #file to pull/generate env from
# from consts import DRAW_MAZE    #flag to show graphic window
from consts import ALPHA as alpha, GAMMA as gamma, EPSILON as epsilon
from consts import SPEED
import csv

def main():
    number_of_turns = 0 #going to use this for counting the number of steps before game end
    catchCount = 0  #count of game ends
    env = Maze(FILE_NAME)
    myCat = Brain('Cat', env.cat.pos, env.actions)
    myMouse = Brain('Mouse', env.mouse.pos, env.actions)
    cheesePos = env.cheese.pos
    board = env.mazeList

    ## DEBUGING 
    debug = False   #Step by step toggle
    env.renderWindow = False    #start with graphics being rendered

    while True:
        if debug:
            print('\nCLICK to start loop.')
            env.win.getMouse()
        print('==At start of loop, cat and mouse information:==')
        myCat.printInfo()
        myMouse.printInfo()

        if debug:
            print('\nCLICK to let mouse choose action.')
            env.win.getMouse()
        # print('Calling mouse.chooseRandom with catpos mousepos cheese pos:', myCat.pos, myMouse.pos, cheesePos)
        mouseAction = myMouse.chooseAction(board, myCat.pos, myMouse.pos, cheesePos)
        mouseImmediateReward = env.moveMouse(mouseAction)
        
        if debug:
            print('immediate reward:', mouseImmediateReward)
            print('myMouse.q_table:', myMouse.q_table)
            print('\nCLICK to let cat choose action.')
            env.win.getMouse()
        # print('Calling cat.chooseRandom with catpos mousepos cheese pos:', myCat.pos, myMouse.pos, cheesePos)
        catAction = myCat.chooseAction(board, myCat.pos, myMouse.pos, cheesePos)
        catImmediateReward = env.moveCat(catAction)
        

        if debug:
            print('catAction:', catAction)
            print('immediate reward:', catImmediateReward)
            print('myCat.q_table:', myCat.q_table)
            print('\nCLICK to get feedback from environment.')
            env.win.getMouse()
        #get feedback from the environment
        catPos, catReward, mousePos, mouseReward, done = env.turnEnd()

        #add goal rewards if any
        catImmediateReward += catReward
        mouseImmediateReward += mouseReward
        
        if debug:
            print('catPos:', catPos, 'catImmediateReward:', catImmediateReward, 'mousePos:', mousePos, 'mouseImmediateReward:', mouseImmediateReward, 'done:', done)
            print('catReward:', catReward, 'mouseReward:', mouseReward)
            print('\nCLICK to update agent Brain with positions.')
            env.win.getMouse()
        # Update agent's brains to reflect board positions after move
        myMouse.updateBrain(catPos, catReward, mousePos, mouseReward)
        myCat.updateBrain(catPos, catReward, mousePos, mouseReward)

        myCat.printInfo()
        myMouse.printInfo()

        if debug:
            print('\nCLICK to start learnLast step for both agents.')
            env.win.getMouse()
        #immediate learning of step taken 
        myMouse.learnLast(mouseImmediateReward)
        myCat.learnLast(catImmediateReward)
        myCat.printInfo()
        myMouse.printInfo()
        if debug:
            print('\nCLICK to continue.')

        #if something got caught, execute learning of agents
        if done: 
            # time.sleep(1)
            catchCount += 1
            print('Hit something')
            if debug:
                print('mouse q-table before learnAll')
                print(myMouse.q_table)
                print('mouse history before learnAll')
                print(myMouse.history)
            myMouse.learnAll(mouseReward)
            myCat.learnAll(catReward) 
            myCat.pos, myMouse.pos, cheesePos = env.restart()   #using restart() so I can program in random spot spawning
        # env.win.getMouse()
        number_of_turns += 1
        # if number_of_turns == 100:
            # break
            
        if catchCount % 1000 == 0:
            env.renderWindow = True
        if catchCount % 1001 == 2:
            env.renderWindow = False
        if (catchCount % 100 == 0) :
            saveAgent(myCat, catchCount)
            saveAgent(myMouse, catchCount)
        if catchCount == 1:
            break

# A function to save agent's memory for future testing
def saveAgent(player, catchCount):
    fieldnames = ['state', 0,1,2,3]
    wfile = csv.DictWriter(open(str(catchCount)+str(player.name)+'memory.csv', 
            'w', newline=''), fieldnames=fieldnames)
    wfile.writeheader()
    for key,val in player.q_table.items():
        row = {}
        row['state'] = key
        row[0] = val[0]
        row[1] = val[1]
        row[2] = val[2]
        row[3] = val[3]
        wfile.writerow(row)

# Function to load a saved agent's memory for testing
def loadAgent(player, itNum):
    rfile = csv.DictReader(open(str(itNum)+str(player.name)+'memory.csv', 'r'))
    for row in rfile:  
        player.q_table[row['state']] = [float(row['0']), float(row['1']), float(row['2']), float(row['3'])] 

def testLoading(itNumber):
    print('INIT base game..')
    time.sleep(1)
    catchCount = itNumber
    env = Maze(FILE_NAME)
    myCat = Brain('Cat', env.cat.pos, env.actions)
    myMouse = Brain('Mouse', env.mouse.pos, env.actions)
    cheesePos = env.cheese.pos
    board = env.mazeList

    print('loading from file')
    loadAgent(myCat, catchCount)
    loadAgent(myMouse, catchCount)
    time.sleep(1)

    print('showing agent info/q_tables')
    myCat.printInfo()
    myMouse.printInfo()
    time.sleep(1)

    print('testing running of agents from this point..')
    time.sleep(1)

    
    ## DEBUGING 
    debug = True   #Step by step toggle
    env.renderWindow = True    #start with graphics being rendered

    while True:
        if debug:
            print('\nCLICK to start loop.')
            env.win.getMouse()
        print('==At start of loop, cat and mouse information:==')
        myCat.printInfo()
        myMouse.printInfo()

        if debug:
            print('\nCLICK to let mouse choose action.')
            env.win.getMouse()
        # print('Calling mouse.chooseRandom with catpos mousepos cheese pos:', myCat.pos, myMouse.pos, cheesePos)
        mouseAction = myMouse.chooseAction(board, myCat.pos, myMouse.pos, cheesePos)
        mouseImmediateReward = env.moveMouse(mouseAction)
        
        if debug:
            print('immediate reward:', mouseImmediateReward)
            print('myMouse.q_table:', myMouse.q_table)
            print('\nCLICK to let cat choose action.')
            env.win.getMouse()
        # print('Calling cat.chooseRandom with catpos mousepos cheese pos:', myCat.pos, myMouse.pos, cheesePos)
        catAction = myCat.chooseAction(board, myCat.pos, myMouse.pos, cheesePos)
        catImmediateReward = env.moveCat(catAction)
        

        if debug:
            print('catAction:', catAction)
            print('immediate reward:', catImmediateReward)
            print('myCat.q_table:', myCat.q_table)
            print('\nCLICK to get feedback from environment.')
            env.win.getMouse()
        #get feedback from the environment
        catPos, catReward, mousePos, mouseReward, done = env.turnEnd()

        #add goal rewards if any
        catImmediateReward += catReward
        mouseImmediateReward += mouseReward
        
        if debug:
            print('catPos:', catPos, 'catImmediateReward:', catImmediateReward, 'mousePos:', mousePos, 'mouseImmediateReward:', mouseImmediateReward, 'done:', done)
            print('catReward:', catReward, 'mouseReward:', mouseReward)
            print('\nCLICK to update agent Brain with positions.')
            env.win.getMouse()
        # Update agent's brains to reflect board positions after move
        myMouse.updateBrain(catPos, catReward, mousePos, mouseReward)
        myCat.updateBrain(catPos, catReward, mousePos, mouseReward)

        myCat.printInfo()
        myMouse.printInfo()

        if debug:
            print('\nCLICK to start learnLast step for both agents.')
            env.win.getMouse()
        #immediate learning of step taken 
        myMouse.learnLast(mouseImmediateReward)
        myCat.learnLast(catImmediateReward)
        myCat.printInfo()
        myMouse.printInfo()
        if debug:
            print('\nCLICK to continue.')

        #if something got caught, execute learning of agents
        if done: 
            catchCount += 1
            print('Hit something')
            if debug:
                print('mouse q-table before learnAll')
                print(myMouse.q_table)
                print('mouse history before learnAll')
                print(myMouse.history)
            myMouse.learnAll(mouseReward)
            myCat.learnAll(catReward) 
            myCat.pos, myMouse.pos, cheesePos = env.restart()   #using restart() so I can program in random spot spawning

        if catchCount == 500000:
            break
    ## end testLoading()

def testW(player, catchCount):
    fieldnames = ['state', 0,1,2,3]
    wfile = csv.DictWriter(open(str(catchCount)+str(player.name)+'memory.csv', 
            'w', newline=''), fieldnames=fieldnames)
    wfile.writeheader()
    for key,val in player.q_table.items():
        row = {}
        row['state'] = key
        row[0] = val[0]
        row[1] = val[1]
        row[2] = val[2]
        row[3] = val[3]
        wfile.writerow(row)

### BODY ###
# main()
# print('after main')

testLoading(0)
print('after testLoading()')
