import json
import requests
import networkx as nx
from datetime import datetime
from itertools import combinations
from provit import Provenance
from ..config import get_config, PROVIT_AGENT

PROVIT_ACTIVITY = "build_credit_network"
PROVIT_DESCRIPTION = "Network of games connected by overlapping development staff."

NETWORK_FILE = "{project_name}_credits_network_{timestamp}.graphml"

class CreditsNetwork:

    def __init__(self):
        self.cf = get_config()
        self.daft = self.cf.daft + "/mobygames/slug/{slug}"

        self.build_network()

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

    def build_network(self):

        cf = get_config()

        daft_url = cf.daft + "/mobygames/slug/{slug}"

        with open(cf.datasets["games"]) as f:
            games = json.load(f)

        #build dataset
        dataset = {}
        for game, links in games.items():
            devs = self._fetch_credits(links["mobygames"])
            if len(devs) > 0:        
                dataset[game] = devs
            else:
                print("no credits available for ", game)

        #build graph
        g2 = nx.Graph()
        for s1, s2 in combinations(list(dataset), 2):
            overlap = dataset[s1].intersection(dataset[s2])

            if len(dataset[s1]) < len(dataset[s2]):
                smallest = len(dataset[s1])
            else:
                smallest = len(dataset[s2])

            if len(overlap) > 0:
                sim2 = len(overlap)/smallest
            else:
                sim2 = 0
                
            if sim2 > 0:
                g2.add_edge(s1, s2, weight=sim2)

        #save
        filename = NETWORK_FILE.format(
            project_name=self.cf.project_name, 
            timestamp=datetime.now().isoformat())

        filepath = self.cf.dirs["credits_network"] / filename

        print("\nSave visualization ...")
        print("File location: {}".format(filepath))
        nx.write_graphml(g2, filepath)

        prov = Provenance(filepath)
        prov.add(
            agents=[ PROVIT_AGENT ],
            activity=PROVIT_ACTIVITY,
            description=PROVIT_DESCRIPTION
        )
        prov.add_sources([self.cf.datasets["games"]])
        prov.add_primary_source("mobygames")
        prov.save()