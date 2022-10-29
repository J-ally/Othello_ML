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
#                                GLOBALS                                      #
###############################################################################

PLAYER = "White" 
COUNT = 1

###############################################################################
#                                GAME MECH                                    #
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

