# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 2022
@author:  jaly, delpierot, judith
"""

import logging
import numpy as np
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
    

    def __deepcopy__(self):
        """
        Replace the deepcopy method to avoid the extra calculation of deepcopy 

        Returns : new_board (Board): a new board with the same attributes as the current board
        """
        new_board = Board()
        
        #for boards gestion
        new_board.board = self.board
        new_board.future_possible_boards = self.future_possible_boards
        
        #for game gestion
        new_board.previous_moves = self.previous_moves
        new_board.game_count = self.game_count
        new_board.curr_player = self.curr_player
        
        return new_board
    
    
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

def evaluation_function(board : Board, AI_score : int, AI_player : str):
    """
    Evaluate the board for the player AI
    Inputs : board (Board object): the board on which the game is played
    Outputs : Value of the board for the current player
    """    
    evaluation_matrix =  np.zeros((board.size,board.size), dtype= int)
    
    evaluation_matrix[0,] = evaluation_matrix[7,] = [500, -150, 30, 10, 10, 30, -150, 500]
    evaluation_matrix[1,] = evaluation_matrix[6,] = [-150, -250, 0, 0, 0, 0, -250, -150]
    evaluation_matrix[2,] = evaluation_matrix[5,] = [30, 0, 1, 2, 2, 1, 0, 30]
    evaluation_matrix[3,] = evaluation_matrix[4,] = [10, 0, 2, 16, 16, 2, 0, 10] 
    
    if board.game_count <= (board.size**2-4)/3:
        value_of_the_board = np.sum(evaluation_matrix[board.board == AI_player]) - AI_score
        #print(f"{np.sum(evaluation_matrix[board.board == '0'])}-{AI_score} = {value_of_the_board}")
    else:
        value_of_the_board = np.sum(evaluation_matrix[board.board == AI_player]) + AI_score
        #print(f"{np.sum(evaluation_matrix[board.board == '0'])}+{AI_score} = {value_of_the_board}")
        pass
    return value_of_the_board


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


def play_cvc_MinMax (board : Board, depth_exploration : int) :
    """
    lets the compluter play against another computer (one using random moves, one using AI)
    Only one board is used to play !
    Inputs : board (Board object): the board on which the game is played
            depth_exploration (int): the depth the AI explores the game to play
    Returns : board (Board object), score , final_time_ms
    """
    start = time.time()
    count_no_possible_moves = 0
    AI_MinMax_player = ['0', 'O'][randint(0,1)]
    print(f'AI plays : {AI_MinMax_player}')
    
    while board.is_not_full() :
        
        # print(board.is_not_full(), count_no_possible_moves)
        board.print_board()
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
            
            if count_no_possible_moves > 3 : #to prevent infinite loop
                score = calculate_score(board)
                if AI_MinMax_player == '0':
                    print (f"Game over ! | Score : blanc : {score[0]}, noir (IA) : {score[1]}")
                else:
                    print (f"Game over ! | Score : blanc (IA) : {score[0]}, noir : {score[1]}")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                return (board, score)
            
        else :
            if board.curr_player != AI_MinMax_player: #Random is playing
                current_move = moves [ randint(0, len(moves)-1) ] 
                logging.info(f"turn {board.game_count} of random player {board.curr_player} : move {current_move} entered")
            
            else: #The minmax AI is playing
                board.print_board()
                current_move = MinMax(board.__deepcopy__(), depth_exploration)
                logging.info(f"turn {board.game_count} of AI minmax player {board.curr_player} : move {current_move} entered")
            
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
                
                print(current_move)
                
            else :
                print("This move is not possible, please try again")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tile at {current_move} is out of the board")
                pass
    
    score = calculate_score(board)
    if AI_MinMax_player == '0':
        print (f"Game over ! | Score : blanc : {score[0]}, noir (IA) : {score[1]}")
    else:
        print (f"Game over ! | Score : blanc (IA) : {score[0]}, noir : {score[1]}")
    # board.print_board()
    logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
    end = time.time()
    final_time_ms = round((end-start) * 10**3)
    return (board, score, final_time_ms)


###############################################################################
#                        GAME DECISION AGLGORITHMS                            #
###############################################################################

############# MINMAX #############

def leaf_evaluation(possible_boards : list, depth : int, AI_player : str):
    """
    Calculates the value of a list of positions: 
    The maximum for the AI, the minimum for the adverse of the AI
    Inputs : A list of boards to be evaluated  (possible_boards)
                and the depth_exploration (depth)
    Returns : The extremal value of the position (node_value : int) 
    """
    
    value_leaf = []
    
    for leaf in possible_boards:
        white_score, black_score = calculate_score(leaf)
        AI_score = black_score if AI_player == '0' else white_score
        value_leaf.append(evaluation_function(leaf, AI_score, AI_player))
    node_value = max(value_leaf) if depth%2 == 0 else min(value_leaf)
    
    """if depth%2 == 0:
        print('MAX')
    else:
        print('MIN')"""
        
    return node_value



def recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value, to_explore, AI_player):
    """
    Calculates the value of one move by recursion for the AI with the MinMax algorithm.
    Inputs :  - historic_boards : list of boards    (list of previous nodes in the tree)
              - possible_moves : list of tuple      (next moves possible from the last node of historic_boards)
              - possible_boards : list of boards    (next boards possible from the last node of historic_boards)
              - depth : int                         (current depth of the nodes of possible_boards)
              - depth_exploration : int             (choosen depth to explore each time AI plays)
              - node_value : list of int            (list of the value of the node explored)
              - to_explore : list of int            (list of the number of nodes to explore for each depth of the currant branch)
              - AI_player : str                     (color of the AI)
    Returns : The value of the possibles moves (node_value : list)
                and the possibles moves in the same order (next_possible_moves : list)
    """
    Adverse_player = '0' if AI_player == 'O' else 'O'
    
    if depth <= 1 :
        return node_value
    
    else:
        
        if to_explore[depth] >= 0:
        #Descendant case : the nodes of the current depth are not all explored 
            
            if depth < depth_exploration and possible_moves != None:
            #The next nodes are not leaves, then they are to be explored
            #Then generate the next noes to be evaluated
                #print('\npm : ' , possible_moves)
                #print('Non explore avant', depth, to_explore[depth], historic_boards, node_value)
                player = AI_player if depth%2 == 0 else Adverse_player
                #print( 'NEXT PLAYER :', player)
                #print('depth :', depth, 'TO_EXPLORE list :', to_explore, 'len(pb) :', len(possible_boards))
                #print(possible_boards)
                sub_board = possible_boards[to_explore[depth]]
                historic_boards.append(sub_board.__deepcopy__())
                #sub_board.print_board()
                possible_boards = sub_board.generate_possible_boards(player)
                possible_moves = sub_board.generate_all_possible_moves(player)
                to_explore.append(len(possible_boards)-1)
                #print('TO_EXPLORE list :', to_explore)
                depth += 1
                #print('Non explore apres', depth, to_explore[depth-1], sub_board, historic_boards, node_value)
                return recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value, to_explore, AI_player)
            
            elif depth < depth_exploration and possible_moves == None:
            #The next nodes are not leaves, but no move possible for the player
            #Go to the next depth
                historic_boards.extend(possible_boards)
                to_explore.append(len(possible_boards)-1)
                depth += 1
                return recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value, to_explore, AI_player)
            
            else:
            #The next nodes are leaves
            #Then calculates the value of the node
            #Then go back to explore the previous depth
                #depth == depth_exploration or possible_moves == None:
                #print('\npm : ', possible_moves)
                #print('Feuille avant',depth, to_explore[depth-1], historic_boards, node_value)
                node_value.append(leaf_evaluation(possible_boards, depth, AI_player))           
                depth -= 2
                to_explore[depth+1] -= 1
                player = AI_player if depth%2 == 0 else Adverse_player
                #print(historic_boards[depth])
                possible_boards = historic_boards[depth].generate_possible_boards(player)
                possible_moves = historic_boards[depth].generate_all_possible_moves(player)
                historic_boards = historic_boards[:depth+1]
                to_explore = to_explore[:depth+2]
                #print('TO_EXPLORE list :', to_explore)
                #print('Feuille apres', depth, to_explore[depth], historic_boards, node_value, '\n')
                #print('\nNEXT PB', possible_boards)
                depth += 1
                return recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value, to_explore, AI_player)
        
        
        else : 
        #Ascendant case : the nodes of the current depth are all explored 
        #Then calculates the value of the node
        #Then go back to explore the previous depth
            #if to_explore[depth] < 0:
            #print('\nTo explore avant', depth, to_explore[depth], historic_boards, node_value)
            node_value = [max(node_value)] if depth%2 == 0 else [min(node_value)]
            depth -= 2
            to_explore[depth+1] -= 1
            player = AI_player if depth%2 == 0 else Adverse_player
            #print(historic_boards[depth])
            #historic_boards[depth].print_board()
            possible_boards = historic_boards[depth].generate_possible_boards(player)
            possible_moves = historic_boards[depth].generate_all_possible_moves(player)
            historic_boards = historic_boards[:depth+1] 
            to_explore = to_explore[:depth+2]
            #print('To explore apres', depth, to_explore[depth], historic_boards, node_value)
            depth += 1
            return recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value, to_explore, AI_player)



def MinMax(board : Board, depth_exploration : int):
    """
    Calculates the value of the next possible moves for the AI with the MinMax algorithm.
    Inputs : The current game board 
                and the depth of exploration
    Returns : The move of maximum value for AI for the next turn (move_of_max_value : tuple)
    """
    print('# --------- #\nMinMax')
    AI_player = board.curr_player
    Adverse_player = '0' if AI_player == 'O' else 'O'
    
    depth = 0
    player = AI_player if depth%2 == 0 else Adverse_player
    next_possible_moves = board.generate_all_possible_moves(player)
    board.print_board()
    possible_moves = next_possible_moves.copy() if next_possible_moves != None else None
    
    board_copy = board.__deepcopy__()    
    possible_boards_depth1 = board_copy.generate_possible_boards(player)
    board.print_board()

    node_value = [[] for index_sub_board in range(len(next_possible_moves))]
    #print(possible_moves)
    
    for index_sub_board in range(len(next_possible_moves)):
        
        depth = 1
        historic_boards = [board]
        to_explore = [1,1]
        print(f'\n\n##########Move {index_sub_board}############\n---------{next_possible_moves[index_sub_board]}---------')
        possible_boards_depth1[index_sub_board].print_board()
        historic_boards.append(possible_boards_depth1[index_sub_board])
        player = AI_player if depth%2 == 0 else Adverse_player
        #print(f"PLAYER : {player}")
        possible_boards = possible_boards_depth1[index_sub_board].generate_possible_boards(player)
        possible_moves = possible_boards_depth1[index_sub_board].generate_all_possible_moves(player)
        to_explore.append(len(possible_boards)-1)
        depth = 2
        
        node_val = recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value[index_sub_board], to_explore, AI_player)
        node_value[index_sub_board] = node_val[0]
        
    move_of_max_value = next_possible_moves[np.argmax(node_value)] #Can be empty if no possible move
        
    return move_of_max_value



############# MCTS #############

class MCTS (Board) :
    def __init__ (self, board : Board) :
        pass
    
    # main function for the Monte Carlo Tree Search
    # def monte_carlo_tree_search(root):
        
    #     while resources_left(time, computational power):
    #         leaf = traverse(root)
    #         simulation_result = rollout(leaf)
    #         backpropagate(leaf, simulation_result)
            
    #     return best_child(root)

    # # function for node traversal
    # def traverse(node):
    #     while fully_expanded(node):
    #         node = best_uct(node)
            
    #     # in case no children are present / node is terminal
    #     return pick_unvisited(node.children) or node

    # # function for the result of the simulation
    # def rollout(node):
    #     while non_terminal(node):
    #         node = rollout_policy(node)
    #     return result(node)

    # # function for randomly selecting a child node
    # def rollout_policy(node):
    #     return pick_random(node.children)

    # # function for backpropagation
    # def backpropagate(node, result):
    #     if is_root(node) return
    #     node.stats = update_stats(node, result)
    #     backpropagate(node.parent)

    # # function for selecting the best child
    # # node with highest number of visits
    # def best_child(node):
    #     pick child with highest number of visits


    

###############################################################################
#                           GAME SCRIPT                                      #
###############################################################################

# scores = []
# for i in range (200) :
#     A = Board ()   
#     scores.append(play_cvc_random(A))
# print(scores)

# times = []
# for i in range (len(scores)) :
#     try :
#         times.append(scores[i][2])
#     except :
#         pass

# plt.plot(np.arange(200), times)
# plt.axhline(np.mean(times), color = "red")
# plt.ylabel("time (ms)")
# plt.xlabel("game")
# plt.show()

A = Board ()
A.initialise_game()
a = play_cvc_MinMax(A, 2)