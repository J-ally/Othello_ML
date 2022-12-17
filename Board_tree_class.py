
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
                r["child"].append(self.gen_all_possible_nodes(poss, local_depth+1, depth))
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
        
        #the initialization of the tree        
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
    
    def get_leaf_nodes (self) :
        """
        Finds all the leaf nodes
        Returns : a list of leaf nodes
        """
        leaf_nodes = []
        for i in range (len(self.decomposed_tree)) :
            if self.decomposed_tree[i].get("depth") == self.tree_depth +1 :
                leaf_nodes.append(self.decomposed_tree[i])
        return leaf_nodes
    
    
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
    
    
    def play_cvc_random_with_boards (self, board : Board, boards_played : list, count_no_possible_moves : int) :
        """
        lets the compluter play against another computer (both using random moves)
        Only one board is used to play !
        Inputs : board (Board object): the board on which the game is played
        Returns : (final board, score : (tuple : (white_score, black_score)), time for the party to be played)
        """
        
        if board.is_not_full() and count_no_possible_moves < 15 :
            possible_boards = board.generate_possible_boards(board.curr_player)
            
            if possible_boards == [] : #no moves possible
                board2 = board.__deepcopy__()
                board2.game_count += 0
                
                if board2.curr_player == "O" :
                    board2.curr_player = "0"
                else :
                    board2.curr_player = "O"

                boards_played.append(board2)
                self.play_cvc_random_with_boards(board2, boards_played, count_no_possible_moves+1)
                    
            else :
                board2 = possible_boards [ randint(0, len(possible_boards)-1) ] 
                boards_played.append(board2)
                # print(boards_played)
                print(count_no_possible_moves)
                self.play_cvc_random_with_boards(board2, boards_played, count_no_possible_moves)
        
        elif count_no_possible_moves > 15 : #to prevent infinite loop
            score = calculate_score(board)
            print (f"Game over (not finished) ! | Score : blanc : {score[0]}, noir : {score[1]}")
            return (score, boards_played)
        
        else : #game over
            score = calculate_score(board)
            print (f"Game over ! | Score : blanc : {score[0]}, noir : {score[1]}")
            return (score, boards_played)
    
    
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
class MCTS :
    """
    The Monte Carlo Search Tree AI
    1 - It takes the current game state
    2 - It runs multiple random game simulations starting from this game state
    3 - For each simulation, the final state is evaluated by a score (higher score = better outcome)
    4 - It only remembers the next move of each simulation and accumulates the scores for that move
    5 - Finally, it returns the next move with the highest score
    """
    
    def __init__(self, expl_ratio : float, nb_iter : int, board : Board, node_tree : Node_tree) :
        self.expl_ration = expl_ratio
        self.nb_iter = nb_iter
        self.board = board
        self.node_tree = node_tree
        self.init_tree_depth = node_tree.tree_depth
        pass
    
    
    def select_node (self) :
        """
        handles the selection of the MCTS algorithm
        """
        
        pass
    
    
    def exploration_random (self) :
        """
        handles the exploration of the MCTS algorithm
        """
        leaf_nodes = self.node_tree.get_leaf_nodes()
        for i in range (len(leaf_nodes)) :
            if leaf_nodes[i].get("n_vis") == 0 :
                selected_node = leaf_nodes[i]
                # we play a random game from this node
            
                break
        
        pass
        

A = Board(8)
B = Node_tree(A, 0, 2)

for _ in range (50) :
    print(B.play_cvc_random_with_boards(A, [], 0))

# print(B.decomposed_tree)
# print(B.get_leaf_nodes())
# print(B.calculate_and_update_UCB_score(B.decomposed_tree[0], 2, 3))
# print(B.get_boards_from_depth(3))
# print(B.insert_node_to_dec_tree(D, A))

# MCT = MCTS( 1, 10, A, B)

