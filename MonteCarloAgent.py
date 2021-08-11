from copy import copy

from minimax import *
import operator
import random


class MonteCarloAgent(Agent):
    def __init__(self, all_players, simulations_num):
        super().__init__()
        super(self)
        self.simulations_num = simulations_num
        self.all_players = all_players
        self.current_board = None

    def is_end_game(self, player_id, next_move_dict, first_move):
        for player in self.all_players:
            if self.current_board.is_winner(player):
                if player == player_id:
                    next_move_dict[first_move] += 1
                return True
        return False

    def get_action(self, game_state, player):
        self.current_board = copy(game_state)
        legal_moves = game_state.get_legal_moves(player)
        next_move_dict = {}
        for move in legal_moves:
            next_move_dict[move] = 0
        for i in range(self.simulations_num):
            self.simulate(player, next_move_dict)

        return max(next_move_dict.items(), key=operator.itemgetter(1))[0]

    def simulate(self, player, next_move_dict):
        first_next_move = next_move_dict[random.randint(0, len(next_move_dict) - 1)]
        self.current_board.do_move(player, first_next_move)
        if self.current_board.is_winner(player):
            next_move_dict[first_next_move] += 1
            return
        while not self.is_end_game(player, next_move_dict, first_next_move):
            for o_player in self.all_players:
                available_moves = self.current_board.get_legal_moves(o_player)
                random_move = available_moves[random.randint(0, len(available_moves) - 1)]
                self.current_board.do_move(o_player, random_move)

    def stop_running(self):
        pass
