#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Frame coded by:
@author: Yanju Chen
@contact: yanju@cs.ucsb.edu
@file: RandomHex.py
@version: 0.1
@description:
This is Baseline#1 of UCSB CS165A Fall 2018 Machine Problem 2. The script implements basic random
algorithm for playing Hex. Please read the attached readme.txt for detailed usage.

Editted by:
Nuan Wen
'''

from __future__ import print_function

import sys
import time
import getopt
import random
import numpy as np
import copy

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTER2INT = {ALPHABET[i]:i for i in range(26)}
VALUE_EMPTY = 0
VALUE_RED = 1 # from letter side to letter side
VALUE_BLUE = -1 # from integer side to integer side
############ start of extra global variable declaration ############

############  end of extra global variable declaratio   ############
def check_pos(d_pos, d_size):
	# check validity of pos
	try:
		pi = d_pos[0]
		pj = d_pos[1]
		if pi<0 or pi>=d_size or pj<0 or pj>=d_size:
			return False
		else:
			return True
	except Exception:
		# could be type error or something
		return False

def inp_to_pos(d_inp, d_size):
	try:
		pi = d_inp[0]
		if not (pi in ALPHABET):
			return None
		pi = LETTER2INT[pi]
		pj = int(d_inp[1:])
		d_pos = (pi,pj)
		if check_pos(d_pos, d_size):
			return d_pos
		else:
			# out of range
			raise Exception
	except Exception:
		# fail to translate, invalid input
		# print("# Error: invalid position.")
		sys.exit(2)

def pos_to_inp(d_pos, d_size):
	try:
		pi = d_pos[0]
		pj = d_pos[1]
		if check_pos(d_pos, d_size):
			d_inp = "{}{}".format(ALPHABET[pi],pj)
			return d_inp
		else:
			# out of range
			raise Exception
	except Exception:
		# fail to translate, invalid input
		# print("# Error: invalid position.")
		sys.exit(2)

def update_board(d_board, d_pos, d_value, d_size):
	# update board status
	# return True: successful
	# return False: failed <-- actually, just raise an Exception
	try:
		pi = d_pos[0]
		pj = d_pos[1]
		if check_pos(d_pos, d_size):
			if d_board[pi][pj]==VALUE_EMPTY:
				d_board[pi][pj] = d_value
				return True
			else:
				raise Exception
		else:
			# out of range
			raise Exception
	except Exception:
		print("# Error: invalid position.")
		sys.exit(2)

def try_update_board(board, pos, value, size):
	# return True: successful
	# return False: failed
    i = pos[0]
    j = pos[1]
    if check_pos(pos, size) and board[i][j] == VALUE_EMPTY:
        board[i][j] = value
        return True
    return False

def strategy_random(d_board, d_size):
	# search for empty position
	d_available_pos = []
	for i in range(d_size):
		for j in range(d_size):
			if d_board[i][j]==VALUE_EMPTY:
				d_available_pos.append((i,j))
	if len(d_available_pos)==0:
		# END OF GAME
		# print("# Game Over.")
		sys.exit(0)
	# randomized
	random.shuffle(d_available_pos)
	return d_available_pos[0]

################ Start of My Implementation #####################

'''
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTER2INT = {ALPHABET[i]:i for i in range(26)}
VALUE_EMPTY = 0
VALUE_RED = 1 # from letter side to letter side
VALUE_BLUE = -1 # from integer side to integer side
'''
RED_PLAYER = 1
BLUE_PLAYER = -1
MAX_DEPTH = 2

#========= The heuristic function and helper functions =========
##def closest_position(pos_L, pos_N):
####	(pos_L_return, pos_N_return) = (pos_L, pos_N)
##
##	while( not check_pos(pos_L, pos_L)):
##		# update position => nearby location
##	return (pos_L_return, pos_N_return)
##
##def central_unoccupied_pos(board, size):
##        central_pos = int(d_size / 2)
##	return closest_position(central_pos, central_pos)
##
##def closeness_to_connect(board, size, which_player):
##        # the closer to a straight-cut, the better
##        pass
##
##def num_potential_path(board, size, which_player):
##        # the flexibility
##        pass

##def num_path_change(old_board_result, new_board):
##        # old_board_result: num_potential_path(old_board)
##        # positive: more paths for red and less for blue
##        # 0: cancel out
##        # negative: more paths for blud and less for red
##        return num_potential_path(new_board) - old_board_result

def heuristic_function(current_board):
    return 1

#========= The Minimax method with alpha-beta pruning =========
# http://aima.cs.berkeley.edu/python/games.html
def max_value_pos(board, empty_position_dict, alpha, beta, depth, which_player, size, pos = None):
    print("in max_value_pos")
    if (depth > MAX_DEPTH or len(empty_position_dict) == 0):
        print("terminate at 11 with pos:", pos)
        return (heuristic_function(board), pos)

    v = -1.0e40 # neg infinity

    for potential_pos in list(empty_position_dict):
        print("potential_pos_in_max:", potential_pos)
        print("board_in_max:", board)
        print("empty_position_dict.keys() in max:", empty_position_dict.keys())
        if not try_update_board(board, potential_pos, which_player, size):
            print("terminate at 12 with pos:", pos)
            return (v, pos)
        empty_position_dict.pop(potential_pos)
        v = max(v, min_value_pos(board, empty_position_dict, alpha, beta, depth+1, -1 * which_player, size, potential_pos)[0])
        if v >= beta:
            print("terminate at 13 with pos:", pos)
            return (v, pos)
        alpha = max(alpha, v)
    print("terminate at 14 with pos:", pos)
    return (v, pos)

def min_value_pos(board, empty_position_dict, alpha, beta, depth, which_player, size, pos = None):
    print("in min_value_pos")
    if (depth > MAX_DEPTH or len(empty_position_dict) == 0):
        print("terminate at 21 with pos:", pos)
        return (heuristic_function(board), pos)

    v = 1.0e40 # pos infinity

    for potential_pos in list(empty_position_dict):
        print("potential_pos_in_min:", potential_pos)
        print("board_in_min:", board)
        print("empty_position_dict.keys() in min:", empty_position_dict.keys())
        if not try_update_board(board, potential_pos, which_player, size):
            print("terminate at 22 with pos:", pos)
            return (v, pos)
        empty_position_dict.pop(potential_pos)
        v = min(v, max_value_pos(board, empty_position_dict, alpha, beta, depth+1, -1 * which_player, size, potential_pos)[0])
        if v <= alpha:
            print("terminate at 23 with pos:", pos)
            return (v, pos)
        beta = min(beta, v)
    print("terminate at 24 with pos:",pos)
    return (v, pos)

def alpha_beta_game_tree_search(board, size, empty_position_dict, which_player):
    (v, pos) =  min_value_pos(board, empty_position_dict, -1.0e40, 1.0e40, 0, which_player, size)
    print("pos:", pos)
    print("v:", v)
    return pos

#========= The all-in-one function =========

def my_strategy(board, size, empty_pos_dict, which_player):
    if len(empty_pos_dict)==0:
        sys.exit(0)
    temp_board = list(board)
    temp_empty_pos_dict = copy.deepcopy(empty_pos_dict)
    return alpha_beta_game_tree_search(temp_board, size, temp_empty_pos_dict, which_player)

################ End of My Implementation #####################


def print_board(d_board, d_size):
    print("     ",end="")
    for j in range(d_size):
        print(" {:<2} ".format(j),end="")
    print()
    print("    +",end="")
    for j in range(d_size):
        print("---+",end="")
    print()
    for i in range(d_size):
        print(" {:3}|".format(ALPHABET[i]),end="")
        for j in range(d_size):
            if d_board[i][j]==VALUE_RED:
                print(" R |",end="")
            elif d_board[i][j]==VALUE_BLUE:
                print(" B |",end="")
            else:
                print("   |",end="")
        print()
        print("    +",end="")
        for j in range(d_size):
            print("---+",end="")
        print()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "dp:s:", ["debug","player=","size="])
    except getopt.GetoptError:
        print('Error: RandomHex.py [-d] [-p <ai_color>] [-s <board_size>]')
        print('.  or: RandomHex.py [--debug] [--player=<ai_color>] [--size=<board_size>]')
        sys.exit(2)

    # default arguments
    arg_player = "RED"
    arg_size = 7
    arg_debug = False
    for opt, arg in opts:
        if opt in ("-d","--debug"):
            arg_debug = True
        elif opt in ("-p","--player"):
            arg_player = arg.upper()
            if not arg_player in ["RED","BLUE"]:
                print('Error: Invalid player, should be either "RED" or "BLUE".')
                sys.exit(2)
        elif opt in ("-s","--size"):
            try:
                arg_size = int(arg)
                if arg_size<=0 or arg_size>26:
                    raise Exception()
            except Exception:
                print('Error: Invalid size, should be integer in [1,26].')
                sys.exit(2)

    # print("# player: {}".format(arg_player))
    # print("# size: {}".format(arg_size))

    # initialize the game
    hex_board = [[VALUE_EMPTY for j in range(arg_size)] for i in range(arg_size)]


############ start of extra variable declaration ############
    empty_spot_dict = {}
    for i in range(arg_size):
        for j in range(arg_size):
                empty_spot_dict[(i,j)] = VALUE_EMPTY
############  end of extra variable declaratio   ############
    while(True):

        if arg_player=="RED":
            # RED playes first
            c_pos = my_strategy(hex_board, arg_size, empty_spot_dict, RED_PLAYER)
            print("c_pos chosen by RED following my strategy:", c_pos)
            c_inp = pos_to_inp(c_pos, arg_size)
            print(c_inp)
        else:
	    # wait for opponent
            c_inp = input()
            c_pos = inp_to_pos(c_inp, arg_size)

        # RED MOVES
        update_board(hex_board, c_pos, VALUE_RED, arg_size)
	# added line
        empty_spot_dict.pop(c_pos)

        if arg_debug:
            print_board(hex_board, arg_size)

        if arg_player=="BLUE":
	    # BLUE playes
            c_pos = my_strategy(hex_board, arg_size, empty_spot_dict, BLUE_PLAYER)
            print("c_pos chosen by BLUE following my strategy:", c_pos)
            c_inp = pos_to_inp(c_pos, arg_size)
            print(c_inp)
        else:
            # wait for opponent
            c_inp = input()
            c_pos = inp_to_pos(c_inp, arg_size)

        # BLUE MOVES
        update_board(hex_board, c_pos, VALUE_BLUE, arg_size)
        # added line
        empty_spot_dict.pop(c_pos)

        if arg_debug:
            print_board(hex_board, arg_size)


if __name__=="__main__":
    main(sys.argv[1:])
