from board import *
from tile import *
import util

BOARD_SIZE = 5


def tile_value(player: Player):
    """
    The tiles in the middle have a higher value than those closer to edges.
    """
    score = 0
    tile_values = [[0, 1, 1, 1, 0],
                   [1, 2, 2, 2, 1],
                   [1, 2, 3, 2, 1],
                   [1, 2, 2, 2, 1],
                   [0, 1, 1, 1, 0]]
    if player.first_piece:
        score += tile_values[player.first_piece.tile.x][player.first_piece.tile.y]
    if player.second_piece:
        score += tile_values[player.second_piece.tile.x][player.second_piece.tile.y]
    return score


def height_heuristic(game_state: Board, current_player: Player, enemy_player: Player):
    score = game_state.get_height(current_player.first_piece.tile.x, current_player.first_piece.tile.y)
    score += game_state.get_height(current_player.second_piece.tile.x, current_player.second_piece.tile.y)
    score -= game_state.get_height(enemy_player.first_piece.tile.x, enemy_player.first_piece.tile.y)
    score -= game_state.get_height(enemy_player.second_piece.tile.x, enemy_player.second_piece.tile.y)
    return max(score, 0)


def available_adjacent_tiles(game_state: Board, current_player: Player, enemy_player: Player, climbing_potential_factor: float = 1):
    """
    Returns the amount of available tiles for a player to move minus the available tiles to move for the enemy player
    """
    first_player_adjacent_tiles = game_state.get_adjacent_tiles_of_player(current_player)
    first_legal_moves = {move.tile: move for move in game_state.get_legal_moves(current_player)}
    score = 0
    for tile in first_player_adjacent_tiles:
        if tile in first_legal_moves.keys():
            score += 1
            score += _get_climbing_potential(first_legal_moves[tile].piece.tile, tile) * climbing_potential_factor

    second_player_adjacent_tiles = game_state.get_adjacent_tiles_of_player(enemy_player)
    second_legal_moves = {move.tile: move for move in game_state.get_legal_moves(enemy_player)}
    for tile in second_player_adjacent_tiles:
        if tile in second_legal_moves.keys():
            score -= 1
            score -= _get_climbing_potential(second_legal_moves[tile].piece.tile, tile) * climbing_potential_factor
    return max(score, 0)


def _get_climbing_potential(from_tile: Tile, to_tile: Tile):
    """
    Returns a factor of how much we can climb. From 0 to 1 -> 1 point, 1 to 2 -> 2 points etc
    """
    if to_tile.height - from_tile.height == 1:
        if to_tile.height == 3:
            return 5
        return to_tile.height
    return 0


def _win_heuristic(game_state: Board, current_player: Player, enemy_player: Player):
    if game_state.is_on_height_3(current_player):
        return 100
    if game_state.get_phase() == GamePhase.MOVE and not game_state.get_legal_moves(enemy_player):
        return 100
    return 0

def evaluation_function(game_state: Board, current_player: Player, enemy_player: Player):
    score = 0
    if game_state.get_phase() == GamePhase.SETUP:
        return tile_value(enemy_player)
    else:
        score += tile_value(current_player)
        if game_state.get_phase() == GamePhase.MOVE:
            score += 100 * height_heuristic(game_state, current_player, enemy_player)
            score += 20 * available_adjacent_tiles(game_state, current_player, enemy_player)
            score += 200 * _win_heuristic(game_state, current_player, enemy_player)
    return score
