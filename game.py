from board import *
from player import Player
from move import Move
from minimax import *

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

    def play_agents_versus(self, agent_1: Agent, agent_2: Agent):
        player_1, player_2 = Player(1), Player(2)
        # Setup p1
        move_1 = agent_1.get_action(self.board, player_1)
        self.board.add_move(player_1, move_1)
        move_2 = agent_1.get_action(self.board, player_1)
        self.board.add_move(player_1, move_2)

        # Setup p2
        move_3 = agent_2.get_action(self.board, player_2)
        self.board.add_move(player_2, move_3)
        move_4 = agent_2.get_action(self.board, player_2)
        self.board.add_move(player_2, move_4)

        current_player = player_1
        current_agent = agent_1
        while not self.is_winner(player_1) and not self.is_winner(player_2):
            move = current_agent.get_action(self.board, current_player)
            if not move:
                break
            self.board.add_move(current_player, move)
            current_player = player_2 if current_player == player_1 else player_1
            current_agent = agent_2 if current_agent == agent_1 else agent_1


if __name__ == "__main__":
    game = GameEngine()
    game.play_test()