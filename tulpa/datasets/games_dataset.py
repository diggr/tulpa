import json
import yaml
import os
import random
import requests
from ..utils import print_last_prov_entry, open_yaml, open_json, save_json


def get_company_id(slug, diggr_api_url):
    url = diggr_api_url + "/mobygames/slug/{slug}"
    rsp = requests.get(url.format(slug=slug))
    if rsp.ok:
        data = rsp.json()
        return data["entry"]["id"]
    else:
        print(f"Error while processing {slug}")
        return None


def build_games_dataset(games_dataset_path, gamelist_path, diggr_api_url):
    """
    Build the games dataset, by reading the gamelist file and fetching links and companies
    from mobygames.
    """
    games = open_yaml(gamelist_path)

    for title, links in games.items():
        mg_ids = []
        for mg_slug in links["mobygames"]:
            company_id = get_company_id(mg_slug, diggr_api_url)
            if company_id:
                mg_ids.append(company_id)
            else:
                continue

        links["mobygames_ids"] = mg_ids

    save_json(games, games_dataset_path)
    return games_dataset_path


def check_games_dataset(games_dataset_path):

    ds = open_json(games_dataset_path)

    print("Number of games: {}".format(len(ds)))

    no_ids = {"gamefaqs": [], "mediaartdb": [], "mobygames": []}

    for game_title, links in ds.items():

        if "mobygames" not in links:
            no_ids["mobygames"].append(game_title)
        else:
            if len(links["mobygames"]) == 0:
                no_ids["mobygames"].append(game_title)

        if "mediaartdb" not in links:
            no_ids["mediaartdb"].append(game_title)
        else:
            if len(links["mediaartdb"]) == 0:
                no_ids["mediaartdb"].append(game_title)

        if "gamefaqs" not in links:
            no_ids["gamefaqs"].append(game_title)
        else:
            if len(links["gamefaqs"]) == 0:
                no_ids["gamefaqs"].append(game_title)

    print("\t ... without Media Art DB entry: {}".format(len(no_ids["mediaartdb"])))
    for title in no_ids["mediaartdb"]:
        print("\t\t - {}".format(title))
    print("\t ... without Mobygames entry: {}".format(len(no_ids["mobygames"])))
    for title in no_ids["mobygames"]:
        print("\t\t - {}".format(title))
    print("\t ... without GameFAQs entry: {}".format(len(no_ids["gamefaqs"])))
    for title in no_ids["gamefaqs"]:
        print("\t\t - {}".format(title))

    print_last_prov_entry(dataset_file)
