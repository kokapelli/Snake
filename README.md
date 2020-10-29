# Snake
A snake game that is trained using Deep Q-learning in an attempt to create a suitable snake opponent to myself

# State Space
All and all the input of the NN will consist of 32 nodes. These nodes create the state space and the following nodes does the following:
* Eight vision directions (24)
    * Each vision searches for three things
        * Food
        * Walls
        * Itself
* The trajectory the snake is currently travelling (4)
* The trajectory the tail is currently travelling (4)