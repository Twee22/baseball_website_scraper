import requests 
import re

from src.config.config import headers

from src.config.config import starting_url, url_part_1

def get_school_list(school_name):

    URL = starting_url

    r = requests.get(URL, headers=headers)

    text = r.text

    links = re.findall(r"href='.*TeamPage.*'", text)

    links = get_all_links(links, 0)

    return links

def get_all_links(starting_links, limit):

    if limit > 0:
        return starting_links

    new_list = []
    [new_list.append(x) for x in starting_links if x not in new_list]

    for link in new_list:
        URL = url_part_1[:-1] + link.replace("href=", "").replace("\'", "").replace("TeamPage", "TeamSchedule")

        r = requests.get(URL, headers=headers)

        text = r.text

        links = re.findall(r"href='.*TeamPage.*'", text)

        for l in links:
            if l not in new_list:
                print(l)
                new_list.append(l)
                new_list = get_all_links(new_list, limit + 1)

    return new_list                



