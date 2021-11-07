from src.scraping_functions.game_list import get_game_list
from src.scraping_functions.extract_school_information import get_school_name, get_year

def scrape_school(school):
    
    school_name = get_school_name(school)
    year = get_year(school)
    
    game_links = get_game_list(school)