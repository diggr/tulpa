import requests

from .builder import Builder
from diggrtoolbox.unified_api import DiggrAPI
from ..utils import print_last_prov_entry, open_yaml, open_json, save_json


class GamesDatasetBuilder(Builder):

    PROVIT_ACTIVITY = "build_games_dataset"
    PROVIT_DESCRIPTION = (
        "Contains all mobygames links and for the games in the gamelist "
    )

    def __init__(self, gamelist_path, diggr_api_url):
        self.diggr_api = DiggrAPI(diggr_api_url, get_on_item=True).dataset("mobygames")
        self.games = open_yaml(gamelist_path)
        super().__init__([gamelist_path], "mobygames")

    def _get_company_id(self, slug):
        return self.diggr_api.item(slug)["id"]

    def build_dataset(self, outfilename):
        """
        Build the games dataset, by reading the gamelist file and fetching links and companies
        from mobygames.
        """
        for title, links in self.games.items():
            mg_ids = []
            for mg_slug in links["mobygames"]:
                company_id = self._get_company_id(mg_slug)
                if company_id:
                    mg_ids.append(company_id)
                else:
                    continue
            links["mobygames_ids"] = mg_ids

        save_json(self.games, outfilename)
        return outfilename


def build_games_dataset(games_dataset_path, gamelist_file, diggr_api_url):
    """
    Games Dataset Factory
    """
    gdb = GamesDatasetBuilder(gamelist_file, diggr_api_url)
    outfilename = gdb.build(games_dataset_path)
    return outfilename


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

    print_last_prov_entry(games_dataset_path)
