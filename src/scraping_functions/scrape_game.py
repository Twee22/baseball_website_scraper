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
    
    starting_pitchers = scrape_lineups(link)
    results = starting_pitchers + results
    
    return results

def scrape_lineups(link):
    URL = link
    r = requests.get(URL, headers=headers, verify=False)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    results = soup.find_all("section")
    
    res = []
    for r in results:
        if "Pitching" in r.get_text():
            for i in str(r).split("\n"):
                if "<th scope=\"row\"><span class=\"hide-on-medium text-uppercase mobile-jersey-number\">" in i:
                    res.append(i.replace("<th scope=\"row\"><span class=\"hide-on-medium text-uppercase mobile-jersey-number\">", "").replace("</span>", "").replace("</th>", ""))
    
    results = []
    for r in res:
        if r[0] == "p":
            results.append(r)
            
    res = []
    for r in results:
        if "boxscore" in r:
            r = re.sub("<[^>]*>", "", r)
            player_name = str(r.split(" ")[1: ]).replace("'", "").replace("[", "").replace("]", "").replace(",", "")
            res.append("TEAMTEAMTEAM Starting Pitcher: " + player_name)
        else:
            player_name = str(r.split(" ")[1: ]).replace("'", "").replace("[", "").replace("]", "").replace(",", "")
            res.append("OPPOSITION Starting Pitcher: " + player_name)
    
    return res
    