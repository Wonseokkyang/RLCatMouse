"""
#####################################################
##                  RL Cat and Mouse               ##
#####################################################
#   
#   Name: Won Seok Yang
#   
##  PRE:
#
#   Maze environment for RL cat and mouse game.
#   Responsible for initializing the maze/field environment
#   for the cat and mouse to learn in.
#  
#   Ideas: option to parse from txt or manually set
#
#####################################################
##                  Resources                      ##
#####################################################
#
######################################################
"""
from graphics import *  
from consts import SPEED, DRAW_MAZE
import random


#mouse = pink circle
#cat = red square
#cheese = yellow circle

#change mpos, cpos starting position after first round of testing

"""
mpos = mouse position <tuple>
cpos = cat position <tuple>
chpos = cheese position <tuple>
"""
UNIT = 30

class Maze:
    #Populate self with maze from FILENAME and sets default values for pos&actions
    def __init__(self, mazeTextFile):
        self.mazeList=[]
        mazeText=open('mazetxt/'+mazeTextFile+'.txt')
        for line in mazeText:
            rowList=[]
            for ch in line[:-1]:    #[:-1] all but the last char- new line 
                rowList.append(ch)
            self.mazeList.append(rowList)
        mazeText.close()

        #Cardinal directions:
        # 0 = UP,   1 = DOWN,   2 = LEFT,   3 = RIGHT
        self.actions = [0, 1, 2, 3] 
        self.colsize = len(self.mazeList[0])
        self.rowsize = len(self.mazeList)
        print("Number of rows: %d \tNumber of cols: %d" % 
                    (self.rowsize, self.colsize))

        #initializes all agent pos
        self.restart()

        #Graphics window init
        if DRAW_MAZE == True:
            self.win = GraphWin("Maze Visual "+mazeTextFile, 
                width=UNIT*self.colsize, 
                height=UNIT*self.rowsize)    #setup display window according to maze size
            self.drawMaze()

            self.mouse = Oval(Point(0,0), Point(0,0))
            self.cat = Rectangle(Point(0,0), Point(0,0))
            self.cheese = Oval(Point(0,0), Point(0,0))
            self.redrawAgents()  #draw all agents on screen according to positions
            self.win.getMouse()
            self.win.close()
    ## end __init__

    #undraw and redraw all 3 agents according to self positions
    def redrawAgents(self):
        self.mouse.undraw()
        self.cat.undraw()
        self.cheese.undraw()

        mx, my = self.mpos
        cx, cy = self.cpos
        chx, chy = self.chpos

        self.mouse = Oval( Point(mx*UNIT, my*UNIT), Point(mx*UNIT+UNIT, my*UNIT+UNIT))
        self.cat = Rectangle(Point(cx*UNIT,cy*UNIT), Point(cx*UNIT+UNIT,cy*UNIT+UNIT))
        self.cheese = Oval( Point(chx*UNIT+UNIT/4, chy*UNIT+UNIT/4), Point(chx*UNIT+UNIT-UNIT/4, chy*UNIT+UNIT-UNIT/4))

        self.mouse.setFill("pink")
        self.cat.setFill("red")
        self.cheese.setFill("yellow")

        self.mouse.draw(self.win)
        self.cat.draw(self.win)
        self.cheese.draw(self.win)
        time.sleep(SPEED)
    ## end redrawAgents


    #restarts the maze like it was initialized, resetting agent's tracked xpos, ypos
    def restart(self):
        #Agent(s) objct positions init, starting positions
        #Mouse POSition, Cat POSition, CHeese POSition
        self.mpos = (0, 0)   #always start at 0,0
        self.cpos = (self.rowsize-1, self.colsize-1)
        self.chpos = (random.randint(0,self.rowsize-1), random.randint(0,self.colsize-1))  #random position on board
        while (self.chpos == self.mpos or self.chpos == self.cpos):
            self.chpos = (random.randint(0,self.rowsize-1), random.randint(0,self.colsize-1))  
    ## end restart

    #Graphic visualization of maze
    def drawMaze(self):
        for x in range(self.rowsize):      #populating maze squares
            for y in range(self.colsize):
                dSquare = Rectangle(Point(x*UNIT,y*UNIT), Point(x*UNIT+UNIT,y*UNIT+UNIT))
                if self.mazeList[x][y] =='#':   #walls
                    dSquare.setFill("black")
                    dSquare.draw(self.win)
                else:                           #empty squares
                    dSquare.setFill("light grey")
                    dSquare.draw(self.win)
    ## end drawMaze

"""
    #Takes int argument for action/direction to move the agent to calculate the reward and new self.pos
    def moveAgent(self, direction_num):
        #  Takes int argument for action/direction to move the agent to calculate the reward and new self.pos
        #     RETURN: self.pos, reward, done
        #     <tuple> self.pos after move- same state in the case of wall or out of bounds
        #     <int>   reward value for moving to that state
        #     <bool>  done flag when the move results in the agent exiting the maze 
        # print('Print type of direction_num in moveAgent(d_num)', type(direction_num)) #demo false -> int    # # CSV TEST
        if direction_num == 0: dy, dx = 1, 0        #UP
        elif direction_num == 1: dy, dx = -1, 0     #DOWN
        elif direction_num == 2: dy, dx = 0, -1     #LEFT
        elif direction_num == 3: dy, dx = 0, 1      #RIGHT
        
        x,y = self.pos
        tx, ty = self.tpos

        #if the agent attempts to move off screen, remove agent from window before resetting
        #agent is out of bounds so give penalty
        if ((x+dx < 0) or (x+dx > self.rowsize-1)) or ((y+dy < 0) or (y+dy > self.rowsize-1)):
            if ANNOUNCE_AGENT_MOVES == True: print('Agent went out of bounds')
            if DRAW_MAZE == True:
                self.agent.undraw()
                time.sleep(SPEED)
                self.resetAgent()
            reward = OUT_OF_FRAME
            done = False
        #agent hit a wall, blink agent on wall before resetting
        #wall hit so give penalty
        elif self.mazeList[x+dx][y+dy] == '#':
            if ANNOUNCE_AGENT_MOVES == True: print('Agent hit a wall')
            if DRAW_MAZE == True:
                self.agent.move(dx*UNIT,dy*UNIT)
                time.sleep(SPEED)
                for i in range(2):  #blinking animation
                    self.agent.undraw()
                    time.sleep(SPEED/4)
                    self.agent.draw(self.win)
                    time.sleep(SPEED/4)
                self.resetAgent()
            reward = WALL
            done = False
        #agent found the target so reward and trigger done flag
        elif x+dx == tx and y+dy == ty:
            if ANNOUNCE_AGENT_MOVES == True: print('Agent found the target!')
            if DRAW_MAZE == True:
                self.agent.move(dx*UNIT,dy*UNIT)
                self.pos = (x+dx, y+dy)
                time.sleep(SPEED)
            reward = TARGET
            done = True
        #agent landed on regular tile
        else:
            if ANNOUNCE_AGENT_MOVES == True: print('Agent moved')
            if DRAW_MAZE == True:
                self.agent.move(dx*UNIT,dy*UNIT)
                time.sleep(SPEED)
            self.pos = (x+dx, y+dy)
            reward = MOVE
            done = False
        # print('self.pos, reward, done', self.pos, reward, done) # # CSV TEST
        return self.pos, reward, done
"""
    