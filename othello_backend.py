# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 2022
@author:  jaly
"""

import logging
import numpy as np
import copy
from random import randint

###############################################################################
#                          LOGGING DEFINITION                                 #
###############################################################################

logging.basicConfig(level=logging.INFO, filename = "logs_othello_backend.log", filemode = "w",
                    format = "%(asctime)s - %(levelname)s - %(message)s")

###############################################################################
#                         GAME INITIALISATION                                #
###############################################################################

class Board () :
    """
    The board is a numpy array of size 8x8. Each cell contains a string.
    O represents a white tile
    0 represents a black tile
    """
    
    previous_moves = {"O" : [], "0" : []}
    board_history = []
    
    occupied_tiles = []
    
    future_possible_boards = []
    
    game_count = 0 #the number of turn played
    
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
        
        #move gestion
        self.occupied_tiles = [(middle_1,middle_1), (middle_1,middle_2),(middle_2,middle_2), (middle_2,middle_1)]
        self.previous_moves["O"] = [(middle_1,middle_1), (middle_2,middle_2)]
        self.previous_moves["0"] = [(middle_1,middle_2), (middle_2,middle_1)]
        
        self.game_count = 4
        self.board_history.append(copy.deepcopy(self))
        self.future_possible_boards = self.generate_possible_boards(self.curr_player)
        
        logging.info(f"game initialised with middle_1 = {middle_1} and middle_2 = {middle_2}\n")
        pass
    
    
    def print_board (self, ecart : int = 0) :
        """
        print the board in the console
        Inputs : ecart (int) : the number of empty caracteres to print before the board
        Returns :
        """
        print (" "*ecart + "| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 ||||| \n" + " "*ecart + "-------------------------------------")
        for i in range (self.size) :
            print(" "*ecart, end="")
            for j in range (self.size) :
                print (f"| {self.board[i][j]} ", end = "" )
            print (f"| {i}")
            print (" "*ecart + "-------------------------------------")
        print("\n")
            
        logging.debug(f"turn {self.game_count} of {self.curr_player} board printed \n")
        pass
    
    
    def is_valid_loc (self, move : tuple) :
        """
        Checks whether the given move (row, col) is valid.
        A valid coordinate must be in the range of the board.
        Inputs : move (tuple) : the localisation of the tile to be played
        Returns : boolean (True if move is valid, False otherwise)
        
        """
        if 0 <= move[0] < self.size and 0 <= move[1] < self.size :
            #logging.debug(f"turn {self.game_count} of player {self.curr_player} : move {move} is valid (location wise)")
            return True
        #logging.debug(f"turn {self.game_count} of player {self.curr_player} : move {move} is NOT valid (location wise)")
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
            #logging.debug(f"turn {self.game_count} of player {self.curr_player} : current direction {direction} ")
            
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
        places the tiles on the board, updates the occupied tiles and the moves played
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
                if self.generate_tiles_to_be_flipped((i,j), player) != [] and self.board[(i,j)] == " " :
                    possible_moves.append((i,j))
                else :
                    pass
        
        if possible_moves == [] :
            logging.debug(f"turn {self.game_count} of player {self.curr_player} : no possible moves for player {player}")
            return None
                   
        logging.debug(f"turn {self.game_count} of player {self.curr_player} : all possible moves generated : {possible_moves} ")
        return possible_moves
    
    
    def generate_board_after_move (self, move : tuple, player : str) :
        """
        returns the board after a move has been played, and updates the following attributesof the future board :
            - occupied_tiles
            - player 
            - game_count
            - board history 
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        Returns : the board after the move has been played (Board)
        """
    
        new_board = copy.deepcopy(self)
        #play for the future board
        new_board.place_tile(move, player)
        new_board.flip_tiles(move, player)
        
        #updating the future board
        new_board.board_history = self.board_history + [new_board]
        
        if self.curr_player == "0":
            curr_player = self.curr_player
            not_curr_player = "O"
            new_board.previous_moves = {"O" :self.previous_moves[not_curr_player], "0" : self.previous_moves[curr_player] + [move]}
        else :
            curr_player = "O"
            not_curr_player = self.curr_player
            new_board.previous_moves = {"O" :self.previous_moves[curr_player] + [move], "0" : self.previous_moves[not_curr_player]}
        
        if self.curr_player == "0" : 
            new_board.curr_player = "O"
        else :
            new_board.curr_player = "0"
        
        new_board.game_count = self.game_count + 1
        
        logging.debug(f"turn {self.game_count} of player {self.curr_player} : board after move {move} generated : {new_board} ")
        return new_board
    
    
    def generate_possible_boards (self, player : str) :
        """
        returns the list of all possible boards for a given player
        Inputs : player (str): the player who is playing
        Returns : the list of all possible boards (list of boards)
        """

        possible_boards = []
        
        if self.generate_all_possible_moves(player) != None :
            for move in self.generate_all_possible_moves(player) :
                
                possible_boards.append(self.generate_board_after_move(move, player))
    
        else :
            possible_boards.append(self)
            
        logging.debug(f"turn {self.game_count} of player {self.curr_player} : all possible boards generated : {possible_boards} ")
        return possible_boards
    

###############################################################################
#                             GAME FUNCTIONS                                  #
###############################################################################

def calculate_score (board : Board) :
    """
    calculates the score of the game
    Inputs : board (Board object): the board on which the game is played
    Returns : the score of the game (tuple : (white_score, black_score))
    """
    score = (0,0)
    
    for i in range (board.size) :
        for j in range (board.size) :
            if board.board[(i,j)] == "" :
                pass
            elif board.board[(i,j)] == "0" :
                score = (score[0], score[1]+1)
            else :
                score = (score[0]+1, score[1])
    logging.debug (f"score calculated : {score}")
    return score


def generate_all_possible_boards (board : Board, final_depth : int = 2, local_depth : int = 0) :
    """
    Generates all possible boards for a given board, for a given depth using a tail recursion
    
    Args:board (Board): a board instance
         final_depth (int, optional): the number of turns anticipated. Defaults to 4.
         local_depth (int, optional): the current depth of the recursion. Defaults to 0.
    """
    
    for j in range (len(board.future_possible_boards)) : #loop for the number of boards in the possible board list of the board
        future_board = board.future_possible_boards[j]
   
        logging.debug(f"turn {board.game_count} of player {board.curr_player} : all possible boards generated for {future_board}, depth = {local_depth} : \n  ")
        
        while int(local_depth )< int(final_depth) :
            generate_all_possible_boards(future_board, final_depth, local_depth +1)
    

# print(A.print_board())
# for i in range (len(possibles)) :
#     possibles[i].print_board(4)
#     print("\n ")
    
#     #possible moves for the second turn
#     possibles_2 = possibles[i].generate_possible_boards("0")
#     for j in range (len(possibles_2)) :
#         possibles_2[j].print_board(8)
#         print("\n ")
        
#         #possible moves for the third turn
#         possibles_3 = possibles_2[j].generate_possible_boards("O")
#         for k in range (len(possibles_3)) :
#             possibles_3[k].print_board(12)
#             print("\n ")
        
#     print("\n")

###############################################################################
#                               GAME MODES                                    #
###############################################################################

def play_cvc_random (board : Board) :
    """
    lets the compluter play against another computer (both using random moves)
    Only one board is used to play !
    Inputs : board (Board object): the board on which the game is played
    Returns :
    """
    flag = True
    
    while flag :
        board.print_board()
        
        print(f"#### PLAYER {board.curr_player} TURN ! #### turn {board.game_count}")
        
        move = board.generate_all_possible_moves(board.curr_player)
        
        if move == None : #no possible moves for the player
            logging.info(f"turn {board.game_count} of player {board.curr_player} : tile not placed ! No possible moves \n")
            
            board.game_count += 0
            if board.curr_player == "O" :
                board.curr_player = "0"
            else :
                board.curr_player = "O"
            pass
                
            if board.game_count == (board.size**2) : #end of the game
                flag = False
                print ("Game over !")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                break
        
        else :
            move = move[ randint(0, len(move)-1) ]          
            logging.info(f"turn {board.game_count} of player {board.curr_player} : move {move} entered")
            
            if board.is_valid_loc (move) : #the move is possible (location wise)
                
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
                    logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {move} already occupied or no tiles to be flipped")
                    pass
            
            elif board.game_count == (board.size**2)-4 : #end of the game
                flag = False
                print ("Game over !")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                pass
            
            else :
                print("This move is not possible, please try again")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tile at {move} is out of the board")
                pass
            
    pass

def play_pvp (board : Board) :
    """
    lets the player play against another player
    Only one board is used to play !
    Inputs : board (Board object): the board on which the game is played
    Returns :
    """
    flag = True
    
    while flag :
        board.print_board()
        
        print(f"#### PLAYER {board.curr_player} TURN ! #### turn {board.game_count}")
        
        move = str(input ("Enter the coordinates of the tile you want to play (tuple format : (row_index,col_index)) : "))
        
        if move == "pass" : #no possible moves for the player
            board.game_count += 0
            if board.curr_player == "O" :
                board.curr_player = "0"
            else :
                board.curr_player = "O"
            pass 
        
        else : 
            move = (int(move[1]), int(move[3]))
            
            logging.info(f"turn {board.game_count} of player {board.curr_player} : move {move} entered")
            
            if board.is_valid_loc (move) : #the move is possible (location wise)
                
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
                    logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {move} already occupied or no tiles to be flipped")
                    pass
            
            else :
                print("This move is not possible, please try again")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tile at {move} is out of the board")
                pass
            
            if board.game_count == (board.size**2) : #end of the game
                flag = False
                print ("Game over !")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                pass
            
    pass

def play_pvc_minmax (board : Board) :
    """
    lets a player play against  computer (using minmax algorithm)
    Inputs : board (Board object): the board on which the game is played
    Returns :

    Args:
        board (Board): _description_
    """


###############################################################################
#                        GAME DECISION AGLGORITHMS                            #
###############################################################################



###############################################################################
#                           GAME SCRIPT                                      #
###############################################################################

#initialise the game
A = Board ()
A.initialise_game()

# for i in range (len(A.future_possible_boards)) :
#     A.future_possible_boards[i].print_board() #possible moves after for the first turn

# print(f"le board history de A = {A.board_history}")
# print(f"le previous move de A : {A.previous_moves}")

# print(A.game_count)
# for i in range (len(A.board_history)) :
#     A.board_history[i].print_board()

# B_list = A.generate_possible_boards( A.curr_player)
# print(f"the list of possible boards : {B_list}")
# B_list[0].print_board()

# print(f"le board history est {B_list[0].board_history}")
# print(f"le previous move est {B_list[0].previous_moves}")
# print(f"la joueur jouant est {B_list[0].curr_player}")
# print(f"le nombre de coups joués est {B_list[0].game_count}")


# C_list = B_list[0].generate_possible_boards( B_list[0].curr_player)
# print(f"the list of possible boards : {C_list}")
# C_list[0].print_board()

# print(f"le board history est {C_list[0].board_history}")
# print(f"le previous move est {C_list[0].previous_moves}")
# print(f"la joueur jouant est {C_list[0].curr_player}")
# print(f"le nombre de coups joués est {C_list[0].game_count}")

# print(f"le board history de A = {A.board_history}")
# print(f"le previous move de A : {A.previous_moves}")

generate_all_possible_boards(A, A.curr_player)