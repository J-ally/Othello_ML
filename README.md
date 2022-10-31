# Othello_ML

Project Assignement : Apply ML algorithms, where the AI plays against a player (min max, alpha beta and also random methods ...) on the game of Othello.

# Othello game kernel

## Board class

The whole game mechanics and "kernel" is presenet under the __Board__ class. It is a class that represents the board, but also the current stat of the game being played itself. 

The boards prints itself this way in the terminal :

<p align="center">
<img src="https://github.com/ ..." alt="Screenshot of the terminal" width="400"/>
</p>

### Board class attributes

The __Board__ class has the following attributes:
### Methods
It has the following methods :

- initialise_game() : places the 4 tiles in the middle of the board
- print_board() : prints the board in the console
- is_valid_loc(move) : checks if a move is valid
- generate_tiles_to_be_flipped(move, player) : generates the tiles to be flipped after a move for a player
- flip_tiles(tiles_to_be_flipped) : flips the tiles in the list
- place_tile(move, player) : places a tile for a player and a move
- generate_all_possible_moves(player) : generates all the possible moves for a player for a turn
- generate_possible_boards (player) : generates all the possible boards for a player for a turn
- generate_board_after_move(move, player) : generates a board after a move for a player

# "Gameplay"

For the moment, the player can only play against another player, by typing in the terminal the moves in a tuple format (x, y). The game ends when there are no more possible moves for both players.

No evaluation function has been implemented yet (score).

Player will be able to play against the AI in the future.


