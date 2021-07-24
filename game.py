from board import *
from player import Player
from move import Move


class GameEngine:
    def __init__(self):
        self.board = Board()

    def is_winner(self, player: Player):
        if player.first_piece and player.second_piece:
            if player.first_piece.tile.height == 3 or \
                    player.second_piece.tile.height == 3:
                print(f'Player {player} has won!')
                return True
        return False

    def play_test(self):
        player_1 = Player(1)
        player_2 = Player(2)
        while not self.is_winner(player_1) and not self.is_winner(player_2):
            piece_1_p1 = self.board.add_move(player_1, Move(self.board[0, 0]))
            print(self.board)
            piece_2_p1 = self.board.add_move(player_1, Move(self.board[2, 2]))
            print(self.board)
            piece_1_p2 = self.board.add_move(player_2, Move(self.board[3, 3]))
            print(self.board)
            piece_2_p2 = self.board.add_move(player_2, Move(self.board[4, 3]))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[1, 0], piece_1_p1))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[1, 1], piece_1_p1))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[4, 4], piece_2_p2))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[4, 3], piece_2_p2))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[0, 0], piece_1_p1))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[0, 1], piece_1_p1))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[3, 4], piece_2_p2))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[4, 4], piece_2_p2))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[0, 1], piece_1_p1))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[1, 1], piece_1_p1))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[4, 3], piece_1_p2))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[4, 4], piece_1_p2))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[0, 0], piece_1_p1))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[0, 1], piece_1_p1))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[3, 3], piece_1_p2))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[4, 3], piece_1_p2))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[1, 2], piece_2_p1))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[1, 1], piece_2_p1))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[2, 4], piece_2_p2))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[3, 4], piece_2_p2))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[1, 0], piece_1_p1))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[0, 0], piece_1_p1))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[3, 4], piece_2_p2))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[2, 4], piece_2_p2))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[0, 0], piece_1_p1))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[1, 0], piece_1_p1))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[4, 4], piece_2_p2))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[4, 3], piece_2_p2))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[0, 1], piece_1_p1))
            print(self.board)
            self.board.add_move(player_1, Move(self.board[0, 0], piece_1_p1))
            print(self.board)
            self.board.add_move(player_2, Move(self.board[4, 3], piece_2_p2))
            print(self.board)


if __name__ == "__main__":
    game = GameEngine()
    game.play_test()