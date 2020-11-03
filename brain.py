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
#   Ideas: option to parse from txt or manually set?
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


class Brain:
    #List of actions provided during first func call
    def __init__(self, actions, given_alpha, GAMMA, EPSILON):
        self.actions = actions
        self.alpha = given_alpha
        self.gamma = GAMMA
        self.epsilon = EPSILON
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def choose_action(self, state):
        """
        Given state, choose an action according to EPSILON/greediness
        RETURN: action
        <int> action direction- epsilon/100 chance of moving to 
        highest qvalue, (100-epsilon)/100 chance of moving randomly
        """
        self.state_exist_check(state)   #append to q_table if it doesnt exist already
        if np.random.uniform() < self.epsilon:  #greediness 'roll'- if less, then be greedy
            action_choices = self.q_table.loc[str(state), :]     #a list of directional values from 'state' ex: [0, 0, 0.5, 0]   left has highest value
            #from chooseable actions, pick out of the largest/max
            action = np.random.choice(action_choices[action_choices == np.max(action_choices)].index)
        else:   #otherwise, choose random
            action = np.random.choice(self.actions)
        return int(action)

    #updating q_table values
    def calculate(self, state, action, reward, new_state, target):
        """ Takes arguments and updates q-value table according to bellman equation that's influenced by alpha or learn rate
            RETURNS: q_
            <int> q_ is the predicted qvalue for the given state action pair
        """ 
        self.state_exist_check(new_state)   #append the new_state to q_table to add/manip calculations
        q = self.q_table.loc[str(state), action]   #Q value
        # print('After q assignment') # # CSV TEST

        if new_state != target:   #agent didnt find exit
            q_ = reward + self.gamma * self.q_table.loc[str(new_state),:].max()    #max possible Q of new state
        else:   # agent found exit so there is no future state, just give reward
            q_ = reward
        self.q_table.loc[str(state),action] += self.alpha*(q_ - q) #update q_table with difference between estimate and actual * learning rate

    #check if state exists in q_table, if not append it
    def state_exist_check(self, state):
        if str(state) not in self.q_table.index:
            self.q_table = self.q_table.append(     #required to assign a copy of the append q_table to original to keep values for some reason
                pd.Series(      #make an entrie to the q_table according to this format for easy manipulation later
                    [0] * len(self.actions),
                    index = self.q_table.columns,   #columns of series entry according to dataframe(q_table) columns
                    name = str(state),   #the name(left most column for indexing)
                )
            )

    #recursive call to update q_value of all directions from state
    def n_step(self, env, state, depth):
        state = env.pos
        if depth > 0:
            self.state_exist_check(state)
            for action in self.actions: #for every direction move and calculate
                # print('check action:', action, ' state:', state)
                env.pos = state #reset for each direction
                new_state, reward, done = env.moveAgent(action)
                self.calculate(state, action, reward, new_state, env.tpos)
                self.n_step(env, new_state, depth-1)
                # print('after check action:', action, ' state:', state)
        env.pos = state
