import pandas
import seaborn
from matplotlib import pyplot
from board import *
from player import Player
from move import *
from monte_carlo_agent import *
from minimax_agent import *
from reinforcement_learning_agent import QLearningAgent
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
        if show_board:
            print(self.board)
        move_2 = agent_1.get_action(self.board, player_1)
        self.board.add_move(player_1, move_2)
        if show_board:
            print(self.board)

        # Setup p2
        move_3 = agent_2.get_action(self.board, player_2)
        self.board.add_move(player_2, move_3)
        if show_board:
            print(self.board)

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
                    # If current player has legal moves means enemy lost
                    if self.board.get_legal_moves(current_player):
                        current_player = player_2 if current_player == player_1 else player_1
                    if show_messages:
                        print(f"Player {current_player} lost for being out of legal moves.")
                        print(f"Game ended in a total of {count_moves} moves.")
                    return player_1 if current_player == player_2 else player_2
                self.board.add_move(current_player, move)
                if phase == GamePhase.MOVE and self.board.is_winner(current_player):
                    if show_board:
                        print(self.board)
                    if show_messages:
                        print(f"Player {current_player} won!")
                        print(f"Game ended in a total of {count_moves} moves.")
                    return current_player
                if current_player == player_1:
                    agent_1.record_iteration(self.board, move, player_1)
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
            self.board.clear()
        print(f"Rounds: {rounds}. A1 {agent_1} Wins: {agent_1_wins}, A2 {agent_2} Wins: {agent_2_wins}")


def train(alpha, epsilon, gamma, episodes):
    scores = []
    learning_agent = QLearningAgent(alpha=alpha, epsilon=epsilon, gamma=gamma, train_episodes=episodes)
    for i in range(learning_agent.train_episodes):
        game = GameEngine()
        learning_agent.start_episode()
        game.play_agents_versus(learning_agent, RandomAgent(), False, False)
        score = learning_agent.end_episode()

        if score != -1:
            scores.append(score)
    return scores


def tune(alphas, epsilons, gammas, episodes=200):
    scores = dict()
    for alpha in alphas:
        for epsilon in epsilons:
            for gamma in gammas:
                title = f'α: {alpha}, ε: {epsilon}, γ: {gamma}'
                print('-' * (21 + len(title)) + f'\nTraining with values {title}\n' + '-' * (21 + len(title)))
                scores[title] = train(alpha, epsilon, gamma, episodes)

    seaborn.lineplot(data=pandas.DataFrame(scores))
    [seaborn.lineplot(data=pandas.DataFrame(scores)[v]) for v in scores]
    pyplot.savefig('gamma.png')


if __name__ == "__main__":
    # game = GameEngine()
    # random_agent_1 = RandomAgent()
    # random_agent_2 = RandomAgent()
    # winner = game.play_agents_versus(random_agent_1, random_agent_2, True)
    # print(f"Player {winner} won!")
    # game.versus_multiple_rounds(random_agent_1, random_agent_2, 1000)

    # with open('poo.txt', 'w+') as f:
    #     combs = [(e, g, a) for e in range(0, 101, 10) for g in range(0, 101, 10) for a in range(0, 101, 10)]
    #     bar = ProgressBar(max_value=len(combs))
    #     for e, g, a in bar(combs):
    #        minimax_agent = QLearningAgent(epsilon=e/100, gamma=g/100, alpha=a/100, numTraining=100)
    #        # winner = game.play_agents_versus(minimax_agent, minimax_agent, False)
    #        f.write('='*50 + f'\n{(e/100), (g/100), (a/100)}\n')
    #        game.versus_multiple_rounds(minimax_agent, random_agent_2, 100, f)

    # test ideas:
    #   learn against random (hyp: long but correct),
    #   against minmax (hyp: upper bounded by minmax perf),
    #   against own last iteration or against another QLearnAgent
    tune([0.5], [0.05], [0.3, 0.5, 0.8])
