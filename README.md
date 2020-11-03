# Snake
A snake game that is trained using Deep Q-learning in an attempt to create a suitable snake opponent to myself

# How To Play
The game is primarily played by using <pre><code>Play.py</code></pre>. Some additional arguments exist that depends on what the user wish to do. 
* *--debug*: places the game in debug mode. Slowing the game down and displays most of the relevant information in the console.
* *--terminal*: Removes the GUI aspect of the game and allows the computer to play the game. Primarily used in training purposes.
* *--size*: Determined the size of the game, currently it is refrained form changing this as the game is primarily built on the square dimensions of 22x22, whereas the play zone is 20x20 and the last two is reserved for walling. 

# State Space
All and all the input of the NN will consist of 32 nodes. These nodes create the state space and the following nodes does the following:
* Eight vision directions (24)
    * Each vision searches for three things
        * Food
        * Walls
        * Itself
* The trajectory the snake is currently travelling (4)
* The trajectory the tail is currently travelling (4)