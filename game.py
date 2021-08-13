import minimax_agent
from board import *
from player import Player
from move import *
from minimax_agent import *
from random_agent import RandomAgent


class GameEngine:
    def __init__(self):
        self.board = Board()

    def is_winner(self, player: Player):
        if player.first_piece and player.second_piece:
            if player.first_piece.tile.height == 3 or \
                    player.second_piece.tile.height == 3:
                return player
        return None

    """
    Player 1 plays with Agent 1, 2 with 2.
    :return winner
    """
    def play_agents_versus(self, agent_1: Agent, agent_2: Agent, show_board=False, show_messages=True):
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

        count_moves = 0
        current_player = player_1
        current_agent = agent_1
        while not self.is_winner(player_1) and not self.is_winner(player_2):
            for _ in [GamePhase.MOVE, GamePhase.BUILD]:
                move = current_agent.get_action(self.board, current_player)
                if show_board:
                    print(self.board)
                if not move:
                    if show_messages:
                        print(f"Player {current_player} lost for being out of legal moves.")
                    self.board.clear()
                    return player_1 if current_player == player_2 else player_2
                self.board.add_move(current_player, move)
            current_player = player_2 if current_player == player_1 else player_1
            current_agent = agent_2 if current_agent == agent_1 else agent_1
            count_moves += 1
        if show_messages:
            print(f"Game ended in a total of {count_moves} moves.")
        self.board.clear()
        return player_1 if self.is_winner(player_1) else player_2

    def versus_multiple_rounds(self, agent_1: Agent, agent_2: Agent, rounds: int):
        agent_1_wins = 0
        agent_2_wins = 0
        for _ in range(rounds):
            result = self.play_agents_versus(agent_1, agent_2, show_messages=False, show_board=False)
            if result.number == 1:
                agent_1_wins += 1
            else:
                agent_2_wins += 1
        print(f"Rounds: {rounds}. A1 {agent_1} Wins: {agent_1_wins}, A2 {agent_2} Wins: {agent_2_wins}")


if __name__ == "__main__":
    game = GameEngine()
    random_agent_1 = RandomAgent()
    random_agent_2 = RandomAgent()
    winner = game.play_agents_versus(random_agent_1, random_agent_2, True)
    print(f"Player {winner} won!")
    game.versus_multiple_rounds(random_agent_1, random_agent_2, 1000)
