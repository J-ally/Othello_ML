
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
import pandas as pd
import copy
from random import randint

from othello_backend import Board
from othello_backend import play_cvc_random_iter
from othello_backend import play_cvc_random

class Node_tree :
    """
    generate a tree of all possible nodes, and the methods to navigate the tree
    """
    tree_depth = 0
    tree = {}
    decomposed_tree = []
    
    def __init__(self, board : Board, local_depth : int, depth : int):
        """
        Initialize the tree
        inputs : board (Board): the board from which we want to generate all possible boards
                 local_depth (int): the in between depth of the tree
                 depth (int): the depth of the tree
        """
        self.tree = self.gen_all_possible_nodes(board, local_depth, depth)
        self.tree_depth = depth
        self.decomposed_tree = self.decompose_tree(self.tree)
        pass
    
    
    def gen_all_possible_nodes (self, board : Board, local_depth : int, depth : int):
        """
        Generate all possible nodes from a given board and store them in a tree
        Tree is generated from local_depth to depth-1 (depth is not included, and depth-1 level are leaves)
        Inputs : board (Board): the board from which we want to generate all possible nodes
                 local_depth (int): the in between depth of the tree
                 depth (int): the depth of the tree
        """
        if local_depth == depth +1 :
            return board     
        
        else :
            possibles = board.generate_possible_boards(board.curr_player)
            r = {"depth" : local_depth, "board" : [], "score" : 0, "n_vis" : 0, "child" : []}
            
            for poss in possibles :
                if board not in r["board"] :
                    r["board"].append(board)
                r["depth"] = local_depth
                r["child"].append(self.gen_all_possible_boards(poss, local_depth+1, depth))
        return (r)
    
    
    def decompose_tree (self, given_dict : dict, tree_node_list = []) :
        """
        decompose the tree into a list of nodes with their depth, and store them in a list
        Inputs : depth (int): the depth of the tree
                 tree_node_list (list): the list of nodes to fill
        Returns : a list of nodes
        """
    
        for child in given_dict["child"] :
            if child.get("depth") == self.tree_depth : #the before last level of the tree
                tree_node_list.append({"depth" : child.get("depth"), "board" : child.get("board")[0], 'score': 0, 'n_vis': 0 } )
                for board in child.get("child") : #the last level of the tree (list of boards)
                    tree_node_list.append({"depth" : child.get("depth") +1, "board" : board , 'score': 0, 'n_vis': 0} )
            else : #first levels of the tree
                tree_node_list.append({"depth" : child.get("depth"), "board" : child.get("board")[0], 'score': 0, 'n_vis': 0 } )
                self.decompose_tree(child, tree_node_list) #recursion call
                
        tree_node_list_2 = [{"depth" : self.tree.get("depth"), "board" : self.tree.get("board")[0], 'score': 0, 'n_vis': 0}] + tree_node_list

        return tree_node_list_2
    
    
    def get_nodes_from_depth (self, depth : int) :
        """
        Finds all the node for a given depth
        Inputs : depth (int): the depth of the tree
        Returns : a list of nodes
        """
        depth_nodes = []
        for i in range (len(self.decomposed_tree)) :
            if self.decomposed_tree[i].get("depth") == depth :
                depth_nodes.append(self.decomposed_tree[i]["board"])
        return depth_nodes
    
    
    def insert_node_to_dec_tree (self, board_to_add : Board, parent_board : Board ) :
        """
        Adds a node in the tree (at the correct index to maintain the tree structure)
        """
        for i in range (len(self.decomposed_tree)) :
            if self.decomposed_tree[i].get("board") == parent_board :
                decomposed_tree_2 = self.decomposed_tree[:i+1] + \
                                    [{'depth': self.decomposed_tree[i].get("depth") + 1, 'board': board_to_add, 'score': 0, 'n_vis': 0}] + \
                                    self.decomposed_tree[i+1 :]
                break
        self.decomposed_tree = copy.copy(decomposed_tree_2)
        return (self.decomposed_tree)
    
        
    def calculate_and_update_UCB_score (self, board : Board, expl_ratio : float, nb_iter : int) :
        """
        Calculates and updates the UCB score for a given node
        Inputs : board (Board): the node for which we want to calculate the UCB score
                 expl_ratio (float): the exploration ratio
        Returns : the UCB score
        """
        score_2 = 0
        for i in range (len(self.decomposed_tree)) :
            if self.decomposed_tree[i].get("board") == board :
                if self.decomposed_tree[i].get("n_vis") == 0 :
                    score_2 = 0
                else : 
                    score_2 = self.decomposed_tree[i].get("score") + \
                            expl_ratio * math.sqrt(math.log(nb_iter) / self.decomposed_tree[i].get("n_vis"))
                self.decomposed_tree[i]["score"] = score_2
                break
        return score_2
    
    
    def get_node_with_max_UCB_score (self, depth : int) :
        """
        choose the node with the maximum UCB score
        Inputs : depth (int): the depth of the tree for which we want to choose the node
        Returns : the node with the maximum UCB score
        """
        nodes_considered = self.get_nodes_from_depth(depth)
        selected_node = nodes_considered[0]
        
        for i in range (len(nodes_considered)) :
            if nodes_considered[i]["score"] > selected_node["score"] :
                selected_node = nodes_considered[i]
        return selected_node


class MCTS :
    def __init__(self):
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
    
    
###############################################################################
#                               GAME MODES                                    #
###############################################################################

def play_MCTSvc_random (board : Board, depth : int, nb_parties : int) :
    """
    play a game between a computer using MCTS and a computer using random moves
    Inputs : board (Board): a board object
             depth (int): the depth of the tree for the initialisation of the MCTS
             nb_parties (int): number of parties to be played
    """
    start = time.time()
    B = Board_tree(board, 0, depth)
    depth_nodes = B.get_boards_from_depth(depth)
    
    for i in range (nb_parties) :
        print(f"########## PARTY {i+1} ##########")
        party = B.get_party_output(board)
        print(party[0].print_board())
        print(f"########## PARTY {i+1} ##########")

    pass


A = Board(8)
D = Board (8)
print(D)

B = Board_tree(A, 0, 1)

# print(B.tree)
# print(B.decomposed_tree)

# print(B.calculate_and_update_UCB_score(B.decomposed_tree[0], 2, 3))
# print(B.get_boards_from_depth(3))
print(B.insert_board_to_dec_tree(D, A))