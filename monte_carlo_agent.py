

from minimax_agent import *
import operator
import random


class MonteCarloAgent(Agent):

    def __init__(self, simulations_num):
        super().__init__()
        super()
        self.simulations_num = simulations_num
        self.current_board = None
    def __str__(self):
        return "Monte carlo Agent"
    def is_end_game(self, player_id, next_move_dict, first_move):
        for player in self.current_board.get_players():
            if self.current_board.is_winner(player):
                if player == player_id:
                    next_move_dict[first_move] += 1
                return True
        return False

    def get_action(self, game_state, player):
        self.current_board = game_state.get_copy()
        legal_moves = self.current_board.get_legal_moves(player)
        next_move_dict = {}
        for move in legal_moves:
            next_move_dict[move] = 0
        for i in range(self.simulations_num):
            self.simulate(player,game_state, next_move_dict)
        if len(next_move_dict)==0:
            return None
        return max(next_move_dict.items(), key=operator.itemgetter(1))[0]

    def simulate(self, player,game_state, next_move_dict):
        self.current_board = game_state.get_copy()
        if next_move_dict is None or len(next_move_dict)==0:
            return
        first_next_move = random.choice(list(next_move_dict.keys()))
        self.current_board.add_move(player, first_next_move)
        if self.current_board.is_winner(player):
            next_move_dict[first_next_move] += 1
            return
        while not self.is_end_game(player, next_move_dict, first_next_move):
            for o_player in self.current_board.get_players():
                available_moves = self.current_board.get_legal_moves(o_player)
                if available_moves is None or available_moves is [] or len(available_moves)==0:
                    return
                else:
                    random_move = random.choice(available_moves)
                    self.current_board.add_move(o_player, random_move)

