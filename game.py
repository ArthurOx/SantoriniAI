from monte_carlo_agent import *
from minimax_agent import *
from random_agent import RandomAgent
from heuristics import *


class GameEngine:
    def __init__(self, display_in_gui=False):
        self.board = Board(Player(1), Player(2))
        self.display_in_gui = display_in_gui

    """
    Player 1 plays with Agent 1, 2 with 2.
    :return winner
    """
    def play_agents_versus(self, agent_1: Agent, agent_2: Agent,
                           show_board=False, show_messages=True):
        player_1, player_2 = self.board.get_players()
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

        count_moves = 1
        current_player = player_1
        current_agent = agent_1
        while True:
            for phase in [GamePhase.MOVE, GamePhase.BUILD]:
                if show_board:
                    print(self.board)
                move = current_agent.get_action(self.board, current_player)
                if not move:
                    if show_messages:
                        print(f"Player {current_player} lost for being out of legal moves.")
                        print(f"Game ended in a total of {count_moves} moves.")
                    self.board.clear()
                    return player_1 if current_player == player_2 else player_2
                self.board.add_move(current_player, move, False)
                if phase == GamePhase.MOVE and self.board.is_winner(current_player):
                    if show_board:
                        print(self.board)
                    if show_messages:
                        print(f"Player {current_player} won!")
                        print(f"Game ended in a total of {count_moves} moves.")
                    self.board.clear()
                    return current_player
            current_player = player_2 if current_player == player_1 else player_1
            current_agent = agent_2 if current_agent == agent_1 else agent_1
            count_moves += 1

    def versus_multiple_rounds(self, agent_1: Agent, agent_2: Agent, rounds: int):
        agent_1_wins = 0
        agent_2_wins = 0
        for _ in range(rounds):
            result = self.play_agents_versus(agent_1, agent_2, show_messages=False, show_board=True)
            if result.number == 1:
                agent_1_wins += 1
            else:
                agent_2_wins += 1
        print(f"Rounds: {rounds}. A1 {agent_1} Wins: {agent_1_wins}, A2 {agent_2} Wins: {agent_2_wins}")


if __name__ == "__main__":
    game = GameEngine()
    random_agent_1 = RandomAgent()
    random_agent_2 = RandomAgent()
    # winner = game.play_agents_versus(random_agent_1, random_agent_2, True)
    # print(f"Player {winner} won!")
    # game.versus_multiple_rounds(random_agent_1, random_agent_2, 1000)
    minimax_agent = MinMax(evaluation_function)
    minimax_agent_2 = MinMax(evaluation_function)
    ab_agent = AlphaBeta(evaluation_function)
    mcst = MonteCarloAgent(500)
    winner = game.play_agents_versus(minimax_agent, mcst, True)
    # game.versus_multiple_rounds(minimax_agent, random_agent_1, 100)
    # game.versus_multiple_rounds(minimax_agent, minimax_agent_2, 10)
