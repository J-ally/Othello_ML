
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

from othello_final import Board
from othello_final import play_random_vs_random

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
    
    
    def add_child(self, child) -> None:
        """
        Add a child to the current node
        """
        self.children.append(child)
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
        print(f"child {index_child} : visit {child.nb_visit} : score : {child.UCT_score}")
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
    
    
def play_MCTS_vs_random (node : MCTS_Node, nb_rounds : int) -> None:
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


# print(MCTS_Node(Board(), 0, None).generate_children())

choosen_board = play_MCTS_vs_random( MCTS_Node(Board(), None), 10)
# print(choosen_node.children[0].UCT_score)
# print(choosen_node.children[1].UCT_score)
# print(choosen_node.children[2].UCT_score)
# print(choosen_node.children[3].UCT_score)

print(choosen_board)
    