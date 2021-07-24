class Player:
    def __init__(self, number):
        self.number = number
        self.moved_piece = None
        self.first_piece = None
        self.second_piece = None

    def __str__(self):
        return str(self.number)
