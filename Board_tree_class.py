
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 2022
@author:  jaly, delpierot, judith
"""

import matplotlib.pyplot as plt
import numpy as np
import logging
import time
import math
from random import randint

from othello_backend import Board
from othello_backend import play_cvc_random_iter
from othello_backend import play_cvc_random

class Board_tree :
    """
    generate a tree of all possible boards, and the methods to navigate the tree
    """
    tree = {}
    
    def __init__(self, board : Board, local_depth : int, depth : int):
        """
        Initialize the tree
        inputs : board (Board): the board from which we want to generate all possible boards
                 local_depth (int): the in between depth of the tree
                 depth (int): the depth of the tree
        """
        self.tree = self.gen_all_possible_boards(board, local_depth, depth)
        pass
    
    
    def gen_all_possible_boards (self, board : Board, local_depth : int, depth : int):
        """
        Generate all possible boards from a given board and store them in a tree
        Tree is generated from local_depth to depth-1 (depth is not included, and depth-1 level are leaves)
        Inputs : board (Board): the board from which we want to generate all possible boards
                 local_depth (int): the in between depth of the tree
                 depth (int): the depth of the tree
        """

        if local_depth == depth :
            return board     
        
        else :
            possibles = board.generate_possible_boards(board.curr_player)
            r = {"depth" : local_depth, "board" : [],"child" : []}
            
            for poss in possibles :
                if board not in r["board"] :
                    r["board"].append(board)
                r["depth"] = local_depth
                r["child"].append(self.gen_all_possible_boards(poss, local_depth+1, depth))
        return (r)
    
    def resume_tree_to_boards (self) :
        """
        summarize the tree to a list of boards with indicated level
        """
        
        for key, value in self.tree.items() :
            pass
    
    def find_board (self, board : Board) :
        """
        Find a board in the tree
        Inputs : board (Board object): the board to find
        Returns : the board if found, None otherwise
        """
        pass
        
        
    def rollout_backpropagation_random (self, board : Board) :
        """
        lets the compluter play against another computer (both using random moves)
        Only one board is used to play !
        Inputs : board (Board object): the board on which the game is played
        Returns : (final board, score : (tuple : (white_score, black_score)), time for the party to be played)
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
    
    def play_all_parties_from_level (self) :  
        
        pass
        
        
    def add_leaf_child_node (self) :
        """
        Add a node to the tree
        """
        pass
    
    
    def update_MCTS_score (self, board : Board, final_score : tuple) :
        """
        Update the score of the tree
        """
        if final_score[0] > final_score[1] :
            board.MCTS_score += 1
        elif final_score[0] < final_score[1] :
            board.MCTS_score -= 1
        else :
            pass
    

A = Board(8)
B = Board_tree(A, 0, 2)
# start = time.time()
# print(B.tree)
# end = time.time()
# print((end-start)*1000)

print(B.tree)
# party = B.get_party_output(A)
# print(party[0].print_board())