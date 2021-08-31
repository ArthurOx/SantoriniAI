import pandas
import seaborn
from matplotlib import pyplot
from board import *
from feature_extractor import extractor
from player import Player
from move import *
from monte_carlo_agent import *
from minimax_agent import *
from reinforcement_learning_agent import QLearningAgent, ApproximateQAgent
from random_agent import RandomAgent
from heuristics import *
# from test_minimax import *


class GameEngine:
    def __init__(self, display_in_gui=False):
        self.board = Board(Player(1), Player(2))
        self.display_in_gui = display_in_gui

    """
    Player 1 plays with Agent 1, 2 with 2.
    :return winner
    """
    def play_agents_versus(self, agent_1: Agent, agent_2: Agent,
                           show_board=False, show_messages=True, save_file=None):
        player_1, player_2 = self.board.get_players()
        # Setup p1
        move_1 = agent_1.get_action(self.board, player_1)
        self.board.add_move(player_1, move_1, save_file=save_file)
        print(self.board)

        move_2 = agent_1.get_action(self.board, player_1)
        self.board.add_move(player_1, move_2, save_file=save_file)
        print(self.board)

        # Setup p2
        # legal_moves = self.board.get_legal_moves(player_2)
        # if not legal_moves:
        #     return []
        # move_3 = random.choice(legal_moves)
        move_3 = agent_2.get_action(self.board, player_2)
        self.board.add_move(player_2, move_3)
        if show_board:
            print(self.board)

        move_4 = agent_2.get_action(self.board, player_2)
        self.board.add_move(player_2, move_4, save_file=save_file)

        count_moves = 1
        current_player = player_1
        current_agent = agent_1
        while True:
            for phase in [GamePhase.MOVE, GamePhase.BUILD]:
                if show_board:
                    print(self.board)
                move = current_agent.get_action(self.board, current_player)
                if not move:
                    # If current player has legal moves means enemy lost
                    if self.board.get_legal_moves(current_player):
                        current_player = player_2 if current_player == player_1 else player_1
                    if show_messages:
                        print(f"Player {current_player} lost for being out of legal moves.")
                        print(f"Game ended in a total of {count_moves} moves.")
                    if save_file:
                        save_file.write('Game Ended: Tie\n')
                    self.board.clear()
                    return player_1 if current_player == player_2 else player_2
                self.board.add_move(current_player, move, save_file=save_file)
                if phase == GamePhase.MOVE and self.board.is_on_height_3(current_player):
                    if show_board:
                        print(self.board)
                    if show_messages:
                        print(f"Player {current_player} won!")
                        print(f"Game ended in a total of {count_moves} moves.")
                    if save_file:
                        save_file.write(f'Game Ended: Player {current_player} won!\n')
                    self.board.clear()
                    return current_player
                current_agent.record_iteration(self.board, move, player_1)
            current_player = player_2 if current_player == player_1 else player_1
            current_agent = agent_2 if current_agent == agent_1 else agent_1
            count_moves += 1

    def versus_multiple_rounds(self, agent_1: Agent, agent_2: Agent, rounds: int, reset_1=False, reset_2=False):
        agent_1_wins = 0
        agent_2_wins = 0
        counter = 1
        for _ in range(rounds):
            result = self.play_agents_versus(agent_1, agent_2, show_messages=False, show_board=True)
            if result.number == 1:
                agent_1_wins += 1
            else:
                agent_2_wins += 1
            self.board.clear()
            # todo
            if reset_1 is True:
                agent_1.reset_minimax()
            if reset_2 is True:
                agent_2.reset_minimax()
            print(f"Rounds: {counter}. A1 {agent_1} Wins: {agent_1_wins}, A2 {agent_2} Wins: {agent_2_wins}")
            counter += 1
        print(f"Rounds: {rounds}. A1 {agent_1} Wins: {agent_1_wins}, A2 {agent_2} Wins: {agent_2_wins}")


def train(epsilon=0.05, gamma=0.8, alpha=0.2, episodes=0):
    scores = []
    learning_agent = QLearningAgent(epsilon, gamma, alpha, episodes)
    for i in range(episodes):
        game = GameEngine()
        learning_agent.start_episode()
        game.play_agents_versus(learning_agent, MonteCarloAgent(10), False, False)
        score = learning_agent.end_episode()

        if score != -1:
            scores.append(score)
    return scores


def tune(alphas, epsilons, gammas, episodes=2000):
    scores = dict()
    for alpha in alphas:
        for epsilon in epsilons:
            for gamma in gammas:
                title = f'a: {alpha}, e: {epsilon}, g: {gamma}'
                print('-' * (21 + len(title)) + f'\nTraining with values {title}\n' + '-' * (21 + len(title)))
                scores[title] = train(alpha, epsilon, gamma, episodes)

    df = pandas.DataFrame(scores)
    with open('scores.tsv', 'w+') as f:
        f.write(df.to_csv(sep='\t'))
    seaborn.lineplot(data=df, palette='colorblind')
    pyplot.savefig('gamma.png')


if __name__ == "__main__":
    # game = GameEngine()
    # random_agent_1 = RandomAgent()
    # random_agent_2 = RandomAgent()
    # with open('renderer/text.log', 'w+') as f:
    #     winner = game.play_agents_versus(random_agent_1, random_agent_2, True, save_file=f)
    #     print(f"Player {winner} won!")
    # game.versus_multiple_rounds(random_agent_1, random_agent_2, 1000)
    # minimax_agent = MinMax(evaluation_function)
    # minimax_agent_2 = MinMax(evaluation_function)
    # ab_agent = AlphaBeta(evaluation_function)
    # mcst = MonteCarloAgent(500)
    # winner = game.play_agents_versus(ab_agent, mcst, True)
    # game.versus_multiple_rounds(minimax_agent, random_agent_1, 100)
    # game.versus_multiple_rounds(minimax_agent, minimax_agent_2, 10)

    # test ideas:
    #   learn against random (hyp: long but correct),
    #   against minmax (hyp: upper bounded by minmax perf),
    #   against own last iteration or against another QLearnAgent
    tune([0.1, 0.3, 0.5], [0.05, 0.1], [0.3, 0.5, 0.8])
