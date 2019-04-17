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
        self.piece_ranks = {'p': 1,
                            'n': 3,
                            'b': 4,
                            'r': 5,
                            'q': 10,
                            'k': -1}
        
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
        self.trackedKing = (False, None)
        self.move_counter = 5
        self.moves_to_kings = 0
        self.interest_squares = [34,35,60]
        
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
        if (self.move_counter == 0 and self.color == chess.WHITE):
            return 52
        elif(self.move_counter == 0 and self.color == chess.BLACK):
            return 12

        new_senses = set(possible_sense) - set([0,1,2,3,4,5,6,7,8,15,16,18,19,20,21,23,24,26,29,31,32,34,37,39,40,42,43,44,45,47,48,55,56,57,58,59,60,61,62,63])
        new_senses_list = list(new_senses)
        print('possible senses', list(new_senses))
        print('possible moves', possible_moves)
        choosing = True
        while choosing:

            choice = random.choice(new_senses_list)
            if choice not in self.sensestaken:
                self.sensestaken += [choice]
                # print(self.sensestaken)
                choosing = False
                print(choice)
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
        kingRecentlyTracked = False
        for square, piece in sense_result:
            if piece != None:
                if piece.symbol() == 'k':
                    self.trackedKing = (True, square)
                    recentlyTracked = True
            self.board.set_piece_at(square, piece)

        if kingRecentlyTracked == False:
            self.trackedKing = (False, self.trackedKing[1])

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
        print(self.board.legal_moves)
        # print(possible_moves)
        our_pieces_moves = []

        for choice in possible_moves:
            # print(choice.from_square)
            # print(our_pieces)
            if choice.from_square not in locations:
                locations.append(choice.from_square)
                # print(self.board.piece_at(choice.from_square))
                # print(choice)
                # print(self.board.piece_at(choice.from_square).color)
                our_pieces_moves.append((self.board.piece_at(choice.from_square),self.piece_ranks[self.board.piece_at(choice.from_square).symbol().lower()], choice))
            else:
                # print(self.board.piece_at(choice.from_square))
                # print(choice)
                our_pieces_moves.append((self.board.piece_at(choice.from_square),self.piece_ranks[self.board.piece_at(choice.from_square).symbol().lower()], choice))

        # print(locations)
        # print(len(our_pieces))
        for i in our_pieces_moves:
            print(i)


        print("SORTED MOVES LIST")
        for i in our_pieces_moves:
            print(i)


            # print(i.piece_type, i.color, i.symbol())

        moves_to_king = 0

        the_move_index = self.find_best_move(our_pieces_moves, possible_moves, moves_to_king)
        print(the_move_index, len(our_pieces_moves))
        print(our_pieces_moves[the_move_index])
        if the_move_index < len(our_pieces_moves):
            return our_pieces_moves[the_move_index][2]
        else:
            return our_pieces_moves[the_move_index % len(our_pieces_moves)][2]





    def find_best_move(self,our_pieces_moves, possible_moves, moves_to_king):
        moves_to_king += 1
        our_pieces_moves.sort(key=lambda tup: tup[1], reverse=True)
        boards_list = [self.board.copy() for i in range(len(our_pieces_moves))]
        best_move = -1

        while moves_to_king < 6:
            for move_index in range(len(our_pieces_moves)):
                new_moves_list = []
                boards_list[move_index].set_piece_at(our_pieces_moves[move_index][2].to_square, our_pieces_moves[move_index][0])
                boards_list[move_index].remove_piece_at(our_pieces_moves[move_index][2].from_square)
                # for poss_next_move_index in range(len(our_pieces_moves)):
                #             #     if our_pieces_moves[poss_next_move_index][2] in boards_list[move_index].legal_moves:
                #             #         new_moves_list += [our_pieces_moves[poss_next_move_index]]
                #             #
                #             # print(new_moves_list)
                for i in boards_list[move_index].legal_moves:
                    new_moves_list.append((boards_list[move_index].piece_at(i.from_square),self.piece_ranks[boards_list[move_index].piece_at(i.from_square).symbol().lower()], i,))


                # if the king is found then return this move index
                for i in new_moves_list:
                    print(i[2].to_square)
                    if i[2].to_square in self.interest_squares:
                        print('here')
                        return move_index
                if moves_to_king > 6:
                    return random.randint(0,len(our_pieces_moves))
                else:
                    return self.find_best_move(new_moves_list, possible_moves, moves_to_king)
        return random.randint(0,len(our_pieces_moves))











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
