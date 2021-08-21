class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 0
        self.piece = None

    def raw_representation(self):
        height_repr = f'{self.height:3b}'
        piece_repr = f'{self.piece.player.number:2b}' if self.piece is not None else '0'
        return height_repr + piece_repr

    def add_level(self):
        self.height += 1

    def __copy__(self):
        tile_copy = Tile(self.x, self.y)
        tile_copy.height = self.height
        return tile_copy

    def __str__(self):
        if not self.piece:
            if self.height == 0:
                return f'  '
            if self.height == 4:
                return f' Ø'
            return f' {self.height}'
        if self.height == 0:
            return f'{self.piece} '
        if self.height == 4:
            return f' Ø'
        return f'{self.piece}{self.height}'

    def __eq__(self, other):
        return self.x == other.x and \
            self.y == other.y

    def __hash__(self):
        if self.piece:
            return hash(f'{self.x}{self.y}{self.height}{self.piece.player}')
        return hash(f'{self.x}{self.y}{self.height}')
