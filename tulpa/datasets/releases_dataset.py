import json
import requests

from collections import defaultdict
from ..config import PROVIT_AGENT
from provit import Provenance
from ..utils import open_json, save_json

class ReleasesDatasetBuilder:

    PROVIT_ACTIVITY = "build_releases_dataset"
    PROVIT_DESCRIPTION = "Contains all available release information from GameFAQS for each game."

    def __init__(self, games_dataset, diggr_api):
        self.games_dataset = games_dataset
        self.daft = diggr_api + "/gamefaqs/{id}"

    def _get_gamefaqs_data(self, id_):
        if not id_:
            return None

        rsp = requests.get(self.daft.format(id=id_.replace("/", "__")))
        data = rsp.json()

        if not "entry" in data:
            return None
        else:
            return data["entry"]

    def build_dataset(self, outfilename):

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

        save_json(dataset, outfilename)

        prov = Provenance(outfilename, overwrite=True)
        prov.add(
            agents=[ PROVIT_AGENT ],
            activity=self.PROVIT_ACTIVITY,
            description=self.PROVIT_DESCRIPTION
        )
        prov.add_sources([self.cf.datasets["games"]])
        prov.add_primary_source("gamefaqs")
        prov.save()

        return release_dataset_path


def build_releases_dataset(release_dataset_path, games_dataset_path, diggr_api_url, force):
    """
    Release Dataset Factory
    """
    if not games_dataset_path.is_file():
        raise FileNotFoundError("Games dataset not found. Run tulpa dataset games to create it")
    if release_dataset_path.exists() and not force:
        raise FileExistsError(f"Dataset already exists at {dataset_path})")
    else:
        games_dataset = open_json(games_dataset_path)
        rdb = ReleasesDatasetBuilder(games_dataset_path, diggr_api_url)
        outfilename = rdb.build_dataset(release_dataset_path)
        return outfilename

