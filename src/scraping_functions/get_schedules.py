from src.config.config import url_part_1
from bs4 import BeautifulSoup

def get_schedules(link):

    # TODO: Update this so that it returns schedules for multiple years

    URL = url_part_1[:-1] + link.replace("href=", "").replace("\'", "").replace("TeamPage", "TeamSchedule")
    URL = URL.split(">", 1)[0]

    return [URL]