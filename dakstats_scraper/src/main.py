from src.setup.setup_helper_functions import check_data_file_exists
from src.user_input.user_input import get_user_input
from src.scraping_functions.school_list import get_school_list
from src.scraping_functions.get_schedules import get_schedules
from src.scraping_functions.scrape_year import scrape_year

def main():
    # TODO: Make it so that it takes user input
    # TODO: Get multiple years
    # TODO: Add '-' to roster for missing data
    check_data_file_exists()
    #user_input = get_user_input()
    school_links = get_school_list("")#user_input["school_name"])
    for link in school_links:
        year_schedules = get_schedules(link)
        for year in year_schedules:
            scrape_year(year)
    print("I win")
    