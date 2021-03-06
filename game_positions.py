from game_constants import BOARD_ROWS, BOARD_COLS, STR_PIECE_SIZE
from game_pieces import Piece, NoPiece
from game_colors import Color, red, blue
from game_exceptions import NotThisColorsTurn, ThisPieceCantMoveThere, InvalidStringCoordinates
import random

class Position:
    def __init__(self, as_string, color_of_turn_as_string):
        self.as_string=as_string
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.pieces[row][col]=Piece.get_piece(as_string=self.as_string[BOARD_ROWS*row+col:BOARD_ROWS*row+col+STR_PIECE_SIZE], row=row, col=col)
        self.color_of_turn=Color(as_string=color_of_turn_as_string)

    def move(self, string_coords_from, string_coords_to): # TODO: could use some delegation :|
        piece_moving=self.pieces[int(string_coords_from[0]), int(string_coords_from[1])] # TODO: check if valid int... exception handling?
        if not piece_moving.color==self.color_of_turn:
            raise NotThisColorsTurn()
        if (not Position.valid_string_coords(string_coords_from)) or (not Position.valid_string_coords(string_coords_to)):
            raise InvalidStringCoordinates()
        if not piece_moving.can_move_to(self.pieces[int(string_coords_to[0]), int(string_coords_to[1])]):
            raise ThisPieceCantMoveThere()
        if not self.pieces[int(string_coords_to[0]), int(string_coords_to[1])].is_empty_square():
            self.pieces[int(string_coords_from[0]), int(string_coords_from[1])]=NoPiece(row=int(string_coords_from[0]), col=int(string_coords_from[1]))
            self.pieces[int(string_coords_to[0]), int(string_coords_to[1])]=piece_moving
            self.color_of_turn = red if self.color_of_turn==blue else blue
            self.update_string()
            return game_move_results.MovedToEmptySquare() # TODO: args to generate specific message or sth
        else: # TODO: refactor with possible class Attack or Combar or sth
            defender_score=self.pieces[int(string_coords_to[0]), int(string_coords_to[1])].score(is_attacker=False)
            attacker_score=self.pieces[int(string_coords_from[0]), int(string_coords_from[1])].score(is_attacker=True)
            if attacker_score > defender_score:
                self.pieces[int(string_coords_from[0]), int(string_coords_from[1])]=NoPiece(row=int(string_coords_from[0]), col=int(string_coords_from[1]))
                self.pieces[int(string_coords_to[0]), int(string_coords_to[1])]=piece_moving
                self.color_of_turn = red if self.color_of_turn==blue else blue
                self.update_string()
                return game_move_results.AttackResult(succeded=True, attacker_score=attacker_score, attacker_color=piece_moving.color, defender_score=defender_score)
            else:
                self.color_of_turn = red if self.color_of_turn==blue else blue
                self.update_string()
                return game_move_results.AttackResult(succeded=False, attacker_score=attacker_score, attacker_color=piece_moving.color, defender_score=defender_score)
        

    def update_string(self):
        self.as_string = ''
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.as_string += self.pieces[row][col].as_string()
    
    def valid_string_coords(string_coords):
        if not (BOARD_ROWS >= string_coords[0] >= 0): return False # TODO: string_coords needs a class Coordinates with string conversion methods ASAP
        if not (BOARD_COLS >= string_coords[1] >= 0): return False
        return True


class PositionStringGenerator:
    def __init__(self):
        random.seed()

    def get_random_position(self):
        red_pieces=self.get_random_pieces(color_letter='r')
        blue_pieces=self.get_random_pieces(color_letter='b')
        empty_squares=self.get_empty_squares(rows=2)
        return red_pieces+empty_squares+blue_pieces

    def get_random_pieces(self, color_letter):
        pieces = []
        pieces.append(color_letter+'k')
        for n in range(10):
            pieces.append(color_letter+str(n))
        random.shuffle(pieces)
        return ''.join(pieces)

    def get_empty_squares(self, rows):
        return 'es'*rows*BOARD_COLS