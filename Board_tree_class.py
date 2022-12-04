
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
    
    def __init__(self, board : Board, depth : int):
        """
        Initialize the tree
        inputs : board (Board): the board from which we want to generate all possible boards
                 depth (int): the depth of the tree
        """
        self.tree = self.gen_all_possible_boards(board, depth)
        pass
    
    
    def gen_all_possible_boards (self, board : Board, depth : int):
        """
        Generate all possible boards from a given board and store them in a tree
        Inputs : board (Board): the board from which we want to generate all possible boards
                 depth (int): the depth of the tree
        """

        if depth == 0 :
            return board     
        
        else :
            possibles = board.generate_possible_boards(board.curr_player)
            r = {"board" : [],"child" : []}
            
            for poss in possibles :
                if board not in r["board"] :
                    r["board"].append(board)
                r["child"].append(self.gen_all_possible_boards(poss, depth-1))
        return (r)
    
    def get_party_output (self, board : Board) :
        """
        Get the output of the party from the tree
        Inputs : tree (dict): the tree of all possible boards
                 depth (int): the depth of the tree
        """
        return (play_cvc_random(board))
    
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
        pass
    

A = Board(8)
B = Board_tree(A, 3)
# start = time.time()
# print(B.tree)
# end = time.time()
# print((end-start)*1000)

party = B.get_party_output(A)
print(party[0].print_board())