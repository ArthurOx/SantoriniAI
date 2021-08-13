from agent import Agent
from board import Board
from player import Player
import random


class RandomAgent(Agent):
    def get_action(self, game_state: Board, player: Player):
        legal_moves = game_state.get_legal_moves(player)
        if not legal_moves:
            return []
        return random.choice(game_state.get_legal_moves(player))

    def __str__(self):
        return "Random Agent"
