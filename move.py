from tile import Tile


class Move:
    def __init__(self, tile: Tile, piece=None):
        self.tile = tile
        self.x = tile.x
        self.y = tile.y
        self.piece = piece


class Piece:
    def __init__(self, tile, player):
        self.tile = tile
        self.player = player

    def __str__(self):
        if self.player.number == 1:
            return 'X'
        else:
            return 'Y'
