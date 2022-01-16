from src.format_data.format_helper_functions import similar

def format_game_data(game_data, school_name):
    
    game_data = [g.lower() for g in game_data]
    game_data.insert(0, "GAME_START_POINT")
    game_data.append("GAME_END_POINT")

    game_data = format_team_names(game_data, school_name)
    game_data = [g.replace("teamteamteam", school_name) for g in game_data]
    
    game_data = [g for gd in game_data for g in gd.split(";")]

    return game_data

def format_team_names(game_data, school_name):
    top_names = []
    bottom_names = []
    for g in game_data:
        if "top of" in g:
            top_names.append(g.split("-")[0])
        elif "bottom of" in g:
            bottom_names.append(g.split("-")[0])
    
    top_similarity = 0
    for t in top_names:
        top_similarity += similar(school_name, t)
    top_similarity = top_similarity / len(top_names)
    
    bottom_similarity = 0
    for b in bottom_names:
        bottom_similarity += similar(school_name, b)
    bottom_similarity = bottom_similarity / len(bottom_names)
    
    #removes duplicates
    top_names = list(set(top_names))
    bottom_names = list(set(bottom_names))
    
    if top_similarity > bottom_similarity:
        for t in top_names:
            game_data = [g.replace(t, school_name) for g in game_data]
        for b in bottom_names:
            game_data = [g.replace(b, "OPPOSITION") for g in game_data]
    else:
        for t in top_names:
            game_data = [g.replace(t, "OPPOSITION") for g in game_data]
        for b in bottom_names:
            game_data = [g.replace(b, school_name) for g in game_data]
            
    return game_data