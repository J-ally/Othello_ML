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

TURN = "White" 
COUNT = 0
BUTTON_ARRAY = np.zeros((8,8), dtype=object)

###############################################################################
#                         Game intitialisation                                #
###############################################################################

def initialise_buttons () :
    """
    initialise the buttons, and place them in an array named BUTTON_ARRAY
    """
    global BUTTON_ARRAY
    for col in range (8) :
        for row in range (8) :
            button = Button (root, text = " ", height = 3, width = 6, bg = "green",command = lambda m = f"[{col}][{row}]": where_click(m))
            BUTTON_ARRAY [col][row] = button
            logging.info(f"button {button} initialised")
    logging.info("buttons initialised \n")
    pass

def initialise_grid () :
    """
    initialise the grid of buttons, based on the array BUTTON_ARRAY
    """
    global BUTTON_ARRAY
    for row in range (8) :
        for col in range (8) :
            BUTTON_ARRAY [col][row].grid(row = row, column = col)
    logging.info("grid initialised \n")
    pass

def initialise_game () :
    """
    initialise the game (places the 4 color tiles in the middle of the board)
    """
    global BUTTON_ARRAY
    
    BUTTON_ARRAY [3][3].config(bg = "white")
    BUTTON_ARRAY [4][4].config(bg = "white")
    
    BUTTON_ARRAY [3][4].config(bg = "black")
    BUTTON_ARRAY [4][3].config(bg = "black")
    
    logging.info("game initialised \n")
    pass


###############################################################################
#                             Game Code                                       #
###############################################################################

def get_played_tiles_loc () :
    """
    returns a list of the localisation of the tiles that have been played already
    """
    global TURN, BUTTON_ARRAY, COUNT
    
    tiles_played = []
    
    for col in range (len(8)) :
        for row in range (len(8)) :
            if BUTTON_ARRAY[col][row].cget("bg") != "green" :
                tiles_played.append( [(col,row)] )
    logging.info(f"tiles played at turn {COUNT}: {tiles_played}")
    return tiles_played
    
def all_possible_moves() :
    """
    find all the possible moves playable by both players
    """
    global BUTTON_ARRAY, TURN
    tiles_played = get_played_tiles_loc()
    
    possible_moves_loc = []
    if TURN == "White" :
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
    
    
def button_click (button) :
    """
    the player play a turn (either white if TURN = "White" or black if TURN = "Black")
    which means they placed a tile on the board
    
    CLICKED takes two values : "White" or "Black"
    Args:
        button (tkinter object): a button on the board
    """
    global TURN, COUNT        
        
    if button.cget("bg") == "green" and TURN == "White" : #White turn and tile unflipped yet
        button['bg'] = "White"
        logging.info(f"player {TURN} clicked on a button at {button.grid_info().get('column')}, {button.grid_info().get('row')}")
        COUNT += 1
        TURN = "Black"
        check_end()
        
    elif button.cget("bg") == "green" and TURN == "Black": #black turn and tile unflipped yet
        button["bg"] = "Black"
        logging.info(f"player {TURN} clicked on a button at {button.grid_info().get('column')}, {button.grid_info().get('row')}")
        COUNT += 1
        TURN = "White"
        check_end()


def check_end() :
    """
    Check if the game is over
    """
    global COUNT
    
    if COUNT == 64 :
        messagebox.showinfo("Game over", "The game is over")
        logging.info("game over")
        pass
    pass


def m_to_button(m) :
    """
    convert the coordinates of a button into a tkinter object
    Input : m (string) : the coordinates of the button
    """
    global BUTTON_ARRAY
    
    m = m.replace("[", "")
    m = m.replace("]", "")
    m = ( int(m[0]), int(m[1]) )
    logging.info(f"button {BUTTON_ARRAY[m]} clicked")
    
    return BUTTON_ARRAY[m]

###############################################################################
#                           Game script                                       #
###############################################################################

initialise_buttons()
initialise_grid()
initialise_game()

#white player starts

root.mainloop()