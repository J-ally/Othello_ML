# Othello_ML

Project Assignement : Apply ML algorithms, where the AI plays against a player (min max, alpha beta and also random methods ...) on the game of Othello.

# Othello game kernel
## Board class

The whole game mechanics and "kernel" is presenet under the __Board__ class. It is a class that represents the board, but also the current stat of the game being played itself. 

The boards prints itself this way in the terminal :

<p align="center">
<img src="https://raw.githubusercontent.com/J-ally/Othello_ML/main/images/2022-10-31%2019_36_01-othello_backend.py%20-%20Othello_ML%20-%20Visual%20Studio%20Code.png" alt="Screenshot of the terminal" width="400"/>
</p>

Player white is defined as "O" and player black is defined by "0". An empty cell is represented by a " ".

The board is coded as a numpy matrix of strings.
### Board class attributes

The __Board__ class has the following attributes:
### Methods
It has the following methods :

- initialise_game () : places the 4 tiles in the middle of the board
- print_board () : prints the board in the console
- is_valid_loc (_move_) : checks if a move is valid
- generate_tiles_to_be_flipped (_move_, _player_) : generates the tiles to be flipped after a move for a player
- flip_tiles (_tiles_to_be_flipped_) : flips the tiles in the list
- place_tile (_move_, _player_) : places a tile for a player and a move
- generate_all_possible_moves (_player_) : generates all the possible moves for a player for a turn
- generate_possible_boards (_player_) : generates all the possible boards for a player for a turn
- generate_board_after_move (_move_, _player_) : generates a board after a move for a player

# "Gameplay"

For the moment, the player can only play against another player, by typing in the terminal the moves in a tuple format (x, y). The game ends when there are no more possible moves for both players.

The game is played in the terminal, and the board can be printed at any time by typing "print_board()". 

No evaluation function has been implemented yet (score).

Player will be able to play against the AI in the future. For the moment, one future move (given a board) can be generated.
For the algorithms implementation, one will have to use the board class as a way to represent the game state, and future moves will be generated as a board instance.

Board class still miss the whole "history" of moves for each player to be full used as a ML input.

# Libraries

- numpy

