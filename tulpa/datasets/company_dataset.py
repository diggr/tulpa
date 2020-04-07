import json
import requests
from provit import Provenance
from collections import defaultdict
from ..config import get_config, PROVIT_AGENT


PROVIT_ACTIVITY = "build_company_dataset"
PROVIT_DESCRIPTION = "Contains all available company information from Mobygames for each game."

class CompanyDatasetBuilder:

    def __init__(self):

        self.cf = get_config()
        self.daft = self.cf.daft + "/mobygames/{id}/companies"

        self.build_dataset()

    def _get_company_data(self, id_):
        if not id_:
            return None

        rsp = requests.get(self.daft.format(id=id_))
        data = rsp.json()

        if not "entry" in data:
            return None
        else:
            return data["entry"]

    def _remove_duplicates(self, companies):
        done = []
        dataset = []
        for c in companies:
            id_ = str(c["company_id"])+c["role"]
            if id_ not in done:
                dataset.append(c)
                done.append(c)
        return dataset


    def build_dataset(self):
        with open(self.cf.datasets["games"]) as f:
            games = json.load(f)

        dataset = {}
        for title, links in games.items():

            companies = []
            for m, mg_id in enumerate(links["mobygames_ids"]):
                data = self._get_company_data(mg_id)
                for company in data:
                    company["game_slug"] = links["mobygames"][m]
                companies += data

            dataset[title] = self._remove_duplicates(companies)

        with open(self.cf.datasets["companies"], "w") as f:
            json.dump(dataset, f, indent=4)

        prov = Provenance(self.cf.datasets["companies"], overwrite=True)
        prov.add(
            agents=[ PROVIT_AGENT ],
            activity=PROVIT_ACTIVITY,
            description=PROVIT_DESCRIPTION
        )
        prov.add_sources([self.cf.datasets["games"]])
        prov.add_primary_source("mobygames")
        prov.save()

        print("completed")
        print("\nFile location: {}".format(self.cf.datasets["companies"]))
