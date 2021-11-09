import requests
import re

from bs4 import BeautifulSoup

from src.config.config import headers

def scrape_game(link):
    
    URL = link
    r = requests.get(URL, headers=headers, verify=False)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    results = soup.find_all("div", id="inning-all")
    
    results = str(results).split("\n")
    results = [r for r in results if ("<th scope=\"row\">" in r or "<caption>" in r)]
    results = [re.sub("<[^>]*>", "", r) for r in results]
    
    return results