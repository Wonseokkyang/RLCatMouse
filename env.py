"""
########################################################################
##                       RL Cat and Mouse                             ##
########################################################################
#   
#   Name: Won Seok Yang
#   
##  PRE:
#   Maze environment for RL cat and mouse game.
#   Responsible for initializing the maze/field environment for the cat
#   and mouse to learn in.
#  
#   Ideas: option to parse from txt or manually set?
#   
#   Questions: should the cheese spawn in different spots?
#   -how about the cat and mouse? changing spawn spots would make the 
#   agents 'smarter' but requires way more memory space for each agent.
#   -should the cat know where the cheese is? if it does, it could come
#   up with blocking/camping strategies :o
#   -who goes first? do they go at the same time? what if they tie 
#   (cat and mouse are both on cheese cell)?
#   #lets have the mouse go first. in case of tie, cat wins and mouse 
#   gets both reward and penalty. this means I cant calculate the 
#   mouse's q-value until after they both go.
#
#   Edit: 11/3- blank maze for now but left in code for walls
########################################################################
##                          Resources                                 ##
########################################################################
#   Style guide:
#   https://www.python.org/dev/peps/pep-0008/#multiline-if-statements
########################################################################
##                          Notes                                     ##
########################################################################
#   I want to use the move function for both cat and mouse but they have
#   different reward conditions. maybe I can move cat and mouse first 
#   then calculate reward?
#   ex: move cat. move mouse. check if mouse is on cheese. check if cat
#   is on mouse. 
#   how do I feed this back into the brain though? 
#   DECISION: cat and mouse move "at the same time" and a turnEnd()
#   function will serve as a neat packer to pass the required values
#
#   
########################################################################
"""
from graphics import *  
from consts import SPEED, DRAW_MAZE, UNIT, OUT_OF_FRAME, WALL, MOVE, TARGET, ANNOUNCE_AGENT_MOVES
import random


#mouse = pink circle
#cat = red square
#cheese = yellow circle

#change mpos, cpos starting position after first round of testing

"""
Maze class also holds a nested Agent class for the cat, mouse, and cheese
"""
class Maze:
    #Populate self with maze from FILENAME
    def __init__(self, mazeTextFile):
        self.mazeList=[]
        mazeText=open('mazetxt/'+mazeTextFile+'.txt')
        for line in mazeText:
            rowList=[]
            for ch in line[:-1]:  #[:-1] last char excluded- new line 
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

        #initializes all agent objects
        self.initAgents()

        #Graphics window init
        if DRAW_MAZE == True:
            #setup display window according to maze size
            self.win = GraphWin("Maze Visual "+mazeTextFile, 
                width=UNIT*self.colsize, 
                height=UNIT*self.rowsize)    
            self.drawMaze() #base layer of graphical window
            self.redrawAgents()  #draw all agents on screen
    ## end __init__

    #starting pos of agents- also in restart()
    def initAgents(self):
        mousepos = (0,0)
        catpos = (self.rowsize-1, self.colsize-1)
        #random position on board
        cheesepos = (random.randint(0,self.rowsize-1), 
                    random.randint(0,self.colsize-1))  
        while (cheesepos == mousepos or cheesepos == catpos):
            cheesepos = (random.randint(0,self.rowsize-1), 
                        random.randint(0,self.colsize-1))

        mx, my = mousepos
        cx, cy = catpos
        chx, chy = cheesepos

        self.mouse = self.Agent(
                Oval(Point(mx*UNIT, my*UNIT), 
                Point(mx*UNIT+UNIT, my*UNIT+UNIT)), 
                "pink", mousepos, "Mouse")
        self.cat = self.Agent(
                Rectangle(Point(cx*UNIT,cy*UNIT), 
                Point(cx*UNIT+UNIT,cy*UNIT+UNIT)), 
                "red", catpos, "Cat")
        self.cheese = self.Agent(
                Oval( Point(chx*UNIT+UNIT/4, chy*UNIT+UNIT/4), 
                Point(chx*UNIT+UNIT-UNIT/4, chy*UNIT+UNIT-UNIT/4)), 
                "yellow", cheesepos, "Cheese")
    ## end initAgents

    #undraw and redraw all 3 agents according to Agent positions
    def redrawAgents(self):
        mx, my = self.mouse.pos
        cx, cy = self.cat.pos
        chx, chy = self.cheese.pos

        self.mouse = self.Agent(
                Oval(Point(mx*UNIT, my*UNIT), 
                Point(mx*UNIT+UNIT, my*UNIT+UNIT)), 
                "pink", self.mouse.pos, "Mouse")
        self.cat = self.Agent(
                Rectangle(Point(cx*UNIT,cy*UNIT), 
                Point(cx*UNIT+UNIT,cy*UNIT+UNIT)), 
                "red", self.cat.pos, "Cat")
        self.cheese = self.Agent(
                Oval(Point(chx*UNIT+UNIT/4, chy*UNIT+UNIT/4), 
                Point(chx*UNIT+UNIT-UNIT/4, chy*UNIT+UNIT-UNIT/4)), 
                "yellow", self.cheese.pos, "Cheese")

        self.mouse.redraw(self.win)
        self.cat.redraw(self.win)
        self.cheese.redraw(self.win)
    ## end redrawAgents

    #restarts agent's tracked pos to starting value
    #also randomizes cheese placement on each restart (??)
    def restart(self):
        print('RESTART CALLED')
        self.mouse.undraw(self.win)
        self.cat.undraw(self.win)
        self.cheese.undraw(self.win)

        #Agent(s) objct positions init, starting positions
        self.mouse.pos = (0, 0)   #always start at 0,0
        self.cat.pos = (self.rowsize-1, self.colsize-1)
        #random position on board
        self.cheese.pos = (random.randint(0,self.rowsize-1), 
                          random.randint(0,self.colsize-1))  
        while (self.cheese.pos == self.mouse.pos 
                or self.cheese.pos == self.cat.pos):
            self.cheese.pos = (random.randint(0,self.rowsize-1), 
                              random.randint(0,self.colsize-1))
        if DRAW_MAZE == True: self.redrawAgents()
    ## end restart

    #Graphic visualization of maze
    def drawMaze(self):
        for x in range(self.rowsize):      
            for y in range(self.colsize):
                dSquare = Rectangle(Point(x*UNIT,y*UNIT), Point(x*UNIT+UNIT,y*UNIT+UNIT))
                if self.mazeList[x][y] =='#':   #walls
                    dSquare.setFill("black")
                    dSquare.draw(self.win)
                else:                           #empty squares
                    dSquare.setFill("light grey")
                    dSquare.draw(self.win)
    ## end drawMaze

    def moveAgent(self, agent, direction_num):
        x, y = agent.pos
        agent.reward = 0    #reset reward value
        if direction_num == 0: dy, dx = 1, 0        #UP
        elif direction_num == 1: dy, dx = -1, 0     #DOWN
        elif direction_num == 2: dy, dx = 0, -1     #LEFT
        elif direction_num == 3: dy, dx = 0, 1      #RIGHT

        #If agent out of bounds- remove agent from screen and redraw
        if (x+dx < 0 or x+dx > self.rowsize-1) or (
            y+dy < 0 or y+dy > self.colsize-1):
            #Out of bounds
            if ANNOUNCE_AGENT_MOVES == True: 
                print(agent.name,'went out of bounds')
            if DRAW_MAZE == True:
                agent.undraw(self.win)
                time.sleep(SPEED)
                agent.redraw(self.win)
            agent.reward = OUT_OF_FRAME
        #Agent hit a wall- blink agent on wall before resetting
        elif self.mazeList[x+dx][y+dy] == '#':
            if ANNOUNCE_AGENT_MOVES == True: 
                print(agent.name, 'hit a wall')
            if DRAW_MAZE == True:
                #graphically move on screen but dont update agent pos
                agent.shapeObj.move(dx*UNIT,dy*UNIT)    
                agent.blink(self.win)
                agent.redraw(self.win)
            agent.reward = WALL
        #Agent landed on regular tile
        else:
            if ANNOUNCE_AGENT_MOVES == True: print(agent.name,'moved')
            if DRAW_MAZE == True:
                agent.shapeObj.move(dx*UNIT,dy*UNIT)
                time.sleep(SPEED)
            agent.pos = (x+dx, y+dy)
            agent.reward = MOVE
        # print(agent.name, ', reward', agent.pos, agent.reward )
    ## end moveAgent

    # The cat catching the mouse and the mouse getting 
    # the cheese in the same turn is possible
    def turnEnd(self):
        done = False
        #cat eat mouse
        if self.cat.pos == self.mouse.pos:
            self.cat.reward += CAUGHT
            self.mouse.reward -= CAUGHT
            done = True
        #mouse eat cheese
        if self.mouse.pos == self.cheese.pos:
            self.mouse.reward += TARGET
            done = True
        return self.cat.pos, self.cat.reward, self.mouse.pos, self.mouse.reward, done

    ## Wrappers for moving agents- calls moveAgent
    def moveMouse(self, direction_num):
        self.moveAgent(self.mouse, direction_num)
    ## end moveMouse
    def moveCat(self, direction_num):
        self.moveAgent(self.cat, direction_num)
    ## end moveCat

    class Agent:
        def __init__(self, shape, color="green", 
                    pos=(0,0), name="BLANK"):
            self.shapeObj = shape
            self.shapeObj.setFill(color)
            self.pos = pos
            #for testing and terminal printing
            self.name = name    
            self.reward = 0
        
        #for testing
        def printAgentInfo(self):
            print(self.name, 'shapeObj=', self.shapeObj, 'pos=', self.pos)

        def blink(self, window):
            for _ in range(2):
                self.shapeObj.undraw()
                time.sleep(SPEED/4)
                self.shapeObj.draw(window)
                time.sleep(SPEED/4)

        def undraw(self, window):
            self.shapeObj.undraw()

        def redraw(self, window):
            self.shapeObj.undraw()
            self.shapeObj.draw(window)


    
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
    