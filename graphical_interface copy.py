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
#                               Game code                                     #
###############################################################################

def initialise_buttons () :
    """
    initialise the buttons, and place them in an array named BUTTON_ARRAY
    """
    global BUTTON_ARRAY
    
    button1 = Button (root, text = " ", height = 3, width = 6, bg = "green", command = lambda : button_click(button1))
    BUTTON_ARRAY [0][1] = button1
    BUTTON_ARRAY [0][1].grid(row = 0, column = 1)
    logging.info("button 1 initialised")
    
    button2 = Button (root, text = " ", height = 3, width = 6, bg = "green", command = lambda : button_click(button2))
    BUTTON_ARRAY [0][2] = button2
    BUTTON_ARRAY [0][2].grid(row = 0, column = 2)
    logging.info("button 2 initialised")
    
    button3 = Button (root, text = " ", height = 3, width = 6, bg = "green", command = lambda : button_click(button3))
    BUTTON_ARRAY [0][3] = button3
    BUTTON_ARRAY [0][3].grid(row = 0, column = 3)
    logging.info("button 3 initialised")
    
    button4 = Button (root, text = " ", height = 3, width = 6, bg = "green", command = lambda : button_click(button4))
    BUTTON_ARRAY [0][4] = button4
    BUTTON_ARRAY [0][4].grid(row = 0, column = 4)
    logging.info("button 4 initialised")
    
    button5 = Button (root, text = " ", height = 3, width = 6, bg = "green", command = lambda : button_click(button5))
    BUTTON_ARRAY [0][5] = button5
    BUTTON_ARRAY [0][5].grid(row = 0, column = 5)
    logging.info("button 5 initialised")
    
    button6 = Button (root, text = " ", height = 3, width = 6, bg = "green", command = lambda : button_click(button6))
    BUTTON_ARRAY [0][6] = button6
    BUTTON_ARRAY [0][6].grid(row = 0, column = 6)
    logging.info("button 6 initialised")
    
    button7= Button (root, text = " ", height = 3, width = 6, bg = "green", command = lambda : button_click(button7))
    BUTTON_ARRAY [0][7] = button7
    BUTTON_ARRAY [0][7].grid(row = 0, column = 7)
    logging.info("button 1 initialised")
    
    button8 = 

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
    
    logging.info("game initialised")
    pass

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
        logging.info(f"player {TURN} clicked on a button at {button.grid_info().get('row')}, {button.grid_info().get('column')}, button named  {button.grid_info().get('in')}")
        COUNT += 1
        TURN = "Black"
        check_end()
        
    elif button.cget("bg") == "green" and TURN == "Black": #black turn and tile unflipped yet
        button["bg"] = "Black"
        logging.info(f"player {TURN} clicked on a button at {button.grid_info().get('row')}, {button.grid_info().get('column')}, button named  {button.grid_info().get('in')}")
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
    print("checked win")
    pass

###############################################################################
#                           Game script                                       #
###############################################################################

initialise_buttons()
initialise_game()

#white player starts

root.mainloop()