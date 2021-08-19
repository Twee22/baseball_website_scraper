from src.config.config import url_part_1, headers
from bs4 import BeautifulSoup
import requests
import re
from os import getcwd, mkdir
from os.path import isdir


def scrape_year(year):

    pages_to_scrape = get_pages_to_scrape_dakstats(year)
    school_information = scrape_school_information(year)
    check = check_if_school_folders_exist(school_information)
    check = get_roster(year, school_information)
    check = scrape_pages_dakstats(school_information, pages_to_scrape)

def get_pages_to_scrape_dakstats(year):
    
    URL = year

    r = requests.get(URL, headers=headers, verify=False)
    text = r.text

    links = re.findall(r'ShowWebcastPopup[^\s]+;', text)

    return links

def scrape_pages_dakstats(school, pages_to_scrape):

    print("Scraping data for", school["name"])

    file_destination = "data/" + school["school_name"] + "/" + school["year"] + "/" + school["school_name"] + "_batting_" + school["year"] + ".txt"
    open(file_destination, "w").close

    for page in pages_to_scrape:

        seperated_page = page.split(",")

        seasonID = seperated_page[3][1:-3]
        sg = seperated_page[1][1:-1]
        compID = seperated_page[2][1:-1]

        print("Processing: seasonID = {} sg = {} compID = {}".format(seasonID, sg, compID))

        link = "https://www.dakstats.com/WebSync/Pages/GameBook/GameBookData.aspx?sg={}&compID={}&sea={}".format(sg, compID, seasonID)

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(link, headers=headers, verify=False)

        soup = BeautifulSoup(r.content, 'html.parser')

        results = soup.find_all("td")                 

        play_by_play_text = ""
        home_or_away = "NOT_DEFINED"

        for res in results:
            text = res.text
            if re.search("Starting Lineup", text):
                if home_or_away == "NOT_DEFINED":
                    if school["name"] in text:
                        home_or_away = "HOME"
                    else:
                        home_or_away = "AWAY"
                
                    play_by_play_text += "GAME_START_POINT\n"

                player_name = text.split(',')[-1]
                player_name = player_name.strip()[:-1]   

                if school["name"] in text:
                    play_by_play_text += school["name"] + " Starting Pitcher: " + player_name + "\n"
                else: 
                    play_by_play_text += "OPPOSITION Starting Pitcher: " + player_name + "\n"

            if re.search("Top|Bottom", text):
                if home_or_away == "HOME":  
                    if re.search("Bottom of", text):
                        text = text.replace("Bottom of", school["name"] + " Bottom of", 1)
                    elif re.search("Top of", text):
                        text = text.replace("Top of", "OPPOSITION Top of", 1)
                elif home_or_away == "AWAY":
                    if re.search("Top of", text):
                        text = text.replace("Top of", school["name"] + " Top of", 1)
                    elif re.search("Bottom of", text):
                        text = text.replace("Bottom of", "OPPOSITION Bottom of", 1)
                else:
                    pass

                text = text.replace("- ", "\n", 1)
                text = text.replace(". ", "\n")

                play_by_play_text += text
                play_by_play_text += "\n"

        play_by_play_text +=  "GAME_END_POINT\n"
            
        with open(file_destination, "a") as file:
            file.write(play_by_play_text)

    print("Complete")

    return True

def scrape_school_information(year):
    
    URL = year

    r = requests.get(URL, headers=headers, verify=False)
    text = r.text

    soup = BeautifulSoup(r.content, 'html.parser')
    results = soup.find_all("span", id="ctl00_websyncPageTitle_pageTitleNameLabel") 

    school_name = str(results[0])
    school_name = school_name[79:-7]
    school_name = re.sub(r"\([^()]*\)", "", school_name)
    school_name = school_name.lower().strip().replace(" ", "_")

    results = soup.find_all("span", id="ctl00_websyncTeamRecord_seasonLabel")

    year = str(results[0])
    year = year[47:-7]

    school_information = {"school_name": school_name, "year": year}

    return school_information


def check_if_school_folders_exist(school_information):

    path = getcwd() + "/data/" + school_information["school_name"]

    if not isdir(path):
        mkdir(path)

    path = getcwd() + "/data/" + school_information["school_name"] + "/" + school_information["year"]

    if not isdir(path):
        mkdir(path)

def get_roster(year, school_information):

    print("Getting Roster for :", school_information["school_name"])

    URL = year.replace("TeamSchedule", "Roster")

    r = requests.get(URL, headers=headers, verify=False)

    soup = BeautifulSoup(r.content, 'html.parser')
    results = soup.find_all("table", id="ctl00_websyncContentPlaceHolder_rosterGridView") 

    players = str(results[0]).split("<tr")
    players = players[2:]

    file_name = "data/" + school_information["school_name"] + "/" + school_information["year"] + "/" + school_information["school_name"] + "_team_" + school_information["year"] + ".txt"


    with open(file_name, "w") as f:

        f.write("number f_name name position class height weight b_t\n")

        for player in players:
            player_profile = ""
            data_points = player.split(">")
            for point in data_points:
                if "<td" not in point and "class" not in point and "Career Stats" not in point:
                    point = point.split("<")[0].strip()
                    if point == "L" or point == "R" or point == "SW":
                        player_profile += point  + "/"
                    elif point:
                        player_profile += point + " "
                    else:
                        #player_profile += "- "
                        pass
            if player_profile[-1] == "/":
                player_profile = player_profile[:-1]
            f.write(player_profile + "\n")

    return True
