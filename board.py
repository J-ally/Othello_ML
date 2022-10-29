# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 2022
@author:  jaly
"""

import logging
import numpy as np
from tkinter import *
from tkinter import messagebox

import game

###############################################################################
#                         LOGGING DEFINITION                                  #
###############################################################################

logging.basicConfig(level=logging.INFO, filename = "logs_othello_board.log", filemode = "w",
                    format = "%(asctime)s - %(levelname)s - %(message)s", datefmt='%H:%M:%S')


###############################################################################
#                             ROOT DEFINITION                                 #
###############################################################################

root = Tk()
root.title("Othello") 


###############################################################################
#                              GLOBALS                                  #
###############################################################################

PLAYER = "White" 
COUNT = 1


###############################################################################
#                          class definition                                   #
###############################################################################

class Board :
    
    """
    Definition of the tile and initialisation of the board
    
    """
    
    tiles_already_played = []
    empty_border_game = []
    
    def __init__(self, size = 8, root = root) :
        """
        Initialisation of the board
        Args: 
            size (int, optional): The size of the board (number of squares). Defaults to 8.
        """
        self.size = size
        self.initialise_buttons(root)
        self.initialise_grid()
        pass
    
    
    def initialise_buttons (self, root = root) :
        """
        initialises the buttons, and places them in an class array named button_array
        Inputs :
        Returns :
        """
        self.button_array = np.zeros((self.size, self.size), dtype = object)
        
        for col in range (self.size) :
            for row in range (self.size) :
                button = Button (root, text = " ", height = 3, width = 6, bg = "green",command = lambda m = f"[{col}][{row}]": self.where_click(m))
                button.pack()
                self.button_array [col][row] = button
                logging.debug(f"button {button} has been created")
        logging.info("buttons initialised \n")
        
        pass
    
    
    def initialise_grid (self) :
        """
        initialise the grid of buttons, based on the array BUTTON_ARRAY
        Inputs :
        Returns :
        """
        
        for row in range (self.size) :
            for col in range (self.size) :
                self.button_array [col][row].grid(row = row, column = col)
        
        logging.info("grid initialised \n")
        
        pass

    
    def where_click(self, m) :
        """
        find the button corresponding to the click of the player
        Input : m (string) : the coordinates of the button
        """
        button_clicked = self.m_to_button(m)
        game.button_click(button_clicked)
        
        pass


    def m_to_button(self, m) :
        """
        convert the coordinates of a button into a tkinter object
        
        Input : m (string) : the coordinates of the button
        Returns : the tkinter object corresponding to the button
        """
        
        m = m.replace("[", "")
        m = m.replace("]", "")
        m = ( int(m[0]), int(m[1]) )
        
        logging.info(f"turn {COUNT} of player {PLAYER} : {self.button_array[m]} has been clicked")
        
        return self.button_array[m]

###############################################################################
#                             BOARD CREATION                                  #
###############################################################################

def board_creation() :
    """
    """
    return (Board(size = 8))
    
###############################################################################
#                             BOARD LOOP                                      #
###############################################################################

board_creation ()

root.mainloop()