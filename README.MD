# Reinforced Learning - Cat and Mouse

A ***DUAL*** reinforced learning program! Both the cat agent and the mouse agent use reinforced learning to navigate and exploite the maze while trying to out smart the other.

General Agent behavior: 
- Given current position in the board, choose a direction to move according to state:values stored in memory.
- Learns from immediate actions as well has a history of pervious actions
    - Reward scheme: (values configurable)
    - Agent tries to move out of bounds -100
    - Agent tries to move into a square occupied by a wall -10
    - Agent moves to an unoccupied square -1
    - Agent reaches it's goal condition +20
