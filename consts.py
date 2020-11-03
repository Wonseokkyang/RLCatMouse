#Draw the graphical window to show the agent(s) in action. If false, simulate the runs until the end
DRAW_MAZE = True    
ANNOUNCE_AGENT_MOVES = True

#Number of seconds to pause after drawing each step. Window refresh rate
SPEED = 0.5

#Name of txt file to create the learning environment
FILE_NAME = 'blank10x10'   #file name to parse from w/o extension

#Size of individual squares
UNIT = 30

#Reward values:
OUT_OF_FRAME = -100.0   #out of bounds penalty
WALL = -10.0            #hitting a wall penalty
MOVE = -0.1             #moving into a square penalty
TARGET = 100.0          #finding the end of the maze reward
