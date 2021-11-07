import requests
import re

#from bs4 import BeautifulSoup

from src.config.config import headers

def get_school_name(school):
    URL = school["url_part_1"] + school["url_part_2"]
    r = requests.get(URL, headers=headers, verify=False)
    text = r.text
    
    school_name = re.findall(r"window.client_title\s?=\s?[^;]+;", text)[0]
    school_name = school_name.split("\"")[1]
    
    return school_name

def get_year(school):
    URL = school["url_part_1"] + school["url_part_2"]
    
    r = requests.get(URL, headers=headers, verify=False)
    text = r.text
    
    year = re.findall(r"href=\"/sports/baseball/schedule/[0-9]+\?grid=true", text)[0]
    year = year.split("/")[-1]
    year = year.split("?")[0]

    return year