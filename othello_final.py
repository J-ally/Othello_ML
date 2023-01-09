# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 2022
@author:  jaly, deplierrot, judith
"""

import logging
import copy
import time
import math
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from random import randint
from numpy import mean
from tqdm import tqdm

sys.setrecursionlimit(1000000000)

###############################################################################
#                          LOGGING DEFINITION                                 #
###############################################################################

# logging.basicConfig(level=logging.INFO, filename = "logs_othello_backend_info.log", filemode = "w",
#                     format = "%(asctime)s - %(levelname)s - %(message)s")

# logging.basicConfig(level=logging.DEBUG, filename = "logs_othello_backend_debug.log", filemode = "w",
#                     format = "%(asctime)s - %(levelname)s - %(message)s")

###############################################################################
#                         GAME INITIALISATION                                 #
###############################################################################


class Board () :
    """
    The board is a numpy array of size 8x8. Each cell contains a string.
    O represents a white tile
    0 represents a black tile
    """
    
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
        self.moves_history = []
        self.initialise_game()
        
        # logging.info(f"the size of the of the game : {self.size} \n")
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
        self.moves_history.append(["O", (middle_1,middle_1)])
        self.moves_history.append(["O", (middle_2,middle_2)])
        self.moves_history.append(["0", (middle_1,middle_2)])
        self.moves_history.append(["0", (middle_2,middle_1)])
        
        #board history gestion
        self.game_count = 4
        
        # logging.info(f"game initialised with middle_1 = {middle_1} and middle_2 = {middle_2}\n")
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
        new_board.moves_history = copy.copy(self.moves_history)
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
            
        # logging.debug(f"turn {self.game_count} of {self.curr_player} board printed : {id(self)}\n")
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
                    if self.board[new_move_loc] == " " : #empty tile nearby
                        break
                    
                    elif i == 1 and self.board[new_move_loc] == player : #same color tile nearby
                        break
                    
                    elif self.board[new_move_loc] != player and self.board[new_move_loc] != " " :
                        #empty tile after a tile from the opposite color
                        tiles_to_be_fliped_dir.append(new_move_loc)
                    
                    elif self.board[new_move_loc] == player :
                        tiles_to_be_fliped.extend(tiles_to_be_fliped_dir)
                        break
                else :
                    break
                
        # logging.debug(f"   turn {self.game_count} of player {self.curr_player} : tiles to be flipped : {tiles_to_be_fliped}")
        return tiles_to_be_fliped
    
    
    def place_tile (self, move : tuple, player : str) :
        """
        places the tiles on the board, updates the occupied tiles and the moves played
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        """
        self.board [move] = player
        
        # logging.debug(f"turn {self.game_count} of player {self.curr_player} : tile placed at {move} ")
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
                
            # logging.debug(f"turn {self.game_count} of player {self.curr_player} : tiles {tiles_to_be_fliped} fliped ! ")
        
        else :
            # logging.debug(f"turn {self.game_count} of player {self.curr_player} : no tiles to be flipped ")
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
            # logging.debug(f"turn {self.game_count} of player {self.curr_player} : no possible moves for player {player}")
            return None
                   
        # logging.debug(f"turn {self.game_count} of player {self.curr_player} : all possible moves generated : {possible_moves} ")
        return possible_moves
    
        
    def generate_board_after_move (self, move : tuple, player : str) :
        """
        returns the board after a move has been played, and updates the following attributes of the future board :
            - player 
            - game_count
            - board history 
            - moves_history
            
        Inputs : move (tuple): the localisation of the tile to be played
                 player (str): the player who is playing
        Returns : the board after the move has been played (Board)
        """
    
        new_board = self.__deepcopy__()
        #play for the future board
        new_board.flip_tiles(move, player)
        new_board.place_tile(move, player)
        new_board.moves_history.append([player, move])
        
        #updating the future board
        new_board.game_count = self.game_count + 1
        
        if self.curr_player == "0":
            new_board.curr_player = "O"
        else :
            new_board.curr_player = "0"

        # logging.debug(f"turn {self.game_count} of player {self.curr_player} : board after move {move} generated : {new_board} ")
        return new_board
    
    
    def generate_possible_boards (self, player) :
        """
        returns the list of all possible boards for a given player
        Inputs : player (str): the player who is playing
        Returns : the list of all possible boards (list of boards) or an empty list if no move is possible
        """        
        possible_boards = []
    
        if self.generate_all_possible_moves(player) != None :
            for move in self.generate_all_possible_moves(player) :
                possible_boards.append(self.generate_board_after_move(move, player))
        else :
            possible_boards.append(self)
        
        # logging.debug(f"turn {self.game_count} of player {self.curr_player} : all possible boards generated : {possible_boards} ")
        return possible_boards


    def generate_possible_boards_MCTS (self, player) :
        """
        returns the list of all possible boards for a given player
        Inputs : player (str): the player who is playing
        Returns : the list of all possible boards (list of boards) or an empty list if no move is possible
        """        
        possible_boards = []
    
        if self.generate_all_possible_moves(player) != None :
            for move in self.generate_all_possible_moves(player) :
                possible_boards.append(self.generate_board_after_move(move, player))
        
        # logging.debug(f"turn {self.game_count} of player {self.curr_player} : all possible boards generated : {possible_boards} ")
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
    # logging.debug (f"score calculated : {score}")
    return score


def who_win (score:tuple, AI: str) :
    if score[0] > score[1]: #score blanc > score noir
        winner = 'AI' if AI == 'O' else 'Random'
    elif score[0] < score[1]:
        winner = 'AI' if AI == '0' else 'Random'
    else: #score blanc = score noir : it's a draw
        winner = 'Egalite'
    return winner 


def evaluation_function(board : Board, score : int, player : str):
    """
    Evaluate the board for the player AI
    Inputs : board (Board object): the board on which the game is played
    Outputs : Value of the board for the current player
    """    
    evaluation_matrix =  np.zeros((board.size,board.size), dtype= int)
    
    evaluation_matrix[0,] = evaluation_matrix[7,] = [150, -50, 13, 8, 8, 13, -50, 150]
    evaluation_matrix[1,] = evaluation_matrix[6,] = [-50, -80, 0, 0, 0, 0, -80, -50]
    evaluation_matrix[2,] = evaluation_matrix[5,] = [13, 0, 1, 2, 2, 1, 0, 13]
    evaluation_matrix[3,] = evaluation_matrix[4,] = [5, 0, 2, 8, 8, 2, 0, 5]
    
    if board.game_count <= (board.size**2-4)/3:
        value_of_the_board = np.sum(evaluation_matrix[board.board == player]) - score
        #print(f"{np.sum(evaluation_matrix[board.board == '0'])}-{AI_score} = {value_of_the_board}")
    else:
        value_of_the_board = np.sum(evaluation_matrix[board.board == player]) + score
        #print(f"{np.sum(evaluation_matrix[board.board == '0'])}+{AI_score} = {value_of_the_board}")
        pass
    return value_of_the_board


###############################################################################
#                        ALPHA BETA ALGO FUNCTIONS                            #
###############################################################################

def Alpha_Beta(board:Board, AI_player:str, depth:int, depth_max:int, alpha:float, beta:float):

    if board.curr_player == "O":
        player = "0"
    else:
        player = "O"

    #Evaluation if the board is a leaf or it's the end of the game or there is no one can play
    if depth == depth_max or board.game_count == 64 or board.generate_possible_boards(board.curr_player) == None and board.generate_possible_boards(player)== None:
        if AI_player == "O":
            score = calculate_score(board)[0]
        else:
            score = calculate_score(board)[1]
        value = evaluation_function(board, score, AI_player)
    
    else:
        depth += 1

        if board.generate_possible_boards(board.curr_player) == None:
            board_list = board.generate_possible_boards(board.curr_player)
        else:
            board_list = board.generate_possible_boards(player)

        for board in board_list:
            if board.curr_player == AI_player:
                value = -math.inf

                value = max(value, Alpha_Beta(board, AI_player, depth, depth_max, alpha, beta))
                alpha = max(value, alpha)
                if beta <= alpha:
                    break
            else:
                value = math.inf
                
                value = min(value, Alpha_Beta(board, AI_player, depth, depth_max, alpha, beta))
                beta = min(value, beta)
                if beta <= alpha:
                    break
    return value
    
def Best_Move (board:Board, AI_player:str, depth_max:int):
    beta = math.inf
    best_value = -math.inf
    best_node = None
    best_move = None

    depth = 0
    depth += 1

    moves = board.generate_all_possible_moves(board.curr_player)

    boards_list = board.generate_possible_boards(board.curr_player)
    if boards_list != None:
        for board in boards_list:
            value = Alpha_Beta(board, AI_player, depth, depth_max, best_value, beta)

            if value >= best_value:
                best_value = value
                best_board = board
                best_move = moves[boards_list.index(best_board)]
    else:
        return (0,0)
    return best_move


###############################################################################
#                          MIN MAX ALGO FUNCTIONS                             #
###############################################################################


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
    node_value = max(value_leaf) if (depth-1)%2 == 0 else min(value_leaf)
        
    return node_value


def recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value, to_explore, AI_player):
    """
    Calculates the value of one move by recursion for the AI with the move_Min_Max algorithm.
    Inputs :  - historic_boards : list of boards    (list of previous nodes in the tree)
            - possible_moves : list of tuple      (next moves possible from the last node of historic_boards)
            - possible_boards : list of boards    (next boards possible from the last node of historic_boards)
            - depth : int                         (current depth of the nodes of possible_boards)
            - depth_exploration : int             (choosen depth to explore each time AI plays)
            - node_value : list of list of int    (list of the value of the node explored)
            - to_explore : list of int            (list of the number of nodes to explore for each depth of the currant branch)
            - AI_player : str                     (color of the AI)
    Returns : The value of the possibles moves (node_value : list)
                and the possibles moves in the same order (next_possible_moves : list)
    """
    Adverse_player = '0' if AI_player == 'O' else 'O'
    
    if depth <= 1 :
        return node_value[depth]
    
    else:
        
        if to_explore[depth] >= 0:
        #Descendant case : the nodes of the current depth are not all explored 
            
            if depth < depth_exploration and possible_moves != None:
            #The next nodes are not leaves, then they are to be explored
            #Then generate the next noes to be evaluated
                player = AI_player if depth%2 == 0 else Adverse_player
                sub_board = possible_boards[to_explore[depth]]
                historic_boards.append(sub_board)
                possible_boards = sub_board.generate_possible_boards(player)
                possible_moves = sub_board.generate_all_possible_moves(player)
                to_explore.append(len(possible_boards)-1)
                node_value.append([])
                depth += 1
                return recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value, to_explore, AI_player)
            
            elif depth < depth_exploration and possible_moves == None:
            #The next nodes are not leaves, but no move possible for the player
            #Go to the next depth
                historic_boards.extend(possible_boards)
                to_explore.append(len(possible_boards)-1)
                node_value.append([])
                depth += 1
                return recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value, to_explore, AI_player)
            
            else:
            #The next nodes are leaves
            #Then calculates the value of the node
            #Then go back to explore the previous depth
                node_value[depth-1].append(leaf_evaluation(possible_boards, depth, AI_player))           
                depth -= 2
                to_explore[depth+1] -= 1
                player = AI_player if depth%2 == 0 else Adverse_player
                possible_boards = historic_boards[depth].generate_possible_boards(player)
                possible_moves = historic_boards[depth].generate_all_possible_moves(player)
                historic_boards = historic_boards[:depth+1]
                to_explore = to_explore[:depth+2]
                node_value = node_value[:depth+2]
                depth += 1
                return recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value, to_explore, AI_player)
        
        
        else : 
        #Ascendant case : the nodes of the current depth are all explored 
        #Then calculates the value of the node
        #Then go back to explore the previous depth
            node_value[depth-1].append(max(node_value[depth]) if (depth-1)%2 == 0 else min(node_value[depth]))
            depth -= 2
            to_explore[depth+1] -= 1
            player = AI_player if depth%2 == 0 else Adverse_player
            possible_boards = historic_boards[depth].generate_possible_boards(player)
            possible_moves = historic_boards[depth].generate_all_possible_moves(player)
            historic_boards = historic_boards[:depth+1] 
            to_explore = to_explore[:depth+2]
            node_value = node_value[:depth+2]
            depth += 1
            return recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, node_value, to_explore, AI_player)


def move_Min_Max(board : Board, depth_exploration : int):
    """
    Calculates the value of the next possible moves for the AI with the move_Min_Max algorithm.
    Inputs : The current game board 
                and the depth of exploration
    Returns : The move of maximum value for AI for the next turn (move_of_max_value : tuple)
    """
    AI_player = board.curr_player
    Adverse_player = '0' if AI_player == 'O' else 'O'
    
    depth = 0
    player = AI_player if depth%2 == 0 else Adverse_player
    next_possible_moves = board.generate_all_possible_moves(player)
    possible_moves = next_possible_moves.copy() if next_possible_moves != None else None
    
    possible_boards_depth1 = board.generate_possible_boards(player)

    nodes_values = [[[]] for index_sub_board in range(len(next_possible_moves))]
    
    if depth_exploration == 1:
        
        value_leaf = []
    
        for leaf in possible_boards_depth1:
            white_score, black_score = calculate_score(leaf)
            AI_score = black_score if AI_player == '0' else white_score
            value_leaf.append(evaluation_function(leaf, AI_score, AI_player))
            
        move_of_max_value = next_possible_moves[np.argmax(value_leaf)]
    
    else:
    
        for index_sub_board in range(len(next_possible_moves)):
            
            depth = 1
            historic_boards = [board]
            to_explore = [1,1]
            historic_boards.append(possible_boards_depth1[index_sub_board])
            player = AI_player if depth%2 == 0 else Adverse_player
            possible_boards = possible_boards_depth1[index_sub_board].generate_possible_boards(player)
            possible_moves = possible_boards_depth1[index_sub_board].generate_all_possible_moves(player)
            to_explore.append(len(possible_boards)-1)
            nodes_values[index_sub_board].append([])
            depth = 2
            
            node_val = recursion_MinMax(historic_boards, possible_moves, possible_boards, depth, depth_exploration, nodes_values[index_sub_board], to_explore, AI_player)
            nodes_values[index_sub_board] = node_val[0]
            
        move_of_max_value = next_possible_moves[np.argmax(nodes_values)] #Can be empty if no possible move
        
    return move_of_max_value


###############################################################################
#                          MCTS ALGO FUNCTIONS                             #
###############################################################################

class MCTS_Node :   
        
    def __init__(self, board : Board, parent , \
                       win_count : int = 0, UCT_score : float = 0, nb_visit : int = 0 ) -> None:
        self.board = board.__deepcopy__()
        self.UCT_score = UCT_score
        self.nb_visit = nb_visit
        self.parent = parent
        self.win_count = win_count
        self.children = []
        self.move = None
        pass
    
    
    def generate_children(self) -> list:
        """
        Get the children of the current node (the possible moves) in a node list
        Inputs :
        Returns : the list of children nodes
        """
        possible_boards = self.board.generate_possible_boards(self.board.curr_player)
        possible_moves = self.board.generate_all_possible_moves(self.board.curr_player)
        
        children = []
        for i in range (len(possible_boards)):
            # possible_boards[i].print_board()
            # print(possible_boards[i].curr_player)
            children.append(MCTS_Node(possible_boards[i], self))
            children[i].move = possible_moves[i]
        return children
        
        
    def play_random_from_node(self, ai_player : str, print_output : bool) -> None:
        """
        Play a random game from the current node
        Inputs : ai_player : the player that will be played by the AI
        Returns : updates the score of the node as well as the number of visits
        """
        # initial_player = self.board.curr_player
        # print(f"initial player : {initial_player}")
        output_game = play_FAST_random_vs_random (self.board, print_output)
        score = output_game[2]
        # print(score, score[0], score[1])
        # print(type(initial_player))
        self.nb_visit += 1
        if ai_player == "0" and score[0] < score[1] : #black wins
            self.win_count += 1
        elif ai_player == "O" and score[0] > score[1] : #white wins
            self.win_count += 1
        # output_game = None
        return output_game

    
    def calc_UCT_score (self, nb_exploration : int, index_child : int) -> None:
        """
        calculates and updates the UCT score of the current node
        Inputs : nb_exploration (int) : number of exploration rounds
                 index_child (int) : index of the child node that has been visited
        Returns : updates the score of the node
        """
        child = self.children[index_child]
        child.UCT_score += (child.win_count / child.nb_visit) + 2*(math.sqrt( math.log(nb_exploration) / child.nb_visit))
        # print(f"child {index_child} ; visit {child.nb_visit} ; score : {child.UCT_score} ; win_count : {child.win_count}")
        pass
    
        
    def choose_child_node_index (self) :
        """
        chooses a node to expand (max UCT score)
        Inputs :
        Returns : the index of the node to expand in the list of children
        """
        # index_node = 0
        child_score = []
        for child in self.children :
            child_score.append(child.UCT_score)
        # print(child_score)
        if 0 in child_score :
            return child_score.index(0)
        else :
            return np.argmax(child_score)
    
    
def move_MCTS (node : MCTS_Node, nb_rounds : int, ai_player : str, print_output : bool, save_party : bool) -> None:
    """
    Play one iteration game with MCTS
    Inputs : board : Board, 
             nb_rounds : int
             ai_player : str
    Returns : The board choosen for the simulation
    """
    if save_party :
        two_d_array = []
    node.children = node.generate_children()
    # print(f"current node {node.board}")
    # print(f"children {node.children}")
    for round in tqdm (range (1, nb_rounds + 1,1), desc= "Calculation one turn ") :
        # print(f"round {round}")
        exploration_node = node.children[node.choose_child_node_index()]
        # exploration_node.board.print_board()     
        if save_party : 
            two_d_array.append(exploration_node.play_random_from_node(ai_player, print_output))
        else :
            exploration_node.play_random_from_node(ai_player, print_output)
        node.calc_UCT_score(nb_rounds, node.children.index(exploration_node))
        # print("\n")
        
    final_node = node.children[node.choose_child_node_index()]
    
    if save_party : 
        df = pd.DataFrame(two_d_array, columns = ["Game type", "AI player", "final score", "play duration", "moves played"])
        now = int( time.time() )
        df.to_csv(f"Dataframes/{now}_games_data_mcts_generated.csv", index=False)
    
    return final_node.move


def play_FAST_random_vs_random (board_init : Board, print_output : bool) -> list:
    """
    Lets the computer play against another computer (both using random moves)
    Only one board is used to play
    Inputs : board (Board object): the board on which the game is played
             print_output (bool): choose if the board is printed after each party
    Returns : (final board, score : (tuple : (white_score, black_score)), time for the party to be played)
    """
    start = time.time()
    count_no_possible_moves = 0
    board = board_init.__deepcopy__()

    while board.is_not_full() :

        moves = board.generate_all_possible_moves(board.curr_player)

        if moves == None : #no possible moves for the player
            count_no_possible_moves += 1
            if board.curr_player == "O" :
                board.curr_player = "0"
            else :
                board.curr_player = "O"
            
            if count_no_possible_moves > 3 : #to prevent infinite loop
                score = calculate_score(board)
                if print_output :
                    print (f"Simulation over ! | Score : blanc : {score[0]}, noir : {score[1]}")
                end = time.time()
                final_time_ms = round((end-start) * 10**3)
                return ([f"random vs random", None, score, final_time_ms, board.moves_history])
            
        else : #some moves are possible 
            current_move = moves [ randint(0, len(moves)-1) ] 
            board.flip_tiles(current_move, board.curr_player)

            #for next turn
            board.place_tile(current_move, board.curr_player)
            board.game_count += 1
            board.moves_history.append([board.curr_player, current_move])
        
            if board.curr_player == "O" :
                board.curr_player = "0"
            else :
                board.curr_player = "O"

    score = calculate_score(board)
    if print_output :
        print (f"Simulation over ! | Score : blanc : {score[0]}, noir : {score[1]}")
    # board.print_board()
    end = time.time()
    final_time_ms = round((end-start) * 10**3)
    return ["random vs random", None, score, final_time_ms, board.moves_history]


###############################################################################
#                          PLAYING FUNCTIONS                                  #
###############################################################################

def play_FAST_othello (board_init : Board, AI_type : str, player_type : str, depth : int, nb_simulations : int = 500, print_output : bool = False ) :
    """ 
    play all types of games (AI vs AI or AI vs player or player vs player or random vs random)
    Only one board is used to play ! (but not returned at the end)
    Inputs : board_init (Board object): the board on which the game is played
             AI_type (str) : the type of AI that will be played
                    can be "random", "min_max", "alpha_beta", "mcts", "human"
             player_type (str) : the type of player that will be played
                    can be "random", "min_max", "alpha_beta", "mcts", "human"
             depth (int) : the depth of the search tree for the AI (needed for min max and alpha beta)
    Returns : [f"{AI_type} vs {player_type}", AI_player, score, final_time_ms, board.moves_history]
    """
    start = time.time()
    count_no_possible_moves = 0
    
    board = board_init.__deepcopy__()

    if AI_type == "random" or AI_type == "human" :
        AI_player = None
    else : 
        position = randint(0,1)
        AI_player = ['0', 'O'][position]
        
    while board.is_not_full() :
    
        moves = board.generate_all_possible_moves(board.curr_player)
        # print("moves possible", moves)
        if moves == None : #no possible moves for the player
            
            count_no_possible_moves += 1
            if board.curr_player == "O" :
                board.curr_player = "0"
            else :
                board.curr_player = "O"

            if count_no_possible_moves > 3 : #to prevent infinite loop
                score = calculate_score(board)
                if print_output :
                    if AI_player == '0':
                        print (f"Game over ! | Score : blanc : {score[0]}, noir (IA) : {score[1]}")
                    else:
                        print (f"Game over ! | Score : blanc (IA) : {score[0]}, noir : {score[1]}")

                end = time.time()
                final_time_ms = round((end-start) * 10**3)
                return [f"{AI_type} vs {player_type}, depth {depth}, nb rounds {nb_simulations}", AI_player, score, final_time_ms, board.moves_history]

        else : # some moves are possible  
            if board.curr_player != AI_player: # player is playing (can be "random", "min_max", "alpha_beta", "mcts", "human")
                if player_type == "human" :
                    current_move = input(f"Enter your move for player {board.curr_player} : ")           
                elif player_type == "random" :
                    current_move = moves [ randint(0, len(moves)-1) ] 
                elif player_type == "min_max" :
                    current_move = move_Min_Max (board, depth)
                elif player_type == "mcts" :
                    current_move = move_MCTS (MCTS_Node(board, None), nb_simulations, AI_player, print_output, save_party=False)
                    
            else: # AI is playing (can be "random", "min_max", "alpha_beta", "mcts", "human")
                if AI_type == "human" :
                    current_move = input(f"Enter your move for player {board.curr_player} : ")
                elif AI_type == "random" :
                    current_move = moves [ randint(0, len(moves)-1) ] 
                elif AI_type == "min_max" :
                    current_move = move_Min_Max (board, depth)
                elif AI_type == "alpha_beta" :
                    AI_score = calculate_score(board)[position]
                    current_move = move_Alpha_Beta (board, board.curr_player, AI_player, AI_score, depth)
                elif AI_type == "mcts" :
                    current_move = move_MCTS (MCTS_Node(board, None), nb_simulations, AI_player, print_output, save_party=False)
            
            board.flip_tiles(current_move, board.curr_player)
            board.place_tile(current_move, board.curr_player)
            board.game_count += 1
            board.moves_history.append([board.curr_player, current_move])
            if board.curr_player == "O" :
                board.curr_player = "0"
            else :
                board.curr_player = "O"

    score = calculate_score(board)
    if print_output :
        if AI_player == '0':
            print (f"Game over ! | Score : blanc : {score[0]}, noir (IA) : {score[1]}")
        else:
            print (f"Game over ! | Score : blanc (IA) : {score[0]}, noir : {score[1]}")
    end = time.time()
    final_time_ms = round((end-start) * 10**3)
    return [f"{AI_type} vs {player_type}, depth {depth}, nb rounds {nb_simulations}", AI_player, score, final_time_ms, board.moves_history]
