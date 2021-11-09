
def format_game_data(game_data):
    
    game_data.insert(0, "GAME_START_POINT")
    game_data.append("GAME_END_POINT")

    return game_data