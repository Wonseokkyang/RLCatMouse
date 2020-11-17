"""#####################################################################
##                RL Cat and Mouse - brain                            ##
########################################################################
#   
#   Name: Won Seok Yang
#   
##  PRE:
#   The "brain" of the cat and mouse agents where the calculations and
#   learnings are processed and saved.
#  
#   Notes:
#   The cat and mouse must know each other's position. The cat is more 
#   straight forward. The cat only needs to know the mouse's position
#   while the mouse has to keep track of both the cat and cheese.
#   Factoring in only the board/env size, n*m, and possible action at
#   each state, 4- the list of q-value entries is n*m length long with
#   4 values at each of those index states.
#   If we factor in the mouse, the mouse can be in any n*m position so
#   the q-table becomes 4*(n*m)^2 index's long with the entries becoming
#   (cat_pos, mouse_pos, possible_actions).
#   The mouse on the otherhand also has to factor in the cheese. If the
#   cheese was static, as in, it doesn't spawn at different squares in the 
#   board, the q-table for the mouse would be the same as the cat.
#   With changing cheese location/spawn, it becomes 4*(n*m)^3 entries.
#
#   Question:
#   Do i want to make it fun and have the cheese spawn in different 
#   positions when the mouse gets it?
#   Should the cat&mouse continue from where it left off or start over?
#   If they start over, do they spawn in the same spot?
#   Would n-step lookahead be applicable? N-step would be used for 
#   minamaxing in this case. 
#   
#   Ideas:
#   I'd love to create a visual heat map of the q-values at different
#   cat/mouse/cheese positions to get a gauge of what the agents are
#   'thinking'.
#   Applying a neural network would be awesome but that requires much
#   more research
#
#   Applying and adjusting what the professor suggested, perhaps the
#   agent can keep a 'snapshot' of however big area around itself.
#   within this 'snapshot' I can use the direct line Christina mentioned
#   during class to include the cat in the snapshot if it's within 
#   direct line of sight of the mouse.
#
########################################################################
##                          Resources                                 ##
########################################################################
#   Style guide:
#   https://www.python.org/dev/peps/pep-0008/#multiline-if-statements
########################################################################
##                          Notes                                     ##
########################################################################
#   Problem I'm facing: 
#   So I can implement a snapshot of the agent's surroundings to add
#   to ass to the q-table but how about the walls and out of bounds?
#   I was initially planning on having the agents run until an end
#   condition is met but then how would I update the agent's penalty for
#   running out of frame?
#   I could possibly call the learning function early if the agent's
#   reward isn't 0 in the main body of the program.
# 
#   Perhaps instead of vision distance we do depth distance, simulating
#   the agent 
########################################################################
"""
import random
import pandas as pd
import numpy as np
from consts import VIEW_DISTANCE, ALPHA, GAMMA, EPSILON

#const view_distance 

class Brain:
    #List of actions provided during first func call
    def __init__(self, name, pos, actions, alpha=ALPHA, gamma=GAMMA, epsilon=EPSILON):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}   #key : snapshot of n area around agent. value : cardinal directions
        self.history = []
        self.name = name    #mainly for troubleshooting
        self.pos = pos
    ## end __init__

    # Given envState and agent objects, choose a random direction number to return
    # Return: random direction
    def chooseRandom(self, envState, catPos, mousePos, cheesePos):
        if self.name == 'Mouse': self.pos = mousePos
        else: self.pos = catPos

        action = self.actions[random.randint(0, len(self.actions)-1)]
        # Tuple of (state, action)
        self.history.append(
            (self.hashProcess(
                envState, catPos, mousePos, cheesePos), action))
        return action
    ##end chooseRandom

    # Given envState and agent objects, choose best action
    # Return: Action with highest q-value
    def chooseAction(self, envState, catPos, mousePos, cheesePos):
        if self.name == 'Mouse': self.pos = mousePos
        else: self.pos = catPos

        # Pick direction that will get you into a state with the
        # highest q-value.
        #for all actions, simulate the state if you were to move in
        #that direction
        hashed = self.hashProcess(
            envState, catPos, mousePos, cheesePos)
        actionChoices = self.q_table.get(hashed, [0] * len(self.actions))
        maxPool = []
        maxVal = -999
        for indx, val in enumerate(actionChoices):
            if val == maxVal:
                maxPool.append(indx)
            if val > maxVal:
                maxPool.clear()
                maxVal = val
                maxPool.append(indx)
        print('after populating maxPool:', maxPool)

        action = max(maxPool)

        print('Action pool:', actionChoices)
        print('Chosen action index =', action)
        # Tuple of (state, action)
        self.history.append(
            (self.hashProcess(
                envState, catPos, mousePos, cheesePos), action))
        return action

    # Given curr board, init q-table a board snapshot according to vDist
    # and return the hashed 1d string of snapshot for tracking
    # Return: string representing envState reduced to view distance of agent
    def hashProcess(self, envState, catPos, mousePos, cheesePos):
        # given the current board, extract the board snapshot around the agent of VIEW_DISTANCE
        x,y = self.pos
        snapshot = ''
        for rowNum, row in enumerate(envState):
            if rowNum <= x + VIEW_DISTANCE and rowNum >= x - VIEW_DISTANCE:
                for colNum, square in enumerate(row):
                    if colNum <= y + VIEW_DISTANCE and colNum >= y - VIEW_DISTANCE:
                        if (rowNum, colNum) == catPos: 
                            snapshot += 'C'
                        elif (rowNum, colNum) == mousePos: 
                            snapshot += 'm'
                        elif (rowNum, colNum) == cheesePos: 
                            snapshot += '*'
                        elif square == ' ':
                            snapshot += '-'
                        else:
                            snapshot += square
        print('Snapshot:', snapshot)
        # add in mouse/cheese/cat by checking visibility w/ a function
        # check to see if there's a wall obscuring the mouse/cat 's vision from seeing the cheese/mouse/cat
            # true- keep obscured agent out of snapshot
            # false- include agent in snapshot
        return snapshot
    ## end hashProcess

    # Calculate reward for the last move performed from history stack 
    # and update q-table.
    # Return: reward * discount factor
    def learnStep(self, step, reward):
        # Get last move's value or set it to 0 if it doesnt exist
        lastState, lastAction = step
        values = self.q_table.get(lastState, [0] * len(self.actions))
        self.q_table.update({lastState : values})

        print('specific value before update-', self.q_table[lastState][lastAction])


        # Update state:action for that one action
        # learning rate * (discount factor * reward - current value at that action)
        self.q_table[lastState][lastAction] += self.alpha * (
            self.gamma * reward - self.q_table[lastState][lastAction])


        print('for step reward:', step, reward)
        print('specific value after update-', self.q_table[lastState][lastAction])
        return reward * self.gamma
    ## end learnStep

    # Calculate and update for all steps taken in self.history
    def learnAll(self, reward):
        newReward = reward
        for _ in range(len(self.history)):
            newReward = self.learnStep(self.history.pop(), newReward)
        print('History after learnAll finishs:', self.history)
    ## end learnAll

    # Wrapper to call learnStep from outside class
    def learnLast(self, reward):
        self.learnStep(self.history[len(self.history)-1], reward)
    ## end learnLast

    # Update self info with given info from board/main program
    def updateBrain(self, catPos, catReward, mousePos, mouseReward):
        if self.name == 'Mouse': 
            self.pos = mousePos
            # print('Updated mouse brain:', self.pos)
        else: 
            self.pos = catPos
            # print('Updated cat brain:', self.pos)
    ## end updateBrain

    def printInfo(self):
        print(' name:', self.name)
        print(' position:', self.pos)
        print(' history:', self.history)
    ## end printInfo

        # def choose_action(self, state):
    #     """
    #     Given state, choose an action according to EPSILON/greediness
    #     RETURN: action
    #     <int> action direction- epsilon/100 chance of moving to 
    #     highest qvalue, (100-epsilon)/100 chance of moving randomly
    #     """
    #     self.state_exist_check(state)   #append to q_table if it doesnt exist already
    #     if np.random.uniform() < self.epsilon:  #greediness 'roll'- if less, then be greedy
    #         action_choices = self.q_table.loc[str(state), :]     #a list of directional values from 'state' ex: [0, 0, 0.5, 0]   left has highest value
    #         #from chooseable actions, pick out of the largest/max
    #         action = np.random.choice(action_choices[action_choices == np.max(action_choices)].index)
    #     else:   #otherwise, choose random
    #         action = np.random.choice(self.actions)
    #     return int(action)

#   def state_exist_check(self, state):
#         if str(state) not in self.q_table.index:
#             self.q_table = self.q_table.append(     #required to assign a copy of the append q_table to original to keep values for some reason
#                 pd.Series(      #make an entrie to the q_table according to this format for easy manipulation later
#                     [0] * len(self.actions),
#                     index = self.q_table.columns,   #columns of series entry according to dataframe(q_table) columns
#                     name = str(state),   #the name(left most column for indexing)
#                 )
#             )
    # #updating q_table values
    # def calculate(self, state, action, reward, new_state, target):
    #     """ Takes arguments and updates q-value table according to bellman equation that's influenced by alpha or learn rate
    #         RETURNS: q_
    #         <int> q_ is the predicted qvalue for the given state action pair
    #     """ 
    #     self.state_exist_check(new_state)   #append the new_state to q_table to add/manip calculations
    #     q = self.q_table.loc[str(state), action]   #Q value
    #     # print('After q assignment') # # CSV TEST

    #     if new_state != target:   #agent didnt find exit
    #         q_ = reward + self.gamma * self.q_table.loc[str(new_state),:].max()    #max possible Q of new state
    #     else:   # agent found exit so there is no future state, just give reward
    #         q_ = reward
    #     self.q_table.loc[str(state),action] += self.alpha*(q_ - q) #update q_table with difference between estimate and actual * learning rate

    #check if state exists in q_table, if not append it
  

