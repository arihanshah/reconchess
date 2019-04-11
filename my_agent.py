#!/usr/bin/env python3

"""
File Name:      my_agent.py
Authors:        Arihan Shah // Naud Ghebre
Date:           3/27/19

Description:    Python file for my agent.
Source:         Adapted from recon-chess (https://pypi.org/project/reconchess/)
"""

import random
import chess
import numpy as np
from player import Player


# TODO: Rename this class to what you would like your bot to be named during the game.
class Dior(Player):

    def __init__(self):
        self.board = None
        self.color = None
        self.my_piece_captured_square = None
        
    def handle_game_start(self, color, board):
        """
        This function is called at the start of the game.

        :param color: chess.BLACK or chess.WHITE -- your color assignment for the game
        :param board: chess.Board -- initial board state
        :return:
        """
        # TODO: implement this method
        self.board = board
        self.color = color
        self.sensestaken = []
        self.move_counter = 5
        
    def handle_opponent_move_result(self, captured_piece, captured_square):
        """
        This function is called at the start of your turn and gives you the chance to update your board.

        :param captured_piece: bool - true if your opponents captured your piece with their last move
        :param captured_square: chess.Square - position where your piece was captured
        """
        self.my_piece_captured_square = captured_square
        if captured_piece:
            self.board.remove_piece_at(captured_square)

    def choose_sense(self, possible_sense, possible_moves, seconds_left):
        """
        This function is called to choose a square to perform a sense on.

        :param possible_sense: List(chess.SQUARES) -- list of squares to sense around
        :param possible_moves: List(chess.Moves) -- list of acceptable moves based on current board
        :param seconds_left: float -- seconds left in the game

        :return: chess.SQUARE -- the center of 3x3 section of the board you want to sense
        :example: choice = chess.A1
        """
        # TODO: update this method
        new_senses = set(possible_sense) - set([0,1,2,3,4,5,6,7,8,15,16,18,19,20,21,23,24,26,29,31,32,34,37,39,40,42,43,44,45,47,48,55,56,57,58,59,60,61,62,63])
        new_senses_list = list(new_senses)
        print('possible senses', list(new_senses))
        print('possible movies', possible_moves)
        choosing = True
        while choosing:
            choice = random.choice(new_senses_list)
            if choice not in self.sensestaken:
                self.sensestaken += [choice]
                # print(self.sensestaken)
                choosing = False
                if len(self.sensestaken) == 24:
                    self.sensestaken = []
                # print(self.sensestaken)
        return choice



        
    def handle_sense_result(self, sense_result):
        """
        This is a function called after your picked your 3x3 square to sense and gives you the chance to update your
        board.

        :param sense_result: A list of tuples, where each tuple contains a :class:`Square` in the sense, and if there
                             was a piece on the square, then the corresponding :class:`chess.Piece`, otherwise `None`.
        :example:
        [
            (A8, Piece(ROOK, BLACK)), (B8, Piece(KNIGHT, BLACK)), (C8, Piece(BISHOP, BLACK)),
            (A7, Piece(PAWN, BLACK)), (B7, Piece(PAWN, BLACK)), (C7, Piece(PAWN, BLACK)),
            (A6, None), (B6, None), (C8, None)
        ]
        """
        # TODO: implement this method
        # Hint: until this method is implemented, any senses you make will be lost.

        for square, piece in sense_result:
            self.board.set_piece_at(square, piece)

    def choose_move(self, possible_moves, seconds_left):
        """
        Choose a move to enact from a list of possible moves.

        :param possible_moves: List(chess.Moves) -- list of acceptable moves based only on pieces
        :param seconds_left: float -- seconds left to make a move
        
        :return: chess.Move -- object that includes the square you're moving from to the square you're moving to
        :example: choice = chess.Move(chess.F2, chess.F4)
        
        :condition: If you intend to move a pawn for promotion other than Queen, please specify the promotion parameter
        :example: choice = chess.Move(chess.G7, chess.G8, promotion=chess.KNIGHT) *default is Queen
        """

        if self.move_counter == 0:
            self.move_counter += 1
            return chess.Move(chess.B1, chess.C3)
        elif self.move_counter == 1:
            self.move_counter += 1
            return chess.Move(chess.C3, chess.E4)
        elif self.move_counter == 2:
            self.move_counter += 1
            return chess.Move(chess.E4, chess.D6)
        elif self.move_counter == 3:
            self.move_counter += 1
            return chess.Move(chess.D6, chess.E8)
        else:
            return self.test_algo(possible_moves, seconds_left)


        # while seconds_left:
        # if self.color == chess.BLACK:
        #     target = 'e1'
        # min = 10000000
        # bestMove = None
        #
        # curboard = self.board



        # for choice in possible_moves:
        #     num_moves_to_goal = self.recursive_moves(choice, curboard, 0)
        #     print('num_moves_to_goal', num_moves_to_goal)
        #     if num_moves_to_goal < min:
        #         min = num_moves_to_goal
        #         bestMove = choice

        # return bestMove

        # choice = random.choice(possible_moves)
        # print(possible_moves)
        # print(len(possible_moves))
        # return choice
    # def recursive_moves(self, move, board, move_count):
    #     if move.to_square == 'e1':
    #
    #         return move_count + 1
    #
    #     board.push(move)
    #
    #     if move_count < 10:
    #         min = 10000000
    #         for nextmove in board.legal_moves:
    #             num_moves = self.recursive_moves(nextmove, board, move_count+1)
    #             if num_moves < min:
    #                 min = num_moves
    #         return min
    #     else:
    #
    #         return random.randint(1,70)
    #
    #
    #     board.pop()
    def test_algo(self, possible_moves, seconds_left):
        locations = []
        our_pieces = {}
        for choice in possible_moves:
            if choice.from_square not in locations:
                locations.append(choice.from_square)
                our_pieces[self.board.piece_at(choice.from_square)] = [choice]
            else:
                our_pieces[self.board.piece_at(choice.from_square)] += [choice]


        for i in our_pieces.keys():
            print('key',i)
            print('value', our_pieces[i])

            # print(i.piece_type, i.color, i.symbol())


        return random.choice(possible_moves)
        
    def handle_move_result(self, requested_move, taken_move, reason, captured_piece, captured_square):
        """
        This is a function called at the end of your turn/after your move was made and gives you the chance to update
        your board.

        :param requested_move: chess.Move -- the move you intended to make
        :param taken_move: chess.Move -- the move that was actually made
        :param reason: String -- description of the result from trying to make requested_move
        :param captured_piece: bool - true if you captured your opponents piece
        :param captured_square: chess.Square - position where you captured the piece
        """
        # TODO: implement this method
        if taken_move is not None:
            self.board.push(taken_move)
        
    def handle_game_end(self, winner_color, win_reason):  # possible GameHistory object...
        """
        This function is called at the end of the game to declare a winner.

        :param winner_color: Chess.BLACK/chess.WHITE -- the winning color
        :param win_reason: String -- the reason for the game ending
        """
        # TODO: implement this method
        pass
