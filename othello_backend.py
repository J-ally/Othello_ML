# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 2022
@author:  jaly, delpierot
"""

import logging
import numpy as np
import copy
import time
from random import randint
import matplotlib.pyplot as plt

###############################################################################
#                          LOGGING DEFINITION                                 #
###############################################################################
logging.basicConfig(level=logging.DEBUG, filename = "logs_othello_backend_debug.log", filemode = "w",
                    format = "%(asctime)s - %(levelname)s - %(message)s")


logging.basicConfig(level=logging.INFO, filename = "logs_othello_backend_info.log", filemode = "w",
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
        
        self.initialise_game()
        self.future_possible_boards = self.generate_possible_boards(self.curr_player)
        self.board_history.append(copy.deepcopy(self))
        
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
        
        self.game_count = 5
        
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
    
        new_board = copy.deepcopy(self)
        #play for the future board
        new_board.flip_tiles(move, player)
        new_board.place_tile(move, player)
        
        #updating the future board
        new_board.board_history = self.board_history + [new_board]
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
    
    
    def generate_possible_boards (self, player : str, depth : int = 1, max_depth : int = 3) :
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

      
    def evaluation_func (self):
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
        
        #Defining the strenth of the cases on the board
        strength = np.zeros((8,8))
        strength[0,] = strength[7,] = [500, -150, 30, 10, 10, 30, -150, 500]
        strength[1,] = strength[6,] = [-150, -250, 0, 0, 0, 0, -250, -150]
        strength[2,] = strength[5,] = [30, 0, 1, 2, 2, 1, 0, 30]
        strength[3,] = strength[4,] = [10, 0, 2, 16, 16, 2, 0, 10]
        
        #Use the possible boards generated above as input for the evaluation function
        if self.generate_possible_boards(self.curr_player)!= None:
            possible_boards = self.generate_possible_boards(self.curr_player)
            possible_board_evaluations = []
            
            #Creating a matrice containing different evaluation for each board possible :
            #number of pawns, mobility, sum of the boxes arranged, evaluation function (the 3rd variables weighted)
            possible_board_evaluations = np.zeros((len(possible_boards),4))
            print(possible_board_evaluations)
            for i in range(len(possible_boards)) :
                
                board_evaluated = possible_boards[i]
                print(f"the possible board examined : {board_evaluated}")

                #Counting points obtained after a move of the current player
                possible_board_evaluations[(i, 0)] = np.sum(board_evaluated.board == self.curr_player)
                
                #Counting the mobility (empty cases avalaible on the board) after a move of the current player
                possible_board_evaluations[(i, 1)] = np.sum(board_evaluated.board == " ")
                
                #initialisation of the counter of strengh value obtained (depending on cases occuped by the current player, see the matrice strengh above)
                strength_value = 0

                size = self.size

                for row in range(size):
                    for col in range(size):
                        if board_evaluated.board[(row,col)] == self.curr_player:
                            strength_value += strength[(row,col)] #sum of the strategic strength of all the player's pieces on the board
                
                possible_board_evaluations[(i, 2)] = strength_value
                
                
                #give a score weighted by the importance of each evaluation criterion according to game period
                
                #The bifining period is during the first 12 rounds
                #Score = 3 * mobility * 2 strenth * 1 * points
                if self.game_count-4 >= 12 :
                    for i in range(len(possible_board_evaluations[:, 0])):
                        possible_board_evaluations[(i, 3)] = 3* possible_board_evaluations[(i, 1)] + 2* possible_board_evaluations[(i, 2)] + possible_board_evaluations[(i, 0)]
                        
                #the middle is between the 13th stroke and 60-deep exploration
                #Score = 3 * mobility * 3 strenth * 1 * points
                elif self.game_count-4 >= 60 : #!!!- nb exploration 
                    for i in range(len(possible_board_evaluations[:, 0])):
                        possible_board_evaluations[(i, 3)] = 3* possible_board_evaluations[(i, 1)] + 3* possible_board_evaluations[(i, 2)] + possible_board_evaluations[(i, 0)]
                                                            
                #For the end period we give more importance to the points
                #Score = 1 * mobility * 2 strenth * 3 * points
                else:
                    possible_board_evaluations[(i, 3)] = 1* possible_board_evaluations[(i, 1)] + 2* possible_board_evaluations[(i, 2)] + 3*possible_board_evaluations[(i, 0)]
        else :
            possible_board_evaluations.append(self)      
    
    
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
            if board.board[(i,j)] == " " :
                pass
            elif board.board[(i,j)] == "0" :
                score = (score[0], score[1]+1)
            else :
                score = (score[0]+1, score[1])
    logging.debug (f"score calculated : {score}")
    return score


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
    start = time.time()
    count_no_possible_moves = 0
    
    while board.is_not_full() :
        
        # print(board.is_not_full(), count_no_possible_moves)
        # board.print_board()
        # print(f"#### PLAYER {board.curr_player} TURN ! #### turn {board.game_count}")
        
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
                print (f"Game over ! | Score : blanc : {score[0]}, noir : {score[1]}")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                return (board, score)
            
        else :
            current_move = moves [ randint(0, len(moves)-1) ] 
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
    print (f"Game over ! | Score : blanc : {score[0]}, noir : {score[1]}")
    # board.print_board()
    logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
    end = time.time()
    final_time_ms = round((end-start) * 10**3)
    return (board, score, final_time_ms)
    
    
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

# scores = []
# for i in range (20) :
#     A = Board ()   
#     scores.append(play_cvc_random(A))
# print(scores)

# times = [a[2] for a in scores]

# plt.plot(np.arange(20), times)
# plt.axhline(np.mean(times), color = "red")
# plt.ylabel("time (ms)")
# plt.xlabel("game")
# plt.show()



