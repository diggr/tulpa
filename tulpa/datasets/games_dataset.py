import json
import yaml
import os
import random
import requests
from ..config import get_config
from ..utils import print_last_prov_entry, open_yaml, save_json

config = get_config()


def get_company_id(slug):
    url = config.daft + "/mobygames/slug/{slug}"
    rsp = requests.get(url.format(slug=slug))
    if rsp.ok:
        data = rsp.json()
        return data["entry"]["id"]
    else:
        print(f"Error while processing {slug}")
        return None


def build_games_dataset():
    """
    Build the games dataset, by reading the gamelist file and fetching links and companies
    from mobygames.
    """
    games = open_yaml(config.gamelist_file)

    for title, links in games.items():
        mg_ids = []
        for mg_slug in links["mobygames"]:
            company_id = get_company_id(mg_slug)
            if company_id:
                mg_ids.append(company_id)
            else:
                continue

        links["mobygames_ids"] = mg_ids

    save_json(games, config.datasets["games"])
    return config.datasets["games"]


def check_games_dataset():

    dataset_file = config.datasets["games"]

    print("\nFile location: {}\n".format(dataset_file))

    with open(dataset_file) as f:
        ds = json.load(f)

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
