# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 2022
@author:  jaly
"""

import logging
import numpy as np
from tkinter import *
from tkinter import messagebox

###############################################################################
#                          logging definition                                 #
###############################################################################

logging.basicConfig(level=logging.INFO, filename = "logs_othello.log", filemode = "w",
                    format = "%(asctime)s - %(levelname)s - %(message)s")

###############################################################################
#                           Define root                                       #
###############################################################################

root = Tk()
root.title("Othello") 

###############################################################################
#                               Globals                                       #
###############################################################################

BOARD_SIZE = 8
PLAYER = "White" 
COUNT = 1
BUTTON_ARRAY = np.zeros((BOARD_SIZE,BOARD_SIZE), dtype=object)

###############################################################################
#                         Game intitialisation                                #
###############################################################################


def initialise_buttons () :
    """
    initialise the buttons, and place them in an array named BUTTON_ARRAY
    Inputs :
    Returns :
    """
    global BUTTON_ARRAY, BOARD_SIZE
    
    for col in range (BOARD_SIZE) :
        for row in range (BOARD_SIZE) :
            button = Button (root, text = " ", height = 3, width = 6, bg = "green",command = lambda m = f"[{col}][{row}]": where_click(m))
            BUTTON_ARRAY [col][row] = button
            logging.info(f"button {button} initialised")
    
    logging.info("buttons initialised \n")
    
    pass


def initialise_grid () :
    """
    initialise the grid of buttons, based on the array BUTTON_ARRAY
    Inputs :
    Returns :
    """
    global BUTTON_ARRAY, BOARD_SIZE
    
    for row in range (BOARD_SIZE) :
        for col in range (BOARD_SIZE) :
            BUTTON_ARRAY [col][row].grid(row = row, column = col)
    
    logging.info("grid initialised \n")
    
    pass


def initialise_game () :
    """
    initialise the game (places the 4 color tiles in the middle of the board)
    Inputs : 
    Returns :
    """
    global BUTTON_ARRAY, BOARD_SIZE
    
    middle_1, middle_2 = (BOARD_SIZE-1)//2, ((BOARD_SIZE-1)//2) + 1
    BUTTON_ARRAY [middle_1][middle_1].config(bg = "white")
    BUTTON_ARRAY [middle_2][middle_2].config(bg = "white")
    
    BUTTON_ARRAY [middle_1][middle_2].config(bg = "black")
    BUTTON_ARRAY [middle_2][middle_1].config(bg = "black")
    
    logging.info(f"the size of the of the game : {BOARD_SIZE}")
    logging.info(f"game initialised with middle_1 = {middle_1} and middle_2 = {middle_2}\n")
    
    pass


###############################################################################
#                             Game Code                                       #
###############################################################################


def get_already_played_tiles_loc () :
    """
    gets the localisation of the tiles that have been played already
    Inputs :
    Returns : a list of the localisation of the tiles that have been played already
    """
    global PLAYER, BUTTON_ARRAY, COUNT
    
    tiles_played = []
    
    for col in range (BOARD_SIZE) :
        for row in range (BOARD_SIZE) :
            if BUTTON_ARRAY[col][row].cget("bg") != "green" :
                tiles_played.append( (col,row) )
                
    logging.info(f"turn {COUNT} of player {PLAYER} : loc of the tiles played already : {tiles_played}")
    
    return tiles_played

def get_empty_around_tile(tile) :
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
        empty_tiles = get_empty_around_tile(tile)
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


def where_click(m) :
    """
    find the button corresponding to the click of the player
    Input : m (string) : the coordinates of the button
    """
    button_clicked = m_to_button(m)
    button_click(button_clicked)
    
    pass
    

def check_end() :
    """
    Check if the game is over
    """
    global COUNT
    
    if COUNT == 64 :
        messagebox.showinfo("Game over", "The game is over")
        logging.info("GAAAAME OVER")
        pass
    pass


def m_to_button(m) :
    """
    convert the coordinates of a button into a tkinter object
    
    Input : m (string) : the coordinates of the button
    Returns : the tkinter object corresponding to the button
    """
    global BUTTON_ARRAY
    
    m = m.replace("[", "")
    m = m.replace("]", "")
    m = ( int(m[0]), int(m[1]) )
    
    logging.info(f"turn {COUNT} of player {PLAYER} : {BUTTON_ARRAY[m]} has been clicked")
    
    return BUTTON_ARRAY[m]


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
#                           Game script                                       #
###############################################################################

initialise_buttons()
initialise_grid()
initialise_game()

#white player starts

while COUNT < 64 :
    button_click()
    root.mainloop()