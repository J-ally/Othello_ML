# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 2022
@author:  jaly
"""

import logging
import numpy as np
import copy


###############################################################################
#                          LOGGING DEFINITION                                 #
###############################################################################

logging.basicConfig(level=logging.DEBUG, filename = "logs_othello_backend.log", filemode = "w",
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
   
        
    def generate_tiles_to_be_flipped (self, move : tuple, player : str) :
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
            logging.debug(f"turn {self.game_count} of player {self.curr_player} : current direction {direction} ")
            
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
                        
                        logging.debug(f"   turn {self.game_count} of player {self.curr_player} : tile in final direction {direction} from {move} added to the tiles to be flipped (current state : {tiles_to_be_fliped}")
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
        
        logging.debug(f"turn {self.game_count} of player {self.curr_player} : tile placed at {move} ")
        pass
    
    
    def flip_tiles (self, move : tuple, player : str) :
        """
        flips the tiles on the board
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        Returns : tiles_to_be_flipped (list) : the list of tiles to be flipped    
        """
        tiles_to_be_fliped = self.generate_tiles_to_be_flipped (move, player)
        
        if tiles_to_be_fliped != [] :
            for tile in tiles_to_be_fliped :
                self.board[tile] = player
                
            logging.debug(f"turn {self.game_count} of player {self.curr_player} : tiles localised at {tiles_to_be_fliped} fliped ! ")
        
        else :
            logging.debug(f"turn {self.game_count} of player {self.curr_player} : no tiles to be flipped ")
            pass
        
        return tiles_to_be_fliped
    
    
    def generate_all_possible_moves (self, player : str) :
        """
        returns the list of all possible moves for a given player
        Inputs : player (str): the player who is playing
        Returns : the list of all possible moves (tuple)
        """
        possible_moves = []
        
        for i in range (self.size) :
            for j in range (self.size) :
                if self.generate_tiles_to_be_flipped((i,j), player) != [] :
                    possible_moves.append((i,j))
                    
        logging.debug(f"turn {self.game_count} of player {self.curr_player} : all possible moves generated : {possible_moves} ")
        return possible_moves
    
    
    def generate_possible_boards (self, player : str) :
        """
        returns the list of all possible boards for a given player
        Inputs : player (str): the player who is playing
        Returns : the list of all possible boards (list of boards)
        """
        possible_boards = []
        
        for move in self.generate_all_possible_moves(player) :
            possible_boards.append(self.generate_board_after_move(move, player))
            
        logging.debug(f"turn {self.game_count} of player {self.curr_player} : all possible boards generated : {possible_boards} ")
        return possible_boards
    
    
    def generate_board_after_move (self, move : tuple, player : str) :
        
    
        """
        returns the board after a move has been played
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        Returns : the board after the move has been played (Board)
        """
        new_board = copy.deepcopy(self)
        
        new_board.place_tile(move, player)
        new_board.flip_tiles(move, player)
        
        logging.debug(f"turn {self.game_count} of player {self.curr_player} : board after move {move} generated : {new_board} ")
        return new_board

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
        board.print_board()
        print(f"#### PLAYER {board.curr_player} TURN ! ####")
        move = str(input ("Enter the coordinates of the tile you want to play (tuple format : (row_index,col_index)) : "))
        move = (int(move[1]), int(move[3]))
        logging.info(f"turn {board.game_count} of player {board.curr_player} : move {move} entered")
        
        if board.is_valid_loc (move) : #the move is possible (location wise)
            logging.debug(f"turn {board.game_count} of player {board.curr_player} : move {move} is valid (location wise)")
            
            tiles_to_be_fliped = board.flip_tiles(move, board.curr_player)
            logging.info(f"turn {board.game_count} of player {board.curr_player} : tiles fliped : {tiles_to_be_fliped}")
            
            if tiles_to_be_fliped != [] : #the move is possible (gameplay wise)
                
                board.place_tile(move, board.curr_player)
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {move} \n")
                
                board.game_count += 1
                if board.curr_player == "O" :
                    board.curr_player = "0"
                else :
                    board.curr_player = "O"
            
            else :
                print("This move is not possible, please try again")
                logging.debug(f"turn {board.game_count} of player {board.curr_player} : tile placed at {move} already occupied or no tiles to be flipped")
                pass
        
        else :
            print("This move is not possible, please try again")
            logging.debug(f"turn {board.game_count} of player {board.curr_player} : tile at {move} is out of the board")
            pass
        
        if board.game_count == board.size**2 :
            flag = False
            print ("Game over !")
            logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
            pass
        
    pass


###############################################################################
#                           GAME SCRIPT                                      #
###############################################################################

#initialise the game
A = Board ()
A.initialise_game()

possibles = A.generate_possible_boards("O")

for possible in possibles :
    
    possible.print_board()
    print("\n")
