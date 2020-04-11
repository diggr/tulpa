import requests
import json
import os
import pandas as pd
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from ..config import get_config

try:
    import lemongrab

    LEMONGRAB_AVAILABLE = True
except ImportError:
    LEMONGRAB_AVAILABE = False


class GamesDataTableBuilder:
    def __init__(self):
        self.cf = get_config()

        with open(self.cf.datasets["games"]) as f:
            self.gamelist = json.load(f)

        if not LEMONGRAB_AVAILABLE:
            raise RuntimeError("lemongrab is required to use this function!")
        self._load_lemongrab_datasets()

        dataset = []

        for title, links in self.gamelist.items():
            entry = {}
            entry["title"] = title
            data = self._get_company_data(links["mobygames"])
            all_companies = 0
            for country, companies in data["companies"].items():
                n_companies = len(companies)
                entry[country] = n_companies
                all_companies += n_companies
            entry["n_companies"] = all_companies

            all_releases = 0
            releases = self.get_release_data(title)
            for release in releases:
                entry[release["region"]] = release["count"]
                all_releases += release["count"]
            entry["n_releases"] = all_releases
            print(data["platforms"])
            entry["platforms"] = ",".join(sorted(data["platforms"]))

            dataset.append(entry)

        df = pd.DataFrame(dataset)
        # df = df.fillna(0)
        filepath = self.cf.dirs["games_data_table"] / "{}_data_table.csv".format(
            self.cf.project_name
        )
        df.to_csv(filepath)

    def _load_lemongrab_datasets(self):

        dataset, wiki, id_2_slug = lemongrab.utils.get_datasets()

        id_2_slug_map = {x["company_id"]: x["slug"] for x in id_2_slug}
        wiki_map = {x["mobygames_slug"]: x for x in wiki}

        self.datasets = {
            "production_details": dataset,
            "slug_map": id_2_slug_map,
            "wiki_map": wiki_map,
        }

    def _get_company_data(self, mg_slugs):
        platforms = set()
        companies = self.datasets["production_details"]

        companies_dataset = defaultdict(set)

        for company_id, details in companies.items():
            for entry in details:
                if entry["game_slug"] in mg_slugs:
                    slug = self.datasets["slug_map"][company_id]
                    if slug in self.datasets["wiki_map"]:
                        country = self.datasets["wiki_map"][slug]["country"]
                    else:
                        country = "unknown"
                    companies_dataset[country].add(company_id)
                    if entry["platform"]:
                        platforms.add(entry["platform"])

        return {"platforms": list(platforms), "companies": companies_dataset}

    def get_release_data(self, game_id):
        with open(self.cf.datasets["releases"]) as f:
            releases = json.load(f)

        dataset = []
        for region, r in releases[game_id].items():
            dataset.append({"region": region + "_releases", "count": len(r)})

        return dataset
