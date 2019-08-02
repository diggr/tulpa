import json
import requests
from provit import Provenance
from collections import defaultdict
from ..config import get_config, PROVIT_AGENT


PROVIT_ACTIVITY = "build_releases_dataset"
PROVIT_DESCRIPTION = "Contains all available release information from GameFAQS for each game."

class ReleasesDatasetBuilder:

    def __init__(self):

        self.cf = get_config()
        self.daft = self.cf.daft + "/gamefaqs/{id}"

        self.build_dataset()

    def _get_gamefaqs_data(self, id_):
        if not id_:
            return None
            
        rsp = requests.get(self.daft.format(id=id_.replace("/", "__")))
        data = rsp.json()

        if not "entry" in data:
            return None
        else:
            return data["entry"]

    def build_dataset(self):
        
        with open(self.cf.datasets["games"]) as f:
            games = json.load(f)

        dataset = {}

        for title, links in games.items():

            releases = defaultdict(list)

            for gf_id in links["gamefaqs"]:
                data = self._get_gamefaqs_data(gf_id)
                
                if data:
                    for release in data["raw"]["data"]["releases"]:
                        releases[release["region"]].append({
                            "title": release["title"],
                            "date": release["release_date"]
                        })

            dataset[title] = dict(releases)

        with open(self.cf.datasets["releases"], "w") as f:
            json.dump(dataset, f, indent=4)
                
        prov = Provenance(self.cf.datasets["releases"], overwrite=True)
        prov.add(
            agents=[ PROVIT_AGENT ],
            activity=PROVIT_ACTIVITY,
            description=PROVIT_DESCRIPTION
        )
        prov.add_sources([self.cf.datasets["games"]])
        prov.add_primary_source("gamefaqs")
        prov.save()

        print("completed")
        print("\nFile location: {}".format(self.cf.datasets["releases"]))

