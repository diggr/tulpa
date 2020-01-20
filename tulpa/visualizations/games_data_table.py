import requests
import json
import os
import pandas as pd
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from ..config import get_config

COMPANY_DATASET = "/datasets/mobygames_companies.json"
WIKIDATA_MAPPING = "/datasets/wikidata_mapping.json"
ID_2_SLUG = "/datasets/mobygames_companies_id_to_slug.json"




class GamesDataTableBuilder():

    def _load_lemongrab_datasets(self):
        with open(self.cf.lemongrab + COMPANY_DATASET) as f:
            dataset = json.load(f)
        with open(self.cf.lemongrab + WIKIDATA_MAPPING) as f:
            wiki = json.load(f)
        with open(self.cf.lemongrab + ID_2_SLUG) as f:
            id_2_slug = json.load(f)

        id_2_slug_map = { x["company_id"]: x["slug"] for x in id_2_slug }
        wiki_map = { x["mobygames_slug"]: x for x in wiki }

        self.datasets = {
            "production_details": dataset,
            "slug_map": id_2_slug_map,
            "wiki_map": wiki_map }

    def _get_data(self, mg_slugs):
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
                    platforms.add(entry["platform"])
        
        return {
            "platforms": list(platforms),
            "companies": companies_dataset
        }



    def __init__(self):


        self.cf = get_config()

        with open(self.cf.datasets["games"]) as f:
            self.gamelist = json.load(f)

        self._load_lemongrab_datasets()

        dataset = []

        for title, links in self.gamelist.items():
            entry = {}
            entry["title"] = title
            data = self._get_data(links["mobygames"])
            all_companies = 0
            for country, companies in data["companies"].items():
                n_companies = len(companies)
                entry[country] = n_companies
                all_companies += n_companies#
            entry["n_companies"] = all_companies
            entry["plattforms"] = ",".join(data["platforms"])

            dataset.append(entry)

        print(dataset)
        df = pd.DataFrame(dataset)
        filepath = self.cf.dirs["games_data_table"] / "{}_data_table.csv".format(self.cf.project_name)
        df.to_csv(filepath)
            