import requests
from bs4 import BeautifulSoup
import json


def get_games(game_status):
    main_page = requests.get("https://cyberscore.live/")
    soup = BeautifulSoup(main_page.text, features="html.parser")
    data = json.loads(soup.body.find('script', attrs={'id': '__NEXT_DATA__'}).text)
    today_matches = data["props"]["pageProps"]["initialState"]["globalData"]["blocks"]["matches"]["data"]["items"]
    online_matches_list = {}
    for match in today_matches:
        status = match["status"]
        if status == game_status:
            online_matches_list[match["title"]] = match["id"]
    return online_matches_list


def get_match_info(match_id):
    print("https://cyberscore.live/matches/" + str(match_id))
    match_page = requests.get("https://cyberscore.live/matches/" + str(match_id))
    match_soup = BeautifulSoup(match_page.text, features="html.parser")
    match_data = json.loads(match_soup.body.find('script', attrs={'id': '__NEXT_DATA__'}).text)
    match_items = match_data["props"]["pageProps"]["initialState"]["globalData"]["blocks"]["match_single"]["data"][
        "item"]
    team_radiant = match_items["teams"][0]["picks"]
    team_dire = match_items["teams"][1]["picks"]
    networth_node = match_items["networth"][-1]
    towers = {}
    try:
        towers = match_items["buildingState"]["towers"][-1]
    except Exception as e:
        towers["value_dire"] = "11111111111"
        towers["value_radiant"] = "11111111111"

    if towers["value_dire"] == "0":
        towers["value_dire"] = "00000000000"
    if towers["value_radiant"] == "0":
        towers["value_radiant"] = "00000000000"
    result = "{\n    \"cases\":[" \
             "\n    {" \
             "\n    \"networth\": \"" + str(networth_node["value"]) + "\"," \
                                                                      "\n    \"advantage\": \"" + networth_node[
                 "team"] + "\"," \
                           "\n    \"time\": \"" + str(networth_node["time"]) + "\"," \
                                                                               "\n    \"tower_radiant\": \"" + towers[
                 "value_radiant"] + "\"," \
                                    "\n    \"tower_dire\": \"" + towers["value_dire"] + "\"," \
                                                                                        "\n    \"teams\": [" \
                                                                                        "\n    {" \
                                                                                        "\n    \"type\": \"radiant\"," \
                                                                                        "\n    \"hero1\": \"" + \
             team_radiant[0]["hero"]["name"] + "\"," \
                                               "\n    \"hero2\": \"" + team_radiant[1]["hero"]["name"] + "\"," \
                                                                                                         "\n    \"hero3\": \"" + \
             team_radiant[2]["hero"]["name"] + "\"," \
                                               "\n    \"hero4\": \"" + team_radiant[3]["hero"]["name"] + "\"," \
                                                                                                         "\n    \"hero5\": \"" + \
             team_radiant[4]["hero"]["name"] + "\"" \
                                               "\n    }," \
                                               "\n    {" \
                                               "\n    \"type\": \"dire\"," \
                                               "\n    \"hero1\": \"" + team_dire[0]["hero"]["name"] + "\"," \
                                                                                                      "\n    \"hero2\": \"" + \
             team_dire[1]["hero"]["name"] + "\"," \
                                            "\n    \"hero3\": \"" + team_dire[2]["hero"]["name"] + "\"," \
                                                                                                   "\n    \"hero4\": \"" + \
             team_dire[3]["hero"]["name"] + "\"," \
                                            "\n    \"hero5\": \"" + team_dire[4]["hero"]["name"] + "\"" \
                                                                                                   "\n    }" \
                                                                                                   "\n]" \
                                                                                                   "\n}" \
                                                                                                   "\n  ]\n}"
    with open('./current_match/' + str(match_id) + '.json', 'w') as f:
        f.write(result)
        f.close()
