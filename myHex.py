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

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTER2INT = {ALPHABET[i]:i for i in range(26)}
VALUE_EMPTY = 0
VALUE_RED = 1 # from letter side to letter side
VALUE_BLUE = -1 # from integer side to integer side

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
	# return False: failed
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
		# print("# Error: invalid position.")
		sys.exit(2)

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

################ Start of My Functions #####################

'''
# http://aima.cs.berkeley.edu/python/games.html
def alphabeta_search(state, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for (a, s) in successors(state):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for (a, s) in successors(state):
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    action, state = argmax(game.successors(state),
                           lambda ((a, s)): min_value(s, -infinity, infinity, 0))
    return action
'''
def closest_position(pos_L, pos_N):
	(pos_L_return, pos_N_return) = (pos_L, pos_N)
	while( not check_pos(pos_L, pos_L)):
		# update position => nearby location
	return (pos_L_return, pos_N_return)

def central_unoccupied_pos(d_board, d_size):
        central_pos = int(d_size / 2)
		return closest_position(central_pos, central_pos)

def max_path_len(d_board, d_size, which_player):
        # the closer to a straight-cut, the better
        pass

def num_potential_path(d_board, d_size, which_player):
        # the flexibility
        pass

def heuristic_function(d_board, d_size, which_player):
        pass


def my_alpha_beta(d_board, d_size):
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
        # always start at a central location
        # TODO
	return d_available_pos[0]

################ End of My functions #####################


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

	while(True):
                if arg_player=="RED":
			# RED playes first
			c_pos = strategy_random(hex_board, arg_size)
##			c_pos = my_strategy(hex_board, arg_size)
			c_inp = pos_to_inp(c_pos, arg_size)
			# introduce random time pause
			# time.sleep(random.randint(0,4))
			print(c_inp)
		else:
			# wait for opponent
			c_inp = input()
			c_pos = inp_to_pos(c_inp, arg_size)
		# RED MOVES
		update_board(hex_board, c_pos, VALUE_RED, arg_size)
		if arg_debug:
			print_board(hex_board, arg_size)

		if arg_player=="BLUE":
			# BLUE playes
			c_pos = strategy_random(hex_board, arg_size)
##			c_pos = my_strategy(hex_board, arg_size)
			c_inp = pos_to_inp(c_pos, arg_size)
			# introduce random time pause
			# time.sleep(random.randint(0,4))
			print(c_inp)
		else:
			# wait for opponent
			c_inp = input()
			c_pos = inp_to_pos(c_inp, arg_size)
		# BLUE MOVES
		update_board(hex_board, c_pos, VALUE_BLUE, arg_size)
		if arg_debug:
			print_board(hex_board, arg_size)


if __name__=="__main__":
	main(sys.argv[1:])
