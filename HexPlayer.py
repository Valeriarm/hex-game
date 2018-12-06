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
import statistics

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
MAX_DEPTH = 8

#========= The heuristic function and helper functions =========
def neighbours(pos, size):
    # i is letter and j is number
    (i, j) = pos
    neighbour_list = []
    possible_pos_list = [(i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j)]
    for possible_pos in possible_pos_list:
        if (check_pos(possible_pos, size)):
            neighbour_list.append(possible_pos)
    return neighbour_list

def bridge_ends(pos, size):
    # i is letter and j is number
    (i, j) = pos
    ends_list = []
    possible_ends_list = [(i+2, j-1), (i+1, j-2), (i+1, j+1), (i-1, j-1), (i-1, j+2), (i-2, j+1)]
    for possible_pos in possible_ends_list:
        if (check_pos(possible_pos, size)):
            ends_list.append(possible_pos)
    return ends_list

def bridging_factor(board, size):
	pass

def neighbouring_factor(board, size):
	pass

def num_potential_connection_spot(board, size):
    # the average flexibility
    score = 0
    for i in range(size):
        for j in range(size):
            current_player = board[i][j]
            if current_player != 0:
                neighbours_list = neighbours((i,j), size)
                for n in neighbours_list:
                    if board[n[0]][n[1]] == 0:
                        score += current_player
    return score

def distribution_evenlly_penalty_score(red_num_occupancy_list, blue_num_occupancy_list):
	red_num_occupancy_list.sort()
	blue_num_occupancy_list.sort() # small to large
	length = len(red_num_occupancy_list)
	if length != len(blue_num_occupancy_list):
		print("WTF")
		sys.exit(2)

	if len(red_num_occupancy_list) <= 3:
		return (red_num_occupancy_list[-1] - red_num_occupancy_list[0]) - (blue_num_occupancy_list[-1] - blue_num_occupancy_list[0])
	else:
		red_max_list = red_num_occupancy_list[:length//4]
		red_min_list = red_num_occupancy_list[-(length//4):]
		blue_max_list = blue_num_occupancy_list[:length//4]
		blue_min_list = blue_num_occupancy_list[-(length//4):]
		score = 0
		for i in range(len(red_max_list)):
			score += (red_max_list[i] - red_min_list[i]) - (blue_max_list[i] - blue_min_list[i])
		return score

def straightness_row(board, size):
    score = 0
    red_num_occupancy_row = []
    blue_num_occupancy_row = []
    red_count = 0
    blue_count = 0
    for i in range(size):
        for j in range(size):
            value = board[i][j]
            if value == RED_PLAYER:
                red_count += 1
            elif value == BLUE_PLAYER:
                blue_count += 1
        if red_count > (size // 3):
            score += 5
        if blue_count > (size // 2):
            score += 5
        red_num_occupancy_row.append(red_count)
        blue_num_occupancy_row.append(blue_count)
        red_count = 0
        blue_count = 0
	# if distribution too even
    score_evenness = distribution_evenlly_penalty_score(red_num_occupancy_row, blue_num_occupancy_row)
    return score + score_evenness

def straightness_col(board, size):
	# BLUE should follow col
    score = 0
    red_num_occupancy_col = []
    blue_num_occupancy_col = []
    red_count = 0
    blue_count = 0
    for i in range(size):
        for j in range(size):
            value = board[j][i]
            if value == RED_PLAYER:
                red_count += 1
            elif value == BLUE_PLAYER:
                blue_count += 1
        if red_count > (size // 2):
            score -= 5
        if blue_count > (size // 3):
            score -= 5
        red_num_occupancy_col.append(red_count)
        blue_num_occupancy_col.append(blue_count)
        red_count = 0
        blue_count = 0
	# if distribution too even
    score_evenness = distribution_evenlly_penalty_score(red_num_occupancy_col, blue_num_occupancy_col)
    return score + score_evenness

def heuristic_function(current_board, empty_position_dict, size):
    '''
	RED is MAX
    things I want to consider:
	0. centerness
    1. liberty
    2. vulnerability
	3. completeness
    '''
    h1 = num_potential_connection_spot(current_board, size)
    h2 = straightness_row(current_board, size)
    h3 = straightness_col(current_board,size)
    return h1 + h2 + h3

#========= The Minimax method with alpha-beta pruning =========
# http://aima.cs.berkeley.edu/python/games.html
def max_value_pos(board, empty_position_dict, alpha, beta, depth, which_player, size, pos = None):
    print("in max_value_pos with current pos:", pos)
    if (depth >= MAX_DEPTH or len(empty_position_dict) == 0):
        print("terminate at 11 with pos:", pos)
        return (heuristic_function(board, empty_position_dict, size), pos)

    v = -1.0e40 # neg infinity

    for potential_pos in list(empty_position_dict):
        print("potential_pos_in_max:", potential_pos)
        print("board_in_max:", board)
        print("empty_positions in max:", empty_position_dict.keys())
        if not try_update_board(board, potential_pos, which_player, size):
            print("terminate at 12 with v and pos:", v, pos)
            return (v, pos)
        empty_position_dict.pop(potential_pos)
        v_from_min, pos_from_min = min_value_pos(board, empty_position_dict, alpha, beta, depth+1, -1 * which_player, size, potential_pos)
        if (v_from_min > v):
            v = v_from_min
            pos = pos_from_min
            # v = max(v, v_from_min)
        if v >= beta:
            print("terminate at 13 with v and pos:", v, pos)
            return (v, pos)
        alpha = max(alpha, v)
    print("terminate at 14 with v and pos:", v, pos)
    return (v, pos)

def min_value_pos(board, empty_position_dict, alpha, beta, depth, which_player, size, pos = None):
    print("in min_value_pos with current pos:", pos)
    if (depth >= MAX_DEPTH or len(empty_position_dict) == 0):
        print("terminate at 21 with pos:", pos)
        return (heuristic_function(board, empty_position_dict, size), pos)

    v = 1.0e40 # pos infinity

    for potential_pos in list(empty_position_dict):
        print("potential_pos_in_min:", potential_pos)
        print("board_in_min:", board)
        print("empty_positions in min:", empty_position_dict.keys())
        if not try_update_board(board, potential_pos, which_player, size):
            print("terminate at 22 with v and pos:", v, pos)
            return (v, pos)
        empty_position_dict.pop(potential_pos)
        v_from_max, pos_from_max = max_value_pos(board, empty_position_dict, alpha, beta, depth+1, -1 * which_player, size, potential_pos)
        if (v_from_max < v):
            v = v_from_max
            pos = pos_from_max
        # v = min(v, v_from_max)
        if v <= alpha:
            print("terminate at 23 with v and pos:", v, pos)
            return (v, pos)
        beta = min(beta, v)
    print("terminate at 24 with v and pos:", v, pos)
    return (v, pos)

def alpha_beta_game_tree_search(board, size, empty_position_dict, which_player):
    if which_player == RED_PLAYER:
        (v, final) =  max_value_pos(board, empty_position_dict, -1.0e40, 1.0e40, 0, which_player, size)
    else:
        (v, final) =  min_value_pos(board, empty_position_dict, -1.0e40, 1.0e40, 0, which_player, size)
    print("final:", final)
    print("v:", v)
    return final

#========= The all-in-one function =========

def my_strategy(board, size, empty_pos_dict, which_player):
    if len(empty_pos_dict)==0:
        sys.exit(0)
    temp_board = copy.deepcopy(board)
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
    # red_pos_list = []
    # blue_pos_list = []
############  end of extra variable declaratio   ############
    while(True):

        if arg_player=="RED":
            # RED playes first
            c_pos = my_strategy(hex_board, arg_size, empty_spot_dict, RED_PLAYER)
            # print("c_pos chosen by RED following my strategy:", c_pos)
            c_inp = pos_to_inp(c_pos, arg_size)
            print(c_inp)
        else:
	    # wait for opponent
            c_inp = input()
            c_pos = inp_to_pos(c_inp, arg_size)

        # RED MOVES
        # print("before updating")
        # print()
        # print(hex_board)
        # print(c_pos)
        update_board(hex_board, c_pos, VALUE_RED, arg_size)
        # print("after updating")
	# added lines
        empty_spot_dict.pop(c_pos)

        if arg_debug:
            print_board(hex_board, arg_size)

        if arg_player=="BLUE":
	    # BLUE playes
            c_pos = my_strategy(hex_board, arg_size, empty_spot_dict, BLUE_PLAYER)
            # print("c_pos chosen by BLUE following my strategy:", c_pos)
            c_inp = pos_to_inp(c_pos, arg_size)
            print(c_inp)
        else:
            # wait for opponent
            c_inp = input()
            c_pos = inp_to_pos(c_inp, arg_size)

        # BLUE MOVES
        update_board(hex_board, c_pos, VALUE_BLUE, arg_size)
        # added lines
        empty_spot_dict.pop(c_pos)

        if arg_debug:
            print_board(hex_board, arg_size)


if __name__=="__main__":
    main(sys.argv[1:])
