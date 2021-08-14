from board import *
import util


def tile_value(player: Player):
    """
    The tiles in the middle have a higher value than those closer to edges.
    """
    score = 0
    tile_values = [[0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 0],
                   [0, 1, 2, 1, 0],
                   [0, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0]]
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


# todo: the locations represent the player's pieces locations, not the tile they build on. I don't think this was
#  the intention
def distance_heuristic(x_1, y_1, x_2, y_2, s_x_1, s_y_1, s_x_2, s_y_2):
    """
    The player would prefer to build the building away from the second player
    using manhattan distance
    """
    score = util.manhattanDistance([x_1, y_1], [s_x_1, s_y_1]) + \
            util.manhattanDistance([x_1, y_1], [s_x_2, s_y_2]) + util.manhattanDistance([x_2, y_2], [s_x_2, s_y_2]) + \
            util.manhattanDistance([x_2, y_2], [s_x_1, s_y_1])
    score -= min((util.manhattanDistance([x_1, y_1], [s_x_1, s_y_1]) +
                  util.manhattanDistance([x_2, y_2], [s_x_1, s_y_1])),
                 (util.manhattanDistance([x_1, y_1], [s_x_2, s_y_2]) +
                  util.manhattanDistance([x_2, y_2], [s_x_2, s_y_2])))
    return score


def setup_heuristic():
    pass


def evaluation_function(game_state: Board, current_player: Player, enemy_player: Player):
    score = 0
    if game_state.get_phase() == GamePhase.SETUP:
        return tile_value(current_player)
    else:
        score += height_heuristic(game_state, current_player, enemy_player)
        if game_state.get_phase() == GamePhase.MOVE:
            pass
        elif game_state.get_phase() == GamePhase.BUILD:
            # todo find alternative to this
            # score += distance_heuristic(x_1, y_1, x_2, y_2, s_x_1, s_y_1,
            #                            s_x_2, s_y_2)
            pass
    return score
