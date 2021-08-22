import util


def extractor(state, action, player):
    enemy = state.get_enemy_of(player)

    features = util.Counter()
    features['max_player_height'] = max(
        player.first_piece.tile.height if player.first_piece is not None else 0,
        player.second_piece.tile.height if player.second_piece is not None else 0
    )
    features['max_enemy_height'] = max(
        enemy.first_piece.tile.height if enemy.first_piece is not None else 0,
        enemy.second_piece.tile.height if enemy.second_piece is not None else 0
    )

    return features
