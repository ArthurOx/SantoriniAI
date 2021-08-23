from collections import defaultdict
import random
import time
import util
from agent import Agent
from heuristics import evaluation_function


EPISODE_UPDATE_INTERVAL = 100


def all_max(arr, func):
    best_value, best_items = -float('inf'), []
    for item in arr:
        value = func(item)
        if value == best_value:
            best_items.append(item)
        elif value > best_value:
            best_value, best_items = value, [item]
    return best_items


class QLearningAgent(Agent):
    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, train_episodes=0):
        super().__init__()
        self.epsilon, self.discount, self.alpha = epsilon, gamma, alpha
        self.player_q_values = dict()

        self.train_episodes = train_episodes
        self.episode_number = 0
        self.episode_start = None
        self.train_reward, self.inference_reward, self.episode_reward = 0, 0, 0
        self.previous_state, self.previous_action = None, None

    def __str__(self):
        return "Q Learning Agent"

    def get_action(self, state, player):
        legal_actions = state.get_legal_moves(player)
        if len(legal_actions) == 0:
            return None

        action = random.choice(legal_actions) if util.flipCoin(self.epsilon) else self._get_policy(state, player)
        return action

    def record_iteration(self, state, action, player):
        # update the q_values based on this iteration's performance
        if self.previous_state is not None:
            enemy = state.get_enemy_of(player)
            reward = evaluation_function(state, player, enemy) - evaluation_function(self.previous_state, player, enemy)
            self._update(self.previous_state, self.previous_action, state, reward, player)

            # and calculate this iteration's performance into the episode
            self.episode_reward += reward
        self.previous_state, self.previous_action = state.get_copy(), action

    def start_episode(self):
        self.previous_state, self.previous_action = None, None
        self.episode_reward = 0
        if self.episode_start is None:
            self.episode_start = time.time()

        if self.episode_number == 0:
            print(f'Beginning {self.train_episodes} episodes of Training')

    def end_episode(self):
        if self.episode_number < self.train_episodes:
            self.train_reward += self.episode_reward
        else:
            self._set_to_inference_mode()
            self.inference_reward += self.episode_reward

        self.episode_number += 1
        score = -1
        if self.episode_number % EPISODE_UPDATE_INTERVAL == 0:
            score = self.train_reward / EPISODE_UPDATE_INTERVAL
            self._print_run_details()
            self.train_reward, self.inference_reward = 0, 0
            self.episode_start = time.time()
        return score

    def _get_q_value(self, state, action, player):
        try:
            return self.player_q_values[player][state][action]
        except KeyError:
            return 0

    def _get_value(self, state, player):
        legal_moves = state.get_legal_moves(player)
        if len(legal_moves) == 0:
            return 0
        return max([self._get_q_value(state, x, player) for x in legal_moves])

    def _get_policy(self, state, player):
        legal_moves = state.get_legal_moves(player)
        if len(legal_moves) == 0:
            return 0
        return random.choice(all_max(legal_moves, lambda a: self._get_q_value(state, a, player)))

    def _update(self, state, action, next_state, reward, player):
        if player not in self.player_q_values:
            self.player_q_values[player] = defaultdict(util.Counter)

        value, q_value = self._get_value(next_state, player), self._get_q_value(state, action, player)
        self.player_q_values[player][state][action] = self.alpha * (reward + self.discount * value - q_value)

    def _set_to_inference_mode(self):
        self.epsilon = 0  # no exploration
        self.alpha = 0  # no learning

    def _print_run_details(self):
        print('Agent performance update:')
        if self.episode_number <= self.train_episodes:
            print(f'\tRan for {self.episode_number}/{self.train_episodes} training episodes.')
            print(f'\tAverage rewards during training: {self.train_reward / EPISODE_UPDATE_INTERVAL}.')
            print(f'\tKnown state-action pairs: {self._count_state_action_pairs()}')
        if self.episode_number > self.train_episodes:
            inference_episodes = self.episode_number - self.train_episodes
            print(f'\tRan for {inference_episodes} inference episodes.')
            print(f'\tAverage rewards during inference: {self.inference_reward / EPISODE_UPDATE_INTERVAL}')
        print(f'\tRuntime for {EPISODE_UPDATE_INTERVAL} episodes: {(time.time() - self.episode_start)} seconds.')
        if self.episode_number == self.train_episodes:
            print('Finished Training')

    def _count_state_action_pairs(self):
        counter = 0
        for player, states in self.player_q_values.items():
            for state, actions in states.items():
                for action in actions:
                    counter += 1
        return counter


class ApproximateQAgent(QLearningAgent):
    def __init__(self, feature_extractor, epsilon=0.05, gamma=0.8, alpha=0.2, train_episodes=0):
        super().__init__(epsilon, gamma, alpha, train_episodes)
        self.feature_extractor = feature_extractor
        self.weights = util.Counter()

    def _get_q_value(self, state, action, player):
        return self.weights * self.feature_extractor(state, action, player)

    def _update(self, state, action, next_state, reward, player):
        value, q_value = self._get_value(next_state, player), self._get_q_value(state, action, player)
        for feature, f_value in self.feature_extractor(state, action, player).items():
            self.weights[feature] += self.alpha * (reward + self.discount * value - q_value) * f_value
