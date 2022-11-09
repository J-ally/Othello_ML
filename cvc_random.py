# -*- coding: utf-8 -*-

"""
Created on Nov 09 2022
@author:  jaly
"""

from othello_backend import *

def play_cvc_random (board : Board) :
    """
    lets the compluter play against another computer (both using random moves)
    Inputs : board (Board object): the board on which the game is played
    Returns :
    """
    flag = True
    
    while flag :
        board.print_board()
        
        print(f"#### PLAYER {board.curr_player} TURN ! #### turn {board.game_count}")
        
        move = board.generate_all_possible_moves(board.curr_player)
        
        if move == None : #no possible moves for the player
            logging.info(f"turn {board.game_count} of player {board.curr_player} : tile not placed ! No possible moves \n")
            
            board.game_count += 0
            if board.curr_player == "O" :
                board.curr_player = "0"
            else :
                board.curr_player = "O"
            pass
                
            if board.game_count == (board.size**2) : #end of the game
                flag = False
                print ("Game over !")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                break
        
        else :
            move = move[ randint(0, len(move)-1) ]   
                
            logging.info(f"turn {board.game_count} of player {board.curr_player} : move {move} entered")
            
            if board.is_valid_loc (move) : #the move is possible (location wise)
                
                tiles_to_be_fliped = board.flip_tiles(move, board.curr_player)
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tiles fliped : {tiles_to_be_fliped}")
                
                if tiles_to_be_fliped != [] : #the move is possible (gameplay wise)
                    
                    board.place_tile(move, board.curr_player)
                    logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {move} \n")
                    
                    board.game_count += 1
                    if board.curr_player == "O" :
                        board.curr_player = "0"
                    else :
                        board.curr_player = "O"
                
                else :
                    print("This move is not possible, please try again")
                    logging.info(f"turn {board.game_count} of player {board.curr_player} : tile placed at {move} already occupied or no tiles to be flipped")
                    pass
            
            elif board.game_count == (board.size**2)-4 : #end of the game
                flag = False
                print ("Game over !")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : game over \n")
                pass
            
            else :
                print("This move is not possible, please try again")
                logging.info(f"turn {board.game_count} of player {board.curr_player} : tile at {move} is out of the board")
                pass
            
    pass
