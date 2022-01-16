from src.scraping_functions.game_list import get_game_list
from src.scraping_functions.extract_school_information import get_school_name, get_year
from src.scraping_functions.scrape_game import scrape_game
from src.setup.setup_helper_functions import check_school_file_exists
from src.output_functions.output_play_by_play_data import output_play_by_play_data
from src.format_data.format_game_data import format_game_data

def scrape_school(school):
    
    school_name = get_school_name(school)
    year = get_year(school)
    
    formatted_school_name = school_name.lower().replace(" ", "_")
    
    check = check_school_file_exists(formatted_school_name, year)
    
    game_links = get_game_list(school)
    play_by_play_data = []
    
    for link in game_links:
        game_data = scrape_game(link)
        play_by_play_data += format_game_data(game_data, school_name)
        # For testing purposes
        #break
    
    output_play_by_play_data(play_by_play_data, formatted_school_name, year)