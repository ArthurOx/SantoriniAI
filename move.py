from tile import Tile
from copy import copy


class Move:
    def __init__(self, tile: Tile, piece=None):
        self.tile = tile
        self.x = tile.x
        self.y = tile.y
        self.piece = piece

    def __eq__(self, other):
        return type(self) == type(other) and (
            self.tile == other.tile and self.x == other.x and self.y == other.y and self.piece == other.piece
        )

    def __hash__(self):
        return hash(self.raw_representation())

    def raw_representation(self):
        piece_repr = f'{self.piece.player.number:2b}' if self.piece is not None else '0'
        return f'{self.x:3b}{self.y:3b}{self.tile.x:3b}{self.tile.y:3b}' + piece_repr

    def __copy__(self):
        move_copy = Move(copy(self.tile), copy(self.piece))
        move_copy.x = self.x
        move_copy.y = self.y
        return move_copy

    def __str__(self):
        if not self.piece:
            return f"({self.x}, {self.y})"
        return f"[Piece from ({self.piece.tile.x}, {self.piece.tile.y}) to ({self.x}, {self.y})]"

    def __hash__(self):
        return hash(str(self))


class Piece:
    def __init__(self, tile, player):
        self.tile = tile
        self.player = player

    def __hash__(self):
        return hash(self.player) + hash(self.tile)

    def __str__(self):
        if self.player.number == 1:
            return 'ƍ'
        else:
            return '♠'

    def __copy__(self):
        tile_copy = copy(self.tile)
        piece_copy = Piece(tile_copy, self.player)
        self.tile.piece = self
        return piece_copy

    def __eq__(self, other):
        if not other:
            return False
        if not self.tile:
            if other.tile:
                return False
            return self.player.number == other.player.number
        if not other.tile:
            return False
        return self.tile.x == other.tile.x and self.tile.y == other.tile.y and self.player.number == other.player.number
