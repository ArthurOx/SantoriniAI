from copy import copy


class Player:
    def __init__(self, number):
        self.number = number
        self.moved_piece = None
        self.first_piece = None
        self.second_piece = None

    def __hash__(self):
        return hash(self.number)

    def __eq__(self, other):
        return type(other) == type(self) and self.number == other.number

    def reset(self):
        self.__init__(self.number)

    def __str__(self):
        return str(self.number)

    def __copy__(self):
        player_copy = Player(self.number)
        player_copy.moved_piece = self.moved_piece
        if self.first_piece:
            player_copy.first_piece = copy(self.first_piece)
            player_copy.first_piece.player = player_copy
        if self.second_piece:
            player_copy.second_piece = copy(self.second_piece)
            player_copy.second_piece.player = player_copy
        return player_copy
