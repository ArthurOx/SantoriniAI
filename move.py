from tile import Tile
from copy import copy


class Move:
    def __init__(self, tile: Tile, piece=None):
        self.tile = tile
        self.x = tile.x
        self.y = tile.y
        self.piece = piece

    def __copy__(self):
        move_copy = Move(copy(self.tile), copy(self.piece))
        move_copy.x = self.x
        move_copy.y = self.y
        return move_copy

    def __str__(self):
        if not self.piece:
            return f"({self.x}, {self.y})"
        return f"[Piece from ({self.piece.tile.x}, {self.piece.tile.y}) to ({self.x}, {self.y})]"


class Piece:
    def __init__(self, tile, player):
        self.tile = tile
        self.player = player

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
