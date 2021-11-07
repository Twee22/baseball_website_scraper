from src.setup.setup_helper_functions import check_data_file_exists, disable_warnings
from src.scraping_functions.scrape_school import scrape_school

# For testing purposes
from src.config.config import url_part_1, url_part_2

##### TODO
# Check Folder Exists
# Scrape games
# Make get school list (incl year here)
# Update get_year to use proper web scraping

def main():
    
    disable_warnings()
    check_data_file_exists()
    
    test_school = {"url_part_1": url_part_1,
                   "url_part_2": url_part_2}
    school_list = [test_school]
    #school_list = get_school_list
    
    for school in school_list:
        scrape_school(school)
    
    print("Program terminates")
    return
