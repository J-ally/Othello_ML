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

COUNT = 1
PLAYER = "White"

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
    frontier = []
    
    def __init__ (self, size = 8) :
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
            
        logging.info(f"turn {COUNT} of {PLAYER} board printed \n")
        pass


###############################################################################
#                             Game Code                                       #
###############################################################################

class Game (Board) :
    
    def __init__ (self) :
        """
        initialises the game
        Args:
        """
        pass
    
    
    def play (self) :
        """
        lets the player play
        Inputs :
        Returns :
        """
        global COUNT
        global PLAYER
       
        while True :
            move = tuple(input ("Enter the coordinates of the tile you want to play (tuple format) : "))
            if is_move_possible (move, PLAYER) :
                place_tile(move, PLAYER)
                COUNT += 1
                
                logging.info(f"turn {COUNT} of player {PLAYER} : tile placed at {move} \n")
            else :
                print("This move is not possible, please try again")
                pass
            
        pass
    
    def is_move_possible (self, move, player) :
        """
        check if a move is possible, depending on the player
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        Returns : True if the move is possible, False otherwise

        """        
        if move in self.occupied_tiles :
            return False
        
        ####### Has to be updated #######
        if player == "White" :
            if self.board[move[0]][move[1]] == "0" :
                return True
            else :
                return False
        else :
            if self.board[move[0]][move[1]] == "O" :
                return True
            else :
                return False
        
        pass
           
def get_empty_around_tile_loc (tile) :
    """
    returns a list of the empty tiles around the tile given in argument

    Inputs : tile (tkinter object): the tile around which we want to find the empty tiles
    Returns : list of locations of the empty tiles around
    """
    global BUTTON_ARRAY, BOARD_SIZE
    
    empty_around_tile = []
    
    for col in range (tile[0]-1, tile[0]+2) :
        for row in range (tile[1]-1, tile[1]+2) :
            if (col >= 0 and col < BOARD_SIZE) and (row >= 0 and row < BOARD_SIZE) :
                if BUTTON_ARRAY[col][row].cget("bg") == "green" :
                    empty_around_tile.append( (col,row) )
                    
    return empty_around_tile


def get_game_border () :
    """
    gets the localisations of the tiles that are on the border of the tiles already played
    Inputs : 
    Returns : list of the localisation of the tile that are on the border of the game
    """
    global BUTTON_ARRAY, COUNT, PLAYER
    
    tiles_played = get_already_played_tiles_loc ()
    game_tile_border = []
    
    for tile in tiles_played :
        empty_tiles = get_empty_around_tile_loc (tile)
        if empty_tiles != [] :
            game_tile_border.append(tile)    
    
    game_tile_border = list(dict.fromkeys(game_tile_border)) # remove duplicates
    
    logging.info(f"turn {COUNT} of player {PLAYER} : game border tiles : {game_tile_border}")
    
    return (game_tile_border)
    

def all_possible_moves() :
    """
    find all the possible moves playable by both players
    """
    global BUTTON_ARRAY, PLAYER
    tiles_played = get_already_played_tiles_loc()
    
    possible_moves_loc = []
    if PLAYER == "White" :
        for tile in tiles_played :
            if BUTTON_ARRAY[tile[0]][tile[1]].cget("bg") == "White" :
                ######
                pass
                
    else :
        for tile in tiles_played :
            if BUTTON_ARRAY[tile[0]][tile[1]].cget("bg") == "Black" :
                ######
                pass
                
    pass


def player_turn() :
    """
    player plays the game (places a tile)
    """
    
    pass


###############################################################################
#                            Utilities                                        #
###############################################################################

def check_end() :
    """
    Check if the game is over
    """
    global COUNT
    
    if COUNT == 64 :
        print("Game over, The game is over")
        logging.info("GAAAAME OVER")
        pass
    pass


###############################################################################
#                            Turn Script                                      #
###############################################################################


def button_click (button) :
    """
    the player play a turn (either white if PLAYER = "White" or black if PLAYER = "Black")
    which means they placed a tile on the board
    
    CLICKED takes two values : "White" or "Black"
    
    Args: button (tkinter object): a button on the board
    Inputs :
    Returns :
    """
    global PLAYER, COUNT        
    
    #first turn
    all_possible_moves = get_game_border()
        
    if button.cget("bg") == "green" and PLAYER == "White" : #White turn and tile unflipped yet
        button['bg'] = "White"
        logging.info(f"turn {COUNT} of player {PLAYER} : clicked on a button at ({button.grid_info().get('column')}, {button.grid_info().get('row')})")
        COUNT += 1
        PLAYER = "Black"
        check_end()
        
    elif button.cget("bg") == "green" and PLAYER == "Black": #black turn and tile unflipped yet
        button["bg"] = "Black"
        logging.info(f"turn {COUNT} of player {PLAYER} : clicked on a button at ({button.grid_info().get('column')}, {button.grid_info().get('row')})")
        COUNT += 1
        PLAYER = "White"
        check_end()
    
    pass

###############################################################################
#                           GAME SCRIPT                                      #
###############################################################################

#initialise the game
A = Board ()
A.initialise_game()
#white player starts
B = Game (A)