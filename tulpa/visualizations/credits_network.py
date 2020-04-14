import datetime
import json
import requests
import networkx as nx

from ..datasets.builder import Builder
from itertools import combinations
from ..utils import open_json


class CreditsNetworkBuilder(Builder):

    PROVIT_ACTIVITY = "build_credits_network"
    PROVIT_DESCRIPTION = "Network of games connected by overlapping development staff."
    NETWORK_FILENAME = "{project_name}_credits_network_{timestamp}.graphml"

    def __init__(self, games_dataset_path, diggr_api_url):
        self.games = open_json(games_dataset_path)
        self.daft = diggr_api_url + "/mobygames/slug/{slug}"
        super().__init__([games_dataset_path], "mobygames")

    def _get_game_info(self, slug):
        rsp = requests.get(self.daft.format(slug=slug))
        data = rsp.json()
        if "entry" in data:
            return data["entry"]
        else:
            return None

    def _fetch_credits(self, slugs):
        if len(slugs) == 0:
            return []

        devs = set()
        roles = set()

        for slug in slugs:
            ds = self._get_game_info(slug)
            if ds:

                for platform in ds["raw"]["platforms"]:
                    if "credits" in platform:
                        for credits in platform["credits"]:
                            roles.add(credits["role"])
                            for credit in credits["credits"]:
                                devs.add(credit["developer_id"])

        return set([x for x in devs if x])

    def build_dataset(self, outfilename):

        # build dataset
        dataset = {}
        self.missing_credits = []
        for game, links in self.games.items():
            devs = self._fetch_credits(links["mobygames"])
            if len(devs) > 0:
                dataset[game] = devs
            else:
                self.missing_credits.append(game)

        # build graph
        g2 = nx.Graph()
        for s1, s2 in combinations(list(dataset), 2):
            overlap = dataset[s1].intersection(dataset[s2])

            if len(dataset[s1]) < len(dataset[s2]):
                smallest = len(dataset[s1])
            else:
                smallest = len(dataset[s2])

            if len(overlap) > 0:
                sim2 = len(overlap) / smallest
            else:
                sim2 = 0

            if sim2 > 0:
                g2.add_edge(s1, s2, weight=sim2)

        nx.write_graphml(g2, outfilename)
        return outfilename


def build_credits_network(
    games_dataset_path, diggr_api_url, project_name, credits_network_path,
):
    cnb = CreditsNetworkBuilder(games_dataset_path, diggr_api_url)
    outfilename = credits_network_path / cnb.NETWORK_FILENAME.format(
        project_name=project_name, timestamp=datetime.datetime.now().isoformat()
    )
    outfilename = cnb.build(outfilename)
    return outfilename, cnb.missing_credits
