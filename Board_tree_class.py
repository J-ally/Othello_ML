
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

class Node_tree :
    """
    generate a tree of all possible nodes as well as the methods to navigate the tree
    A node is defined this way (it's a dictionary) :
    {"depth" : 0, "board" : [board], "move" : (3,4), "score" : 0, "n_vis" : 0, "child" : [board, board, board ...]}
    """
    tree_depth = 0
    tree = {}
    decomposed_tree = []
    
    def __init__(self, board : Board, local_depth : int, depth : int):
        """
        Initialize the tree
        inputs : board (Board): the board from which we want to generate all possible boards
                 local_depth (int): the in between depth of the tree
                 depth (int): the final depth of the tree
        """
        self.tree = self.gen_all_possible_nodes(board, local_depth, depth)
        self.tree_depth = depth
        self.decomposed_tree = self.decompose_tree(self.tree)
        pass
    
    
    def gen_all_possible_nodes (self, board : Board, local_depth : int, depth : int):
        """
        Generate all possible nodes from a given board and store them in a tree
        Tree is generated from local_depth to depth  (depth +1 level is leaves' level)
        Inputs : board (Board): the board from which we want to generate all possible nodes
                 local_depth (int): the in between depth of the tree
                 depth (int): the depth of the tree
        Returns : a tree of nodes
        """
        if local_depth == depth +1 :
            return board     
        
        else :
            boards_poss = board.generate_possible_boards(board.curr_player)
            r = {"depth" : local_depth, "board" : [], "move" : 0, "score" : 0, "n_vis" : 0, "child" : []}
            
            for i in range (len(boards_poss)) :
                if board not in r["board"] :
                    r["board"].append(board)
                r["depth"] = local_depth
                r["move"] = boards_poss[i].previous_moves[-1][1]
                r["child"].append(self.gen_all_possible_nodes(boards_poss[i], local_depth+1, depth))
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
                tree_node_list.append({"depth" : child.get("depth"), "board" : child.get("board")[0],"move" :child.get("move") , 'score': 0, 'n_vis': 0 } )
                for board in child.get("child") : #the last level of the tree (list of boards)
                    tree_node_list.append({"depth" : child.get("depth") +1, "board" : board ,"move" :child.get("move") , 'score': 0, 'n_vis': 0} )
            else : #first levels of the tree
                tree_node_list.append({"depth" : child.get("depth"), "board" : child.get("board")[0],"move" :child.get("move") , 'score': 0, 'n_vis': 0 } )
                self.decompose_tree(child, tree_node_list) #recursion call
        
        #the initialization of the tree        
        tree_node_list_2 = [{"depth" : self.tree.get("depth"), "board" : self.tree.get("board")[0],"move" :self.tree.get("move") , 'score': 0, 'n_vis': 0}] + tree_node_list

        return tree_node_list_2

    def gen_path_from_node (self, board : Board, original_depth : int, nodes_list : list = []) :
        """
        Generate a random game from a given board, returns the list of nodes generated and 
        the original board
        Inputs : board (Board): the board from which we want to generate a random game
                 original_depth (int): the depth of the board given
                 nodes_list (list): the list of nodes to fill
        Returns : a list of nodes
        """
        boards_poss = board.generate_possible_boards(board.curr_player)
        # print(boards_poss == [], board.is_not_full(), len(boards_poss),{"depth" : original_depth, "board" : board, "move" : board.previous_moves[-1][1], "score" : 0, "n_vis" : 0, "child" : []} )
        # print(nodes_list)
        
        if boards_poss == [] and board.is_not_full() == False : #end of the game
            nodes_list += [{"depth" : original_depth, "board" : board, "move" : board.previous_moves[-1][1], "score" : 0, "n_vis" : 0, "child" : []}]
            return (nodes_list)
        
        elif boards_poss == [] and board.is_not_full() == True : #player has to pass
            board2 = board.__deepcopy__()
            board2.game_count += 0
            
            if board2.curr_player == "O" :
                board2.curr_player = "0"
            else :
                board2.curr_player = "O"
                
            nodes_list += [{"depth" : original_depth , "board" : board2, "move" : board2.previous_moves[-1][1], "score" : 0, "n_vis" : 0, "child" : []}]
            return (self.gen_path_from_node(board2, original_depth +1, nodes_list ))      
        
        else : #normal game turn
            if len(boards_poss) == 1 :
                poss = boards_poss[0]
            else :
                poss = boards_poss [ randint(0, len(boards_poss)-1) ] 
            nodes_list += [{"depth" : original_depth , "board" : poss, "move" : poss.previous_moves[-1][1], "score" : 0, "n_vis" : 0, "child" : []}]
            return (self.gen_path_from_node(poss,original_depth +1, nodes_list))
     
    
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
    
    
    def get_index_from_board (self, board : Board) :
        """
        Finds a node from a given board
        Inputs : board (Board): the board from which we want to find the node
        Returns : the node
        """
        for i in range (len(self.decomposed_tree)) :
            if self.decomposed_tree[i].get("board") == board :
                return i
    
    
    def get_depth_of_board (self, board : Board) :
        """
        Finds the depth of a given board
        Inputs : board (Board): the board from which we want to find the depth
        Returns : the depth of the board
        """
        for i in range (len(self.decomposed_tree)) :
            if self.decomposed_tree[i].get("board") == board :
                return self.decomposed_tree[i].get("depth")
            
    
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
        i = self.get_index_from_board(board)
        
        if self.decomposed_tree[i].get("n_vis") == 0 :
            pass
        else : 
            score_2 = self.decomposed_tree[i].get("score") + \
                    expl_ratio * math.sqrt(math.log(nb_iter) / self.decomposed_tree[i].get("n_vis"))
        self.decomposed_tree[i]["score"] = score_2
        
        return score_2
    
    
    def get_init_leaf_nodes (self) :
        """
        Finds all the leaf nodes at the initial state of the tree
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
    
    
    def merge_branches_dec_tree (self, branch_one : list, branch_two : list) :
        """
        Merges the branches of the tree that have been played
        Inputs : boards_played (list of Board objects): the boards that have been played
        """
        new_branch = []
        if len(branch_one) != len(branch_two) :
            raise ValueError("The branches do not have the same length")
        else :
            for i in range (len(branch_one)) :
                if branch_one[i].get("move") != branch_two[i].get("move") :
                    new_branch += branch_one[i:]
                    new_branch += branch_two[i:]
                    break
                else :
                    new_branch.append(branch_one[i])
                    
        
        return new_branch
    
    
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
    
    
    
    
    


###############################################################################
#                                 TESTINGS                                    #
###############################################################################

A = Board(8)
B = Node_tree(A, 0, 2)

# print(B.tree)

# nodes_list = B.gen_path_from_node(B.decomposed_tree[0]["board"],original_depth=0)
# print(nodes_list)
# print(nodes_list[0]["board"].print_board(), nodes_list[0]["board"].curr_player, nodes_list[0]["board"].previous_moves)
# print(nodes_list[6]["board"].print_board(), nodes_list[6]["board"].curr_player, nodes_list[6]["board"].previous_moves)

# print(B.decomposed_tree[0]["board"].generate_possible_boards("O")[0].print_board())
# print(B.decomposed_tree[0]["board"].generate_possible_boards("O")[0].previous_moves)

# print(B.get_leaf_nodes())

# print(B.calculate_and_update_UCB_score(B.decomposed_tree[0], 2, 3))
# print(B.get_boards_from_depth(3))
# print(B.insert_node_to_dec_tree(D, A))

# MCT = MCTS( 1, 10, A, B)

