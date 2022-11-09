# -*- coding: utf-8 -*-
"""
Created on Nov 09 2022
@author:  jaly
"""

from othello_backend import *

def generate_all_possible_boards (board : Board, depth : int = 4) :
    """
    Generates all possible boards for a given board, for a given depth
    
    Args:board (Board): a board instance
         depth (int, optional): the number of turns anticipated. Defaults to 4.
    """
    
    boards_generated = []
    
    ############ to code ############
    

# print(A.print_board())
# for i in range (len(possibles)) :
#     possibles[i].print_board(4)
#     print("\n ")
    
#     #possible moves for the second turn
#     possibles_2 = possibles[i].generate_possible_boards("0")
#     for j in range (len(possibles_2)) :
#         possibles_2[j].print_board(8)
#         print("\n ")
        
#         #possible moves for the third turn
#         possibles_3 = possibles_2[j].generate_possible_boards("O")
#         for k in range (len(possibles_3)) :
#             possibles_3[k].print_board(12)
#             print("\n ")
        
#     print("\n")
