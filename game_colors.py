from game_exceptions import NoSuchColor

class Color:
    def __init__(self, as_string_or_char):
        if as_string_or_char in ['r', 'red']:
            self.string='red'
        if as_string_or_char in ['b', 'blue']:
            self.string='blue'
        raise NoSuchColor()

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.string == other.string)

    def as_char(self):
        return 'r' if self.string=='red' else 'b'

red = Color('r')
blue = Color('b')