
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
from othello_backend import play_cvc_random

class MCTS_Node :   
        
    def __init__(self, board : Board, depth : int, parent , \
                       win_count : int = 0, UCT_score : float = 0, nb_visit : int = 0 ) -> None:
        self.board = board
        self.depth = depth
        self.UCT_score = UCT_score
        self.nb_visit = nb_visit
        self.parent = parent
        self.win_count = win_count
        self.children = []
        pass
    
    
    def generate_children(self) -> list:
        """
        Get the children of the current node (the possible moves) in a node list
        Inputs :
        Returns : the list of children nodes
        """
        possible_boards = self.board.generate_possible_boards(self.board.curr_player)
        children = []
        for i in range (len(possible_boards)):
            children.append(MCTS_Node(possible_boards[i], self.depth + 1, self))
        return children
        
        
    def play_random_from_node(self) -> None:
        """
        Play a random game from the current node
        Inputs :
        Returns : updates the score of the node as well as the number of visits
        """
        output_game = play_cvc_random(self.board)
        score = output_game[1]
        self.nb_visit += 1

        if self.board.curr_player == "O" and score[0] > score[1]: #white wins
            self.UCT_score += 1
        elif self.board.curr_player == "0" and score[0] > score[1]: #black wins
            self.UCT_score += 1
        else : 
            pass
        pass
    
    
    def add_child(self, child) -> None:
        """
        Add a child to the current node
        """
        self.children.append(child)
        pass
    
    
    def calc_UCT_score (self, nb_exploration : int) -> None:
        """
        calculates the UCT score of the current node
        Inputs :
        Returns : updates the score of the node
        """
        self.UCT_score = self.win_count / self.nb_visit + 2*(math.sqrt(math.log(nb_exploration) / self.nb_visit))
        
        
    def choose_node (self) :
        """
        chooses a node to expand
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
    
    
def play_MCTS_cvc_random (board : Board, nb_rounds : int) -> None:
    """
    Play a game with MCTS
    Inputs : board : Board, nb_rounds : int
    Returns : None
    """
    root = MCTS_Node(board, 0, None)
    root.generate_children()
    for i in range(nb_rounds) :
        node = root
        while len(node.children) != [] : #moves are possible
            node = node.children[node.choose_node()]
        if node.board.is_game_over() :
            pass
        else :
            node.expand_node()
            node = node.children[node.choose_node()]
            node.play_random_from_node()
            while node.parent != None :
                node = node.parent
                node.play_random_from_node()
    pass
    
A = Board()
print(play_MCTS_cvc_random(A, 10))
    