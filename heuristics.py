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
        score += tile_values[player.first_piece.tile.x][player.first_piece.tile.y]
    return max(score, 0)


def height_heuristic(game_state: Board, current_player: Player, enemy_player: Player):
    """
    Returns the difference between the sum of heights of the current player and the sum of heights of the enemy player
    """
    score = 0
    score += game_state.get_height(current_player.first_piece.tile.x, current_player.first_piece.tile.y)
    score += game_state.get_height(current_player.second_piece.tile.x, current_player.second_piece.tile.y)
    score -= game_state.get_height(enemy_player.first_piece.tile.x, enemy_player.first_piece.tile.y)
    score -= game_state.get_height(enemy_player.second_piece.tile.x, enemy_player.second_piece.tile.y)
    return 0 if score < 0 else score


def build_height_heuristic(game_state: Board):
    score = 0
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            score += Board.get_height(game_state, x, y) * 5
    return score


def adjacent_height(game_state: Board, x_1, y_1, x_2, y_2):
    score = 0
    for players_tile in [[x_1, y_1], [x_2, y_2]]:
        adjacent_tile = Board.get_adjacent_tiles(game_state, players_tile[0], players_tile[1])
        for tile in adjacent_tile:
            if Board.get_height(game_state, Tile.get_x(tile), Tile.get_y(tile)) - \
                    Board.get_height(game_state, players_tile[0], players_tile[1]) == 1:
                score += Board.get_height(game_state, Tile.get_x(tile), Tile.get_y(tile))
    return score


# todo: the locations represent the player's pieces locations, not the tile they build on. I don't think this was
#  the intention
def distance_heuristic(x_1, y_1, x_2, y_2, s_x_1, s_y_1, s_x_2, s_y_2):
    score = util.manhattanDistance([x_1, y_1], [s_x_1, s_y_1]) + \
            util.manhattanDistance([x_1, y_1], [s_x_2, s_y_2]) + util.manhattanDistance([x_2, y_2], [s_x_2, s_y_2]) + \
            util.manhattanDistance([x_2, y_2], [s_x_1, s_y_1])
    score -= min((util.manhattanDistance([x_1, y_1], [s_x_1, s_y_1]) +
                  util.manhattanDistance([x_2, y_2], [s_x_1, s_y_1])),
                 (util.manhattanDistance([x_1, y_1], [s_x_2, s_y_2]) +
                  util.manhattanDistance([x_2, y_2], [s_x_2, s_y_2])))
    return score


def block_heuristic(game_state: Board, s_x_1, s_y_1, s_x_2, s_y_2):
    """
    tries to block the enemy
    """
    score = 0
    for players_tile in [[s_x_1, s_y_1], [s_x_2, s_y_2]]:
        adjacent_tile_1 = Board.get_adjacent_tiles(game_state, players_tile[0], players_tile[1])
        for tile in adjacent_tile_1:
            if Board.get_height(game_state, Tile.get_x(tile), Tile.get_y(tile)) - \
                    Board.get_height(game_state, players_tile[0], players_tile[1]) > 1:
                score += 10
    return score


def setup_heuristic():
    pass


def evaluation_function(game_state: Board, current_player: Player, enemy_player: Player):
    score = 0
    if game_state.get_phase() == GamePhase.SETUP:
        return tile_value(current_player)
    else:
        x_1 = current_player.first_piece.tile.x
        y_1 = current_player.first_piece.tile.y
        x_2 = current_player.second_piece.tile.x
        y_2 = current_player.second_piece.tile.y
        s_x_1 = enemy_player.first_piece.tile.x
        s_y_1 = enemy_player.first_piece.tile.y
        s_x_2 = enemy_player.second_piece.tile.x
        s_y_2 = enemy_player.second_piece.tile.y

        if game_state.get_phase() == GamePhase.MOVE:
            # todo I think that the height heuristic and distance heuristic should have higher values
            # todo maybe height > distance > adjacent > tile_value ?
            score += tile_value(current_player)  # the tiles in the center have higher heuristic values
            score += height_heuristic(game_state, current_player, enemy_player)
            # returns the level that the player's pieces are on
            score += distance_heuristic(x_1, y_1, x_2, y_2, s_x_1, s_y_1, s_x_2, s_y_2)
            # heuristic based on the Manhattan distance from the opponent's pieces
            score += adjacent_height(game_state, x_1, y_1, x_2, y_2)
            # checks whether there is a adjacent tile with height = player's height + 1

        elif game_state.get_phase() == GamePhase.BUILD:
            score += build_height_heuristic(game_state)  # buildings with higher level get larger heuristic value
            score += block_heuristic(game_state, s_x_1, s_y_1, s_x_2, s_y_2)  # tries to block the second player
    return score
