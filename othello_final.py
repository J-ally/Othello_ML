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

sys.setrecursionlimit(1000000000)

###############################################################################
#                          LOGGING DEFINITION                                 #
###############################################################################

logging.basicConfig(level=logging.INFO, filename = "logs_othello_backend_info.log", filemode = "w",
                    format = "%(asctime)s - %(levelname)s - %(message)s")

logging.basicConfig(level=logging.DEBUG, filename = "logs_othello_backend_debug.log", filemode = "w",
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
        self.moves_history.append(["O", ((middle_1,middle_1), (middle_2,middle_2))])
        self.moves_history.append(["0", ((middle_1,middle_2), (middle_2,middle_1))])
        
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

        logging.debug(f"turn {self.game_count} of player {self.curr_player} : board after move {move} generated : {new_board} ")
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
        
        logging.debug(f"turn {self.game_count} of player {self.curr_player} : all possible boards generated : {possible_boards} ")
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

def Alpha_Beta(board:Board, player:str, AI_player:str, AI_score:int, depth:int, depth_max:int, alpha:float, beta:float):
    if depth == depth_max or board.game_count ==64 :
        if board.curr_player == "O":
            score = calculate_score(board)[0]
        else:
            score = calculate_score(board)[1]
        return evaluation_function(board, score, board.curr_player)
    
    else:
        depth += 1
        for board in board.generate_possible_boards(board.curr_player):
            if board.curr_player == AI_player:
                value = -math.inf

                if board.curr_player == "O":
                    score = calculate_score(board)[0]
                else:
                    score = calculate_score(board)[1]

                value = max(value, Alpha_Beta(board, board.curr_player, AI_player, AI_score, depth, depth_max, alpha, beta))
                alpha = max(value, alpha)
                if beta <= alpha:
                    break
            else:
                value = math.inf
                if board.curr_player == "O":
                    score = calculate_score(board)[0]
                else:
                    score = calculate_score(board)[1]
                value = min(value, Alpha_Beta(board, board.curr_player, AI_player, AI_score, depth, depth_max, alpha, beta))
                beta = min(value, beta)
                if beta <= alpha:
                    break
            
        return value
    
def Best_Move ( board:Board, player:str, AI_player:str, AI_score:int, depth_max:int):
    beta = math.inf
    best_value = -math.inf
    best_node = None
    best_move = None

    depth = 0
    depth += 1

    moves = board.generate_all_possible_moves(board.curr_player)

    boards_list = board.generate_possible_boards(board.curr_player)
    for board in boards_list:
        value = Alpha_Beta(board, player, AI_player, AI_score, depth, depth_max, best_value, beta)

        if value >= best_value:
            best_value = value
            best_board = board
            best_move = moves[boards_list.index(best_board)]

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
    Calculates the value of one move by recursion for the AI with the MinMax algorithm.
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


def MinMax(board : Board, depth_exploration : int):
    """
    Calculates the value of the next possible moves for the AI with the MinMax algorithm.
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
        
        
    def play_random_from_node(self) -> None:
        """
        Play a random game from the current node
        Inputs :
        Returns : updates the score of the node as well as the number of visits
        """
        initial_player = self.board.curr_player
        # print(f"initial player : {initial_player}")
        output_game = play_random_vs_random(self.board)
        score = output_game[2]
        self.nb_visit += 1

        if initial_player == "O" and score[0] > score[1]: #white wins
            self.UCT_score += 1
        elif initial_player == "0" and score[0] > score[1]: #black wins
            self.UCT_score += 1
        else : 
            pass
        pass

    
    def calc_UCT_score (self, nb_exploration : int, index_child : int) -> None:
        """
        calculates and updates the UCT score of the current node
        Inputs : nb_exploration (int) : number of exploration rounds
                 index_child (int) : index of the child node that has been visited
        Returns : updates the score of the node
        """
        child = self.children[index_child]
        child.UCT_score = child.win_count / child.nb_visit + 2*(math.sqrt( math.log(nb_exploration) / child.nb_visit))
        # print(f"child {index_child} : visit {child.nb_visit} : score : {child.UCT_score}")
        pass
    
        
    def choose_child_node (self) :
        """
        chooses a node to expand (max UCT score)
        Inputs :
        Returns : the index of the node to expand in the list of children
        """
        index_node = 0
        for child in self.children :
            if child.UCT_score == 0 : #node not visited
                return self.children.index(child)
            
            elif child.UCT_score > self.children[index_node].UCT_score :
                index_node = self.children.index(child)
        return index_node
    
    
def play_mcts (node : MCTS_Node, nb_rounds : int) -> None:
    """
    Play one iteration game with MCTS
    Inputs : board : Board, nb_rounds : int
    Returns : The board choosen for the simulation
    """
    node.children = node.generate_children()
    # print(f"current node {node.board}")
    # print(f"children {node.children}")
    for round in range(1, nb_rounds + 1,1) :
        # print(f"round {round}")
        exploration_node = node.children[node.choose_child_node()]
        # exploration_node.board.print_board()     
        exploration_node.play_random_from_node()
        node.calc_UCT_score(round, node.children.index(exploration_node))
        # print("\n")
    final_node = node.children[node.choose_child_node()]
    return final_node.move

###############################################################################
#                          PLAYING FUNCTIONS                                  #
###############################################################################

def play_random_vs_random (board : Board) :
    """
    lets the compluter play against another computer (both using random moves)
    Only one board is used to play !
    Inputs : board (Board object): the board on which the game is played
    Returns : (final board, score : (tuple : (white_score, black_score)), time for the party to be played)
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
            
            if count_no_possible_moves > 3 : #to prevent infinite loop
                score = calculate_score(board)
                print (f"Game over ! | Score : blanc : {score[0]}, noir : {score[1]}")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                end = time.time()
                final_time_ms = round((end-start) * 10**3)
                return ["random vs random", None, score, final_time_ms, board.moves_history]
            
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
                    board.moves_history.append([board.curr_player, current_move])
                    
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
    return ["random vs random", None, score, final_time_ms, board.moves_history]


def play_random_vs_random_boards (board : Board) :
    """
    Inputs : board (Board): _description_
    """
    
    start = time.time()
    count_no_possible_moves = 0
    
    while board.is_not_full() :
        
        poss_boards = board.generate_possible_boards(board.curr_player)
        logging.info(f"turn {board.game_count} of player {board.curr_player} :     boards possible {poss_boards} ")
        
        if poss_boards == [] : #no possible moves for the player
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
            board = poss_boards [ randint(0, len(poss_boards)-1) ] 
            board.game_count += 1
            if board.curr_player == "O" :
                board.curr_player = "0"
            else :
                board.curr_player = "O"
            
            logging.info(f"turn {board.game_count} of player {board.curr_player} : board {board} choosen")
    
    score = calculate_score(board)
    print (f"Game over ! | Score : blanc : {score[0]}, noir : {score[1]}")
    # board.print_board()
    logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
    end = time.time()
    final_time_ms = round((end-start) * 10**3)
    return (board, score, final_time_ms)   
    

def play_min_max_vs_random (board : Board, depth_exploration : int) :
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
    #print(f'AI plays : {AI_MinMax_player}')
    
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
            
            if count_no_possible_moves > 3 : #to prevent infinite loop
                score = calculate_score(board)
                if AI_MinMax_player == '0':
                    print (f"Game over ! | Score : blanc : {score[0]}, noir (IA) : {score[1]}")
                else:
                    print (f"Game over ! | Score : blanc (IA) : {score[0]}, noir : {score[1]}")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                
                end = time.time()
                final_time_ms = round((end-start) * 10**3)
                return ([f"min max vs random, explo depth {depth_exploration}", AI_MinMax_player, score, final_time_ms, board.moves_history])
            
        else :
            if board.curr_player != AI_MinMax_player: #Random is playing
                current_move = moves [ randint(0, len(moves)-1) ] 
                logging.info(f"turn {board.game_count} of random player {board.curr_player} : move {current_move} entered")
            
            else: #The minmax AI is playing
                #board.print_board()
                current_move = MinMax(board, depth_exploration)
                logging.info(f"turn {board.game_count} of AI minmax player {board.curr_player} : move {current_move} entered")
            
            if board.is_valid_loc (current_move) : #the move is possible (location wise)
                
                tiles_to_be_fliped = board.flip_tiles(current_move, board.curr_player)
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tiles fliped : {tiles_to_be_fliped}")
                
                if tiles_to_be_fliped != [] : #the move is possible (gameplay wise)
                    
                    board.place_tile(current_move, board.curr_player)
                    logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {current_move} \n")
                    
                    board.game_count += 1
                    board.moves_history.append([board.curr_player, current_move])
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
    if AI_MinMax_player == '0':
        print (f"Game over ! | Score : blanc : {score[0]}, noir (IA) : {score[1]}")
    else:
        print (f"Game over ! | Score : blanc (IA) : {score[0]}, noir : {score[1]}")
    # board.print_board()
    logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
    end = time.time()
    final_time_ms = round((end-start) * 10**3)
    return ([f"min max vs random, explo depth {depth_exploration}", AI_MinMax_player, score, final_time_ms, board.moves_history])


def play_alpha_beta_vs_random (board : Board, depth_max : int) :
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
    position = randint(0,1)
    AI_player = ['O', '0'][position]

    if position == 0 :
        position_adverse = 1
    else:
        position_adverse = 0

    adverse_player = None
    if AI_player == '0':
        adverse_player = 'O'
    else:
        adverse_player = '0'
    
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
            
            if count_no_possible_moves > 3 : #to prevent infinite loop
                score = calculate_score(board)
                if AI_player == '0':
                    print (f"Game over ! | Score : blanc : {score[0]}, noir (IA) : {score[1]}")
                else:
                    print (f"Game over ! | Score : blanc (IA) : {score[0]}, noir : {score[1]}")
                end = time.time()
                final_time_ms = round((end-start) * 10**3)

                #print (f"Game over ! | Score : blanc : {score[0]}, noir : {score[1]}")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                return ([f"alpha beta vs random, explo depth {depth_max}", AI_player, score, final_time_ms, board.moves_history])
            
        else :
            if board.curr_player == AI_player :
                AI_score = calculate_score(board)[position]
                current_move = Best_Move (board, board.curr_player, AI_player, AI_score, depth_max) #alpha beta for the player choose
                logging.info(f"This the move played by alpha beta player {current_move} \n")
            else :
                current_move = moves[randint(0, len(moves)-1)] #random for the other player

            logging.info(f"turn {board.game_count} of player {board.curr_player} : move {current_move} entered")
            
            if board.is_valid_loc (current_move) : #the move is possible (location wise)
                
                tiles_to_be_fliped = board.flip_tiles(current_move, board.curr_player)
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tiles fliped : {tiles_to_be_fliped}")
                
                if tiles_to_be_fliped != [] : #the move is possible (gameplay wise)
                    
                    board.place_tile(current_move, board.curr_player)
                    logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {current_move} \n")
                    
                    board.game_count += 1
                    board.moves_history.append([board.curr_player, current_move])
                    
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
    logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
    if AI_player == '0':
        print (f"Game over ! | Score : blanc : {score[0]}, noir (IA) : {score[1]}")
    else:
        print (f"Game over ! | Score : blanc (IA) : {score[0]}, noir : {score[1]}")
    end = time.time()
    final_time_ms = round((end-start) * 10**3)
    return ([f"alpha beta vs random, explo depth {depth_max}", AI_player, score, final_time_ms, board.moves_history])


def play_mcts_vs_random (board : Board, nb_simulations : int = 100) :
    """
    lets the compluter play against another computer (both using random moves)
    Only one board is used to play !
    Inputs : board (Board object): the board on which the game is played
    Returns : (final board, score : (tuple : (white_score, black_score)), time for the party to be played)
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
            
            if count_no_possible_moves > 3 : #to prevent infinite loop
                score = calculate_score(board)
                print (f"Game over ! | Score : blanc : {score[0]}, noir : {score[1]}")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                end = time.time()
                final_time_ms = round((end-start) * 10**3)
                return ["mcts vs random", None, score, final_time_ms, board.moves_history]
            
        else :
            current_move = play_mcts(MCTS_Node(board, None), nb_simulations) #mcts for the player choose
            logging.info(f"turn {board.game_count} of player {board.curr_player} : move {current_move} entered")
            
            if board.is_valid_loc (current_move) : #the move is possible (location wise)
                
                tiles_to_be_fliped = board.flip_tiles(current_move, board.curr_player)
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tiles fliped : {tiles_to_be_fliped}")
                
                if tiles_to_be_fliped != [] : #the move is possible (gameplay wise)
                    
                    board.place_tile(current_move, board.curr_player)
                    logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {current_move} \n")
                    
                    board.game_count += 1
                    board.moves_history.append([board.curr_player, current_move])
                    
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
    return ["mcts vs random", None, score, final_time_ms, board.moves_history]