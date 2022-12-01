# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 2022
@author:  jaly
"""

import logging
import numpy as np
import copy
import time
import math
from random import randint
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(1000000000)

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
        
        self.initialise_game()
        
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
        self.previous_moves["O"] = [(middle_1,middle_1), (middle_2,middle_2)]
        self.previous_moves["0"] = [(middle_1,middle_2), (middle_2,middle_1)]
        
        #board history gestion
        self.game_count = 4
        
        logging.info(f"game initialised with middle_1 = {middle_1} and middle_2 = {middle_2}\n")
        pass

    def __deepcopy__(self):
        """
        Replace the deepcopy method to avoid the extra calculation of deepcopy 

        Returns : new_board (Board): a new board with the same attributes as the current board
        """
        new_board = Board()
        
        #for boards gestion
        new_board.board = copy.copy(self.board)
        
        #for game gestion
        new_board.previous_moves = copy.copy(self.previous_moves)
        new_board.game_count = copy.copy(self.game_count)
        new_board.curr_player = copy.copy(self.curr_player)
        return new_board
    
    
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
            
        logging.debug(f"turn {self.game_count} of {self.curr_player} board printed : {id(self)}\n")
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
                curr_direction = (direction[0]*i, direction[1]*i) #increment of one tile for each direction
                new_move_loc = (move[0] + curr_direction[0], move[1] + curr_direction[1])
                
                if self.is_valid_loc(new_move_loc) : #new_move inside the board
                    if self.board[new_move_loc] == " " :
                        break
                    
                    elif i == 1 and self.board[new_move_loc] == player :
                        break
                    
                    elif self.board[new_move_loc] != player and self.board[new_move_loc] != " " :
                        tiles_to_be_fliped_dir.append(new_move_loc)
                    
                    elif self.board[new_move_loc] == player :
                        tiles_to_be_fliped.extend(tiles_to_be_fliped_dir)
                        break
                else :
                    break
                
        logging.debug(f"   turn {self.game_count} of player {self.curr_player} : tiles to be flipped : {tiles_to_be_fliped}")
        return tiles_to_be_fliped
    
    
    def place_tile (self, move : tuple, player : str) :
        """
        places the tiles on the board, updates the occupied tiles and the moves played
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        """
        self.board [move] = player
        
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
                
            logging.debug(f"turn {self.game_count} of player {self.curr_player} : tiles {tiles_to_be_fliped} fliped ! ")
        
        else :
            logging.debug(f"turn {self.game_count} of player {self.curr_player} : no tiles to be flipped ")
            pass
        
        return tiles_to_be_fliped
    
    
    def generate_all_possible_moves (self, player : str) :
        """
        returns the list of all possible moves for a given player
        Inputs : player (str): the player who is playing
        Returns : the list of all possible moves (tuple) or None if the list is empty
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
        returns the board after a move has been played, and updates the following attributes of the future board :
            - player 
            - game_count
            - board history 
            
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        Returns : the board after the move has been played (Board)
        """
    
        new_board = self.__deepcopy__()
        #play for the future board
        new_board.flip_tiles(move, player)
        new_board.place_tile(move, player)
        
        #updating the future board
        new_board.game_count = self.game_count + 1
        
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
        
        logging.debug(f"turn {self.game_count} of player {self.curr_player} : board after move {move} generated : {new_board} ")
        return new_board
    
    
    def generate_possible_boards (self, player) :
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
        
        # while max_depth > depth :
        #     for i in range (len(possible_boards)) :
        #         possible_boards[i].future_possible_boards = possible_boards[i].generate_possible_boards(possible_boards[i].curr_player)
        
        logging.debug(f"turn {self.game_count} of player {self.curr_player} : all possible boards generated : {possible_boards} ")
        return possible_boards

        
    
    def is_not_full (self) :
        """
        checks is the board is full or not
        Inputs :
        Returns: True if it's not full, False if it's full (no empty case)
        """
        arr = np.where(self.board == " ")
        if len(arr[0]) == 0 and len(arr[1]) == 0 :
            return False
        else :
            return True
        
    def evaluation_func(self, depth_max):
        """
        Lets writh an evaluation function that use as criteria :
            -the mobility (blank case available)
            -the position strengh (depending of positions on the board)
            -the number of point
        Giving score calculated with the 3 parameters above and weighted
        by the importance of each evaluation criterion according to
        the period in the game (beginning, middle and end)
        !!! the way to weighted each value need to be rethinck 
        """

        if depth_max%2 == 0:
            current_player = self.curr_player
        else:
            logging.info(f"depth_max : {depth_max}. Is not a multiple of 2, we don't need to put the evaluation function at the advantage of the initial player! \n")
            if self.curr_player == "0":
                current_player = "O"
            else:
                current_player = "0"
        
        #Defining the strenth of the cases on the board
        strength = np.zeros((8,8))
        strength[0,] = strength[7,] = [500, -150, 30, 10, 10, 30, -150, 500]
        strength[1,] = strength[6,] = [-150, -250, 0, 0, 0, 0, -250, -150]
        strength[2,] = strength[5,] = [30, 0, 1, 2, 2, 1, 0, 30]
        strength[3,] = strength[4,] = [10, 0, 2, 16, 16, 2, 0, 10]
        
        board_evaluated = self
        nb_points = np.sum(board_evaluated.board == current_player)
        mobility = np.sum(board_evaluated.board == " ")
        

        strength_value = 0
        size = self.size
        for row in range(size):
            for col in range(size):
                if board_evaluated.board[(row,col)] == current_player:
                           strength_value += strength[(row,col)]
        value = 0
        if board_evaluated.game_count-4 >= 12 :
            value = 3* mobility + 2* strength_value + nb_points
        elif board_evaluated.game_count-4 >= 60:
            value = 3* mobility + 3* strength_value + nb_points
        else:
            value = mobility + 2* strength_value + 3* nb_points
            
        return value
    
            
    def alpha_value (self, depth, depth_max, alpha, beta):
        
        if depth == depth_max:
            logging.info(f"Actual depth : {depth} is the maximal depth. So it's a leaf! \n")
            alpha = self.evaluation_func(depth_max)
            return alpha
        else:
            pass
        
        alpha = -math.inf
        
        if depth < depth_max:
            logging.info(f"Actual depth : {depth}. So it's possible to generate boards from this actual board! \n")
            for node in self.generate_possible_boards(self.curr_player):
                depth += 1
                beta = node.beta_value(depth, depth_max, alpha, beta)
                alpha = max(alpha, beta)
                
                if alpha >= beta:
                    logging.info(f"{alpha} is superior or equal to {beta}. So lpha take the value of beta. This an alpha pruning! \n")
                    return alpha
        
        return alpha
    
    
    def beta_value (self, depth, depth_max, alpha, beta):
        
        if depth == depth_max:
            logging.info(f"Actual depth : {depth} is the maximal depth. So it's a leaf! \n")
            beta = self.evaluation_func(depth_max)
            return beta
        else:
            pass
        
        beta = math.inf
        
        if depth < depth_max:
            logging.info(f"Actual depth : {depth} is not the maxiaml depth. So it's possible to generate boards from this board! \n")
            for node in self.generate_possible_boards(self.curr_player):
                depth += 1
                alpha = node.alpha_value(depth, depth_max, alpha, beta)
                beta = min(beta, alpha)
                
                if alpha <= beta:
                    logging.info(f"{beta} is inferior or equal to {alpha}. So beta take the value of alpha. This an beta pruning! \n")
                    return beta
        else:
            pass
        
        return beta
    
    def alpha_beta(self, depth_max):

        alpha = -math.inf
        beta = math.inf
        best_val = alpha
        
        best_node = None
        best_move = None
        
        if self.game_count - depth_max > 59:
            logging.info(f"Maximal depth become :{depth_max}. You can't generate more depth than you had remaining parts! \n")
            depth_max = 64 - self.game_count
        else:
            pass
        
        depth = 0
        if depth < depth_max:
            logging.info(f"Initial depth : {depth} is inferior to the depth max. It's possible to generate boards from the current board! \n")
            depth += 1
            nodes = self.generate_possible_boards(self.curr_player)
            moves = self.generate_all_possible_moves(self.curr_player)
            for node in nodes:
                value = node.alpha_value(depth, depth_max, alpha, beta)
                if value >= best_val:
                    best_val = value
                    best_node = node
                    if best_node != None:
                        best_move = moves[nodes.index(best_node)]
                    else:
                        best_move = None
        else:
            pass
        
        return best_node, best_move
        
            

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


def end_of_the_game (white_score : int, black_score : int) :
    if white_score < black_score:
        print (f"Game over ! Black win ({black_score})")
    elif white_score > black_score:
        print (f"Game over ! White win ({white_score})")
    else:
        print (f"Game over ! The game is a draw ({white_score})")
        pass

def who_win (score : tuple) :
        if score[0] < score[1] :
            return "black"
        elif score[0] == score[1] :
            return "egalite"
        else :
            return "white"

def play_cvc_alpha_beta_white (board : Board, depth_max : int) :
    """
    lets the compluter play with alpha beta function, the another computer
    chose is move randomly
    Only one board is used to play !
    Inputs : board (Board object): the board on which the game is played
             depth_max (int) : the max depth
    Returns : the score, a list with the time took by the alpha_beta funtion for each turn
    """
    start = time.time()
    count_no_possible_moves = 0
    
    while board.is_not_full() :
        
        moves = board.generate_all_possible_moves(board.curr_player)
        logging.info(f"turn {board.game_count} of player {board.curr_player} :     moves possible {moves} ")
        
        if moves == None : #no possible moves for the player
            logging.info(f"turn {board.game_count} of player {board.curr_player} : tile not placed ! No possible moves \n")
            
            count_no_possible_moves += 1
            board.game_count += 0
            if board.curr_player == "O" :
                board.curr_player = "0"
            else :
                board.curr_player = "O"
            
            if count_no_possible_moves > 15 : #to prevent infinite loop
                score = calculate_score(board)
                #print (f"Game over ! | Score : blanc : {score[0]}, noir : {score[1]}")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                return (board, score)
            
        else :
            if board.curr_player == "O":
               current_move = board.alpha_beta(depth_max)[1] #alpha beta for white
            else :
                current_move = moves[randint(0, len(moves)-1)] #random for black

            logging.info(f"turn {board.game_count} of player {board.curr_player} : move {current_move} entered")
            
            if board.is_valid_loc (current_move) : #the move is possible (location wise)
                
                tiles_to_be_fliped = board.flip_tiles(current_move, board.curr_player)
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tiles fliped : {tiles_to_be_fliped}")
                
                if tiles_to_be_fliped != [] : #the move is possible (gameplay wise)
                    
                    board.place_tile(current_move, board.curr_player)
                    logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {current_move} \n")
                    
                    board.game_count += 1
                    if board.curr_player == "O" :
                        board.curr_player = "0"
                    else :
                        board.curr_player = "O"
                
                else :
                    logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {current_move} already occupied or no tiles to be flipped")
                    pass
            
            else :
                print("This move is not possible, please try again")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tile at {current_move} is out of the board")
                pass
    
    score = calculate_score(board)
    #print (f"Game over ! | Score : blanc : {score[0]}, noir : {score[1]}")
    # board.print_board()
    logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
    end = time.time()
    final_time_ms = round((end-start) * 10**3)
    return (board, score, final_time_ms)
scores = []
for i in range(200):
    A = Board ()
    scores.append(play_cvc_alpha_beta_white(A,3))

times = []
white_w = 0
black_w = 0
for i in range (len(scores)) :
    try :
        times.append(scores[i][2])
    except :
        pass
    
    if who_win(scores[i][1]) == "white" :
            white_w += 1
    elif who_win(scores[i][1]) == "black" :
            black_w += 1
    else :
            white_w += 0.5
            black_w += 0.5

print(white_w, black_w, white_w/(black_w+white_w))
