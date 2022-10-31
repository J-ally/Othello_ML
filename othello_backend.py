# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 2022
@author:  jaly
"""

import logging
import numpy as np


###############################################################################
#                          LOGGING DEFINITION                                 #
###############################################################################

logging.basicConfig(level=logging.INFO, filename = "logs_othello_backend.log", filemode = "w",
                    format = "%(asctime)s - %(levelname)s - %(message)s")

###############################################################################
#                              GLOBALS                                        #
###############################################################################



###############################################################################
#                         GAME INITIALISATION                                #
###############################################################################

class Board () :
    """
    The board is a numpy array of size 8x8. Each cell contains a string.
    O represents a white tile
    0 represents a black tile
    """
    
    occupied_tiles = []
    
    game_count = 1 #the number of turn played
    #Player defined as O for white and 0 for black
    curr_player = "O"  #current player (white starts)
    
    def __init__ (self, size = 8) :
        """
        initialises the board
        Inputs : size (int) : the size of the board (Defaults to 8)
        """
        self.size = size
        self.board = np.zeros((self.size,self.size), dtype= str)
        self.board [:] = " "
        
        logging.info(f"the size of the of the game : {self.size} \n")
        pass


    def initialise_game (self) :
        """
        initialise the game (places the 4 tiles in the middle of the board)
        Inputs : 
        Returns :
        """
        
        middle_1, middle_2 = (self.size-1)//2, ((self.size-1)//2) + 1
        
        self.board [middle_1][middle_1] = "O"
        self.board [middle_2][middle_2] = "O"
        self.board [middle_1][middle_2] = "0"
        self.board [middle_2][middle_1] = "0"
        
        self.occupied_tiles = [(middle_1,middle_1), (middle_2,middle_2), (middle_1,middle_2), (middle_2,middle_1)]
        logging.debug(f"occupied tiles : {self.occupied_tiles} \n")
         
        logging.info(f"game initialised with middle_1 = {middle_1} and middle_2 = {middle_2}\n")
        pass
    
    
    def print_board (self) :
        """
        print the board
        Inputs : 
        Returns :
        """
        print ("\n---------------------------------")
        for i in range (self.size) :
            for j in range (self.size) :
                print (f"| {self.board[i][j]} ", end = "" )
            print ("|")
            print ("---------------------------------")
            
        logging.info(f"turn {self.game_count} of {self.curr_player} board printed \n")
        pass
    
    
    def is_valid_loc (self, move : tuple) :
        """
        Checks whether the given move (row, col) is valid.
        A valid coordinate must be in the range of the board.
        Inputs : move (tuple) : the localisation of the tile to be played
        Returns : boolean (True if move is valid, False otherwise)
        
        """
        if 0 <= move[0] < self.size and 0 <= move[1] < self.size :
            return True
        return False

    
    def is_move_possible (self, move : tuple, player : str) :
        """
        check if a move is possible, depending on which player is playing
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        Returns : True if the move is possible, False otherwise (tiles occupied or no tiles to flip)
        """        
        
        if move in self.occupied_tiles :
            return False
        
        elif self.tiles_to_flip (self, move, player) == [] :
            return False
        
        else :
            return True
        
        
    def tiles_to_flip (self, move : tuple, player : str) :
        """
        check the tiles to be flip, depending on the move and the player
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        Returns : the list of location (tuple) of the tiles to be flipped
        """
        
        DIR_TOT = [(-1, -1), (-1, 0), (-1, +1),
                   (0, -1),           (0, +1),
                   (+1, -1), (+1, 0), (+1, +1)]
        
        tiles_to_be_fliped = []
        
        for direction in DIR_TOT : #for each direction
            tiles_to_be_fliped_dir = []
            
            for i in range (1, self.size) :
                direction = (direction[0]*i, direction[1]*i)
                new_move_loc = (move[0] + direction[0], move[1] + direction[1])
                
                if self.is_valid_loc(new_move_loc) : #new_move inside the board
                    if self.board[new_move_loc] == " " :
                        break
                    
                    elif i == 1 and self.board[new_move_loc] == player :
                        break
                    
                    elif self.board[new_move_loc] != player and self.board[new_move_loc] != " " :
                        tiles_to_be_fliped_dir.append(new_move_loc)
                    
                    elif self.board[new_move_loc] == player :
                        tiles_to_be_fliped.extend(tiles_to_be_fliped_dir)
                        
                        logging.debug(f"turn {self.game_count} of player {self.curr_player} : tile in final direction {direction} \
                            from {move} added to the tiles to be flipped (current state : {tiles_to_be_fliped}")
                        break
                else :
                    break
                
        return tiles_to_be_fliped
    
    def place_tile (self, move : tuple, player : str) :
        """
        places the tiles on the board
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        """
        self.board [move] = player
        self.occupied_tiles.append(move)
        
        logging.info(f"turn {self.game_count} of player {self.curr_player} : tile placed at {move} ")
        pass
    
    def flip_tiles (self, move : tuple, player : str) :
        """
        flips the tiles on the board
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        """
        tiles_to_be_fliped = self.tiles_to_flip (self, move, player)
        
        if tiles_to_be_fliped != [] :
            for tile in tiles_to_be_fliped :
                self.board[tile] = player
                
            logging.debug(f"turn {self.game_count} of player {self.curr_player} : tiles localised at {tiles_to_be_fliped} fliped ! ")
        
        else :
            logging.debug(f"turn {self.game_count} of player {self.curr_player} : no tiles to be flipped ")
            pass
        
        pass
    
    def all_possible_moves (self, player : str) :
        """
        returns the list of all possible moves for a given player
        Inputs : player (str): the player who is playing
        Returns : the list of all possible moves (tuple)
        """
        possible_moves = []
        
        for i in range (self.size) :
            for j in range (self.size) :
                if self.is_move_possible ((i,j), player) :
                    possible_moves.append((i,j))
        
        return possible_moves
    


###############################################################################
#                             GAME FUNCTIONS                                  #
###############################################################################

def play (board : Board) :
    """
    lets the player play
    Inputs : board (Board object): the board on which the game is played
    Returns :
    """
    flag = True
    
    while flag :
        move = tuple(input ("Enter the coordinates of the tile you want to play (tuple format : (column index, row index)) : "))
        
        if board.is_valid_loc (move) : #the move is possible (location wise)
            
            if board.is_move_possible (move, board.curr_player) : #the move is possible (gameplay wise)
                
                board.place_tile(move, board.curr_player)
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {move} \n")
                
                board.game_count += 1
                if board.curr_player == "O" :
                    board.curr_player = "0"
                else :
                    board.curr_player = "O"
                    
        else :
            print("This move is not possible, please try again")
            logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {move} ERROR : not possible \n")
            pass
        
        if board.game_count == board.size**2 :
            flag = False
            print ("Game over !")
            logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
            pass
        
    pass


    
# def get_empty_around_tile_loc (tile) :
#     """
#     returns a list of the empty tiles around the tile given in argument

#     Inputs : tile (tkinter object): the tile around which we want to find the empty tiles
#     Returns : list of locations of the empty tiles around
#     """
#     global BUTTON_ARRAY, BOARD_SIZE
    
#     empty_around_tile = []
    
#     for col in range (tile[0]-1, tile[0]+2) :
#         for row in range (tile[1]-1, tile[1]+2) :
#             if (col >= 0 and col < BOARD_SIZE) and (row >= 0 and row < BOARD_SIZE) :
#                 if BUTTON_ARRAY[col][row].cget("bg") == "green" :
#                     empty_around_tile.append( (col,row) )
                    
#     return empty_around_tile


# def get_game_border () :
#     """
#     gets the localisations of the tiles that are on the border of the tiles already played
#     Inputs : 
#     Returns : list of the localisation of the tile that are on the border of the game
#     """
#     global BUTTON_ARRAY, COUNT, PLAYER
    
#     tiles_played = get_already_played_tiles_loc ()
#     game_tile_border = []
    
#     for tile in tiles_played :
#         empty_tiles = get_empty_around_tile_loc (tile)
#         if empty_tiles != [] :
#             game_tile_border.append(tile)    
    
#     game_tile_border = list(dict.fromkeys(game_tile_border)) # remove duplicates
    
#     logging.info(f"turn {COUNT} of player {PLAYER} : game border tiles : {game_tile_border}")
    
#     return (game_tile_border)
    

# def all_possible_moves() :
#     """
#     find all the possible moves playable by both players
#     """
#     global BUTTON_ARRAY, PLAYER
#     tiles_played = get_already_played_tiles_loc()
    
#     possible_moves_loc = []
#     if PLAYER == "White" :
#         for tile in tiles_played :
#             if BUTTON_ARRAY[tile[0]][tile[1]].cget("bg") == "White" :
#                 ######
#                 pass
                
#     else :
#         for tile in tiles_played :
#             if BUTTON_ARRAY[tile[0]][tile[1]].cget("bg") == "Black" :
#                 ######
#                 pass
                
#     pass



###############################################################################
#                           GAME SCRIPT                                      #
###############################################################################

#initialise the game
A = Board ()
A.initialise_game()
print(A)

#white player starts
B = Game (A)