import json
import requests

from provit import Provenance
from collections import defaultdict
from ..config import PROVIT_AGENT
from ..utils import open_json, save_json

class CompaniesDatasetBuilder:

    PROVIT_ACTIVITY = "build_companies_dataset"
    PROVIT_DESCRIPTION = (
        "Contains all available company information from Mobygames for each game."
    )

    def __init__(self, diggr_api_url, games_dataset_path):

        self.daft = diggr_api_url + "/mobygames/{id}/companies"
        self.games_dataset_path = games_dataset_path

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
            id_ = str(c["company_id"]) + c["role"]
            if id_ not in done:
                dataset.append(c)
                done.append(c)
        return dataset

    def build_dataset(self, outfilename):
        games = open_json(self.games_dataset_path)

        dataset = {}
        for title, links in games.items():

            companies = []
            for m, mg_id in enumerate(links["mobygames_ids"]):
                data = self._get_company_data(mg_id)
                for company in data:
                    company["game_slug"] = links["mobygames"][m]
                companies += data

            dataset[title] = self._remove_duplicates(companies)

        save_json(dataset, outfilename)

        prov = Provenance(outfilename, overwrite=True)
        prov.add(
            agents=[PROVIT_AGENT],
            activity=self.PROVIT_ACTIVITY,
            description=self.PROVIT_DESCRIPTION,
        )
        prov.add_sources([self.games_dataset_path])
        prov.add_primary_source("mobygames")
        prov.save()

        return outfilename

def build_companies_dataset(companies_dataset_path, games_dataset_path, diggr_api_url):
    """
    Companies Dataset Factory
    """
    cdb = CompaniesDatasetBuilder(diggr_api_url, games_dataset_path)
    outfilename = cdb.build_dataset(companies_dataset_path)
    return outfilename

