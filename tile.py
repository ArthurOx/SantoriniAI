class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 0
        self.piece = None

    def add_level(self):
        self.height += 1

    def __str__(self):
        if not self.piece:
            if self.height == 0:
                return f'---'
            return f'-{self.height}-'
        if self.height == 0:
            return f'-{self.piece}-'
        return f'{self.piece}{self.height}-'
