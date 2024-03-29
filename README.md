# Othello_ML

Project Assignement : Apply ML algorithms, where the AI plays against a player (min max, alpha beta and also random methods ...) on the game of Othello.

# Othello game kernel
## Board class

The whole game mechanics and "kernel" is present under the __Board__ class. It is a class that represents the board, but also the current stat of the game being played itself. 

The boards prints itself this way in the terminal (showing the move played):

<p align="center">
<img src="https://raw.githubusercontent.com/J-ally/Othello_ML/main/Images/2022-11-11%2014_47_00-Window.png"  width="300"/>
</p>

Player white is defined as "O" and player black is defined by "0". An empty cell is represented by a " ".

The board itself is coded as a numpy matrix of strings.
### Board class attributes

The __Board__ class has the following attributes (showed as initialized) :
- previous_moves = {"O" : [], "0" : []}

    Used to record all the moves played by the players. White plays first, then black, then white, etc.
- occupied_tiles = [] 
    
    Used to record all the tiles occupied at the moment by the players. 
### Methods
It has the following methods :

- initialise_game () : places the 4 tiles in the middle of the board
- print_board () : prints the board in the console
- is_valid_loc (_move_) : checks if a move is valid location wise (not outside of the board)
- generate_tiles_to_be_flipped (_move_, _player_) : generates the tiles to be flipped after a move, for a player
- flip_tiles (_tiles_to_be_flipped_) : flips the tiles in the list generated by flip_tiles
- place_tile (_move_, _player_) : places a tile for a player and a move
- generate_all_possible_moves (_player_) : generates all the possible moves for a player for one turn
- generate_board_after_move (_move_, _player_) : generates a board after a move for a player
- generate_possible_boards (_player_) : generates all the possible boards for a player for one turn

## Game

The game is played in the terminal, and the board can be printed at any time by typing "Board.print_board()". 
A naïve evaluation function has been coded (using the score).
The game itself is played via the Board class, each Board having it's own possibilities of future moves and plays (which are generated as another Board instance).
Each Board now has its own history of moves, and occupied tiles.

# "Gameplay"

## Evaluation function

### Naïve evaluation function
The evaluation function is a simple one, it is based on the score of the game : each player for a move (and only one) chooses the move which gives him the best score. The score is calculated by counting the number of tiles for each player.

### Evaluation function with ML

## The different game modes
- Player vs Player : 

    the player can only play against another player, by typing in the terminal the moves in a tuple format (x, y). The game ends when the board is full.

- Computer vs Computer (using random moves) :

    the computer plays against itself, using random moves. The game ends when the board is full.

- Computer vs Computer (using min max) :

- Computer vs Computer (using alpha beta) :



# Libraries

- numpy