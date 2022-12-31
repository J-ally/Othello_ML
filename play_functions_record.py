# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 2022
@author:  jaly, delpierot, judith
"""

###############################################################################
#                                  IMPORTS                                    #
###############################################################################

import matplotlib.pyplot as plt
import numpy as np
import logging
import time
import math
import pandas as pd
import copy
from random import randint

from othello_final import Board
from othello_final import MCTS_Node
from othello_final import calculate_score
from othello_final import move_MCTS
from othello_final import move_Min_Max
from othello_final import move_Alpha_Beta
from othello_final import play_FAST_random_vs_random


###############################################################################
#                          PLAYING FUNCTIONS                                  #
###############################################################################


def play_random_vs_random (board_init : Board, print_output : bool = False) -> list:
    """
    lets the compluter play against another computer (both using random moves)
    Only one board is used to play !
    Inputs : board (Board object): the board on which the game is played
    Returns : (final board, score : (tuple : (white_score, black_score)), time for the party to be played)
    """
    start = time.time()
    count_no_possible_moves = 0
    board = board_init.__deepcopy__()
    
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
                if print_output :
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
    if print_output :
        print (f"Game over ! | Score : blanc : {score[0]}, noir : {score[1]}")
    # board.print_board()
    logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
    end = time.time()
    final_time_ms = round((end-start) * 10**3)
    return ["random vs random", None, score, final_time_ms, board.moves_history]


def play_mcts_vs_random (board : Board, nb_simulations : int = 100) :
    """
    lets the compluter play against another computer (one using random moves, one using AI)
    Only one board is used to play !
    Inputs : board (Board object): the board on which the game is played
            depth_exploration (int): the depth the AI explores the game to play
    Returns : board (Board object), score , final_time_ms
    """
    start = time.time()
    count_no_possible_moves = 0
    AI_player = ['0', 'O'][randint(0,1)]
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
                if AI_player == '0':
                    print (f"Game over ! | Score : blanc : {score[0]}, noir (IA) : {score[1]}")
                else:
                    print (f"Game over ! | Score : blanc (IA) : {score[0]}, noir : {score[1]}")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                
                end = time.time()
                final_time_ms = round((end-start) * 10**3)
                return ([f"mcts vs random", AI_player, score, final_time_ms, board.moves_history])
            
        else :
            if board.curr_player != AI_player: #Random is playing
                current_move = moves [ randint(0, len(moves)-1) ] 
                logging.info(f"turn {board.game_count} of random player {board.curr_player} : move {current_move} entered")
            
            else: #AI is playing
                #board.print_board()
                current_move = move_MCTS (MCTS_Node(board, None), nb_simulations, AI_player) #mcts for the player choose
                logging.info(f"turn {board.game_count} of AI player {board.curr_player} : move {current_move} entered")
            
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
    if AI_player == '0':
        print (f"MCTS Game over ! | Score : blanc : {score[0]}, noir (IA) : {score[1]}")
    else:
        print (f"MCTS Game over ! | Score : blanc (IA) : {score[0]}, noir : {score[1]}")
    # board.print_board()
    logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
    end = time.time()
    final_time_ms = round((end-start) * 10**3)
    return ([f"mcts vs random, {nb_simulations} rounds", AI_player, score, final_time_ms, board.moves_history])


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
                current_move = move_Alpha_Beta (board, board.curr_player, AI_player, AI_score, depth_max) #alpha beta for the player choose
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
                current_move = move_Min_Max(board, depth_exploration)
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

