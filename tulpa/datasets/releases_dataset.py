import requests

from .builder import Builder
from collections import defaultdict
from ..utils import open_json, save_json


class ReleasesDatasetBuilder(Builder):

    PROVIT_ACTIVITY = "build_releases_dataset"
    PROVIT_DESCRIPTION = (
        "Contains all available release information from GameFAQS for each game."
    )

    def __init__(self, games_dataset_path, diggr_api):
        self.games = open_json(games_dataset_path)
        self.daft = diggr_api + "/gamefaqs/{id}"
        super().__init__([games_dataset_path], "gamefaqs")

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

        for title, links in self.games.items():

            releases = defaultdict(list)

            for gf_id in links["gamefaqs"]:
                data = self._get_gamefaqs_data(gf_id)

                if data:
                    for release in data["raw"]["data"]["releases"]:
                        releases[release["region"]].append(
                            {"title": release["title"], "date": release["release_date"]}
                        )

            dataset[title] = dict(releases)

        save_json(dataset, outfilename)

        return outfilename


def build_releases_dataset(
    releases_dataset_path, games_dataset_path, diggr_api_url, force
):
    """
    Release Dataset Factory
    """
    if not games_dataset_path.is_file():
        raise FileNotFoundError(
            f"Games dataset not found at {games_dataset_path}. Run tulpa dataset games to create it"
        )
    if releases_dataset_path.exists() and not force:
        raise FileExistsError(f"Dataset already exists at {releases_dataset_path}")
    else:
        rdb = ReleasesDatasetBuilder(games_dataset_path, diggr_api_url)
        outfilename = rdb.build(releases_dataset_path)
        return outfilename
