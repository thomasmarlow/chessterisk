import string
import game_colors
import random
from game_exceptions import NoSuchPieceSubtype

class Piece:
    def get_piece(as_string, row, col): # bk, rk, r6, b5, es, etc.
        PieceSubtype=Piece.get_subtype(as_string) # TODO: class PieceString
        return PieceSubtype(as_string=as_string, row=row, col=col)

    def get_subtype(as_string):
        if as_string[1]=='k': return Master
        if as_string=='es': return NoPiece
        if as_string[1] in string.digits:return Numbered
        raise NoSuchPieceSubtype()

    def __init__(self, as_string, row, col):
        self.color=game_colors.Color(as_string_or_char=as_string[0])
        self.row=row
        self.col=col
    
    def is_empty_square(self):
        return False

    def can_move_to(self, target_piece):
        return (target_piece.row, target_piece.col) in self.possible_moves()

    def get_straight_moves(self, distance):
        return [(self.row+distance, self.col), (self.row-distance, self.col), (self.row, self.col+distance), (self.row, self.col-distance)]

    def get_diagonal_moves(self, distance):
        return [(self.row+distance, self.col+distance), (self.row-distance, self.col+distance), (self.row-distance, self.col+distance), (self.row-distance, self.col-distance)]


class Master(Piece):
    def possible_moves(self):
        return self.get_diagonal_moves(distance=1)+self.get_straight_moves(distance=2)

    def as_string(self):
        return self.color.as_char()+'k'

    def score(self, is_attacker):
        return 1000 if is_attacker else -1


class Numbered(Piece):
    def __init__(self, as_string, row, col):
        self.number=int(as_string[1])
        super().__init__(as_string, row, col)

    def possible_moves(self):
        if self.number%2==0:
            return self.get_straight_moves(distance=1)
        else:
            return self.get_diagonal_moves(distance=1)

    def as_string(self):
        return self.color.as_char()+str(self.number)

    def score(self, is_attacker):
        random.seed()
        score=random.random()*self.number
        return (3/2)*score if is_attacker else score

class NoPiece: # null object
    def __init__(self, row, col, as_string=None):
        self.row=row
        self.col=col

    def is_empty_square(self):
        return True

    def as_string(self):
        return 'es'