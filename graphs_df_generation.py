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
from tqdm import tqdm

from othello_final import Board
from othello_final import play_random_vs_random
from othello_final import play_min_max_vs_random
from othello_final import play_alpha_beta_vs_random
from othello_final import play_mcts_vs_random

sys.setrecursionlimit(1000000000)

###############################################################################
#                       GENERATING GRAPHS MIN MAX                             #
###############################################################################

"""
if score[0] > score[1]: #score blanc > score noir
    winner = 'AI' if AI_MinMax_player == 'O' else 'Random'
elif score[0] < score[1]:
    winner = 'AI' if AI_MinMax_player == '0' else 'Random'
else: #score blanc = score noir : it's a draw
    winner = None 
"""

def gen_graph_min_max () :
    scores = []
    for i in range(200):
        A = Board ()
        scores.append(play_cvc_MinMax(A,1))

    times = []
    Min_Max_Player = 0
    Random_player_score = 0

    for i in range (len(scores)) :
        try:
            times.append(scores[i][3])
            if scores[i][2] == "position":
                Min_Max_Player += 1
            elif scores[i][2] == "egalite":
                Min_Max_Player += 0.5
                Random_player_score += 0.5
            else:
                Random_player_score += 1
        except:
            pass
        
    plt.plot(np.arange(len(times)), times)
    plt.axhline(np.mean(times), color = "red")
    plt.ylabel("time (ms)")
    plt.xlabel("game")
    plt.show()

    print("Frequences of win for Alpha_Beta_player :", Min_Max_Player / (Min_Max_Player + Random_player_score))
    # Depth = [1,2]

    # AI_winner = []
    # Draw_game = []
    # AI_loser = []
    # mean_time = []

    # for d in Depth:
    #     FILE = f"Results_Othello_Depth-{d}-NoPB.txt"
    #     file = open(FILE, "r") 
        
    #     Results = pd.read_csv(
    #         FILE, sep=";",header=None)
    #     file.close()
        
    #     n = len(Results)
        
    #     AI_winner.append(sum(Results[1] == 'AI')/n)
    #     Draw_game.append(sum(Results[1] == 'None')/n)
    #     AI_loser.append(sum(Results[1] == 'Random')/n)
        
    #     mean_time.append(np.mean(Results[2]))
        
    # plt.figure("figure 1")
    # plt.plot(Depth, AI_winner,"ro", Depth,AI_winner,"darkred", 
    #          Depth, Draw_game,"bs", Depth, Draw_game,"darkblue",
    #          Depth, AI_loser,"g^", Depth, AI_loser,"darkgreen")
    # plt.figure("figure 2")
    # plt.plot(Depth,mean_time,"kx", Depth,mean_time,"k") 
    # plt.show()


def gen_graph_alpha_beta () :
    scores = []
    for i in range(200):
        A = Board ()
        scores.append(Alpha_Beta_VS_Random_judith(A,1))

    times = []
    Alpha_Beta_player_score = 0
    Random_player_score = 0

    for i in range (len(scores)) :
        try:
            times.append(scores[i][3])
            if scores[i][2] == "position":
                Alpha_Beta_player_score += 1
            elif scores[i][2] == "egalite":
                Alpha_Beta_player_score += 0.5
                Random_player_score += 0.5
            else:
                Random_player_score += 1
        except:
            pass
    plt.plot(np.arange(len(times)), times)
    plt.axhline(np.mean(times), color = "red")
    plt.ylabel("time (ms)")
    plt.xlabel("game")
    plt.show()
    print("Frequences of win for Alpha_Beta_player :", Alpha_Beta_player_score / (Alpha_Beta_player_score + Random_player_score))


###############################################################################
#                             DATA CONSTRUCTION                               #
###############################################################################

def construction_df_results (nb_games : int) :
    """
    Constructs a dataframe with the results of the games played
    Inputs : nb_games (int): number of games played
             segmentation (tuple): describe the number of games played for each gametype
    Outputs : df (dataframe): dataframe with the results of the games played
    
    | Game type              | AI player | final score | play duration | moves played                                  |   |
    |------------------------|-----------|-------------|---------------|-----------------------------------------------|---|
    | "random vs random"     | None      | (33,31)     | 435           | [['O', ((3, 3), (4, 4))], ['O', (5, 3)], ...] |   |
    | "alpha Beta vs random" | "O"       | (32,32)     | 400           | ...                                           |   |
    | min max vs random"     | "0"       | (62,2)      | 157           | ...                                           |   |
    
    """
    #7 types of games : random vs random, min max vs random depth 1,2,3 , alpha beta vs random depth 1,2,3
    
    two_d_array = []
    types_of_games = 7
    
    for i in tqdm (range (nb_games), desc="Loading ...") :
        A = Board ()
        if i < nb_games/types_of_games :
            two_d_array.append(play_random_vs_random(A))
        elif i < 2*nb_games/types_of_games :
            two_d_array.append(play_min_max_vs_random(A, 1))
        elif i < 3*nb_games/types_of_games :
            two_d_array.append(play_min_max_vs_random(A, 2))
        elif i < 4*nb_games/types_of_games :
            two_d_array.append(play_min_max_vs_random(A, 3))
        elif i < 5*nb_games/types_of_games :
            two_d_array.append(play_alpha_beta_vs_random(A, 1))
        elif i < 6*nb_games/types_of_games :
            two_d_array.append(play_alpha_beta_vs_random(A, 2))
        elif i < 7*nb_games/types_of_games :
            two_d_array.append(play_alpha_beta_vs_random(A, 3))
        elif i < 8*nb_games/types_of_games :
            two_d_array.append(play_mcts_vs_random(A))
            
            
    df = pd.DataFrame(two_d_array, columns = ["Game type", "AI player", "final score", "play duration", "moves played"])
    now = int( time.time() )
    df.to_csv(f"Dataframes/{now}_games_data.csv", index=False)
    return df

# for i in range (10) :

construction_df_results(16)

