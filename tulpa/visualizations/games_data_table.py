import pandas as pd

from ..datasets.builder import Builder
from collections import defaultdict
from ..utils import open_json

LEMONGRAB_AVAILABLE = False
try:
    from lemongrab.utils import get_datasets as get_lemongrab_datasets

    LEMONGRAB_AVAILABLE = True
except ImportError:
    pass


class GamesDataTableBuilder(Builder):

    PROVIT_ACTIVITY = "build_games_data_table"
    PROVIT_DESCRIPTION = "Building the games data table using lemongrab."
    GAMES_DATA_TABLE_FILENAME = "{project_name}_games_data_table_{count_str}.csv"

    def __init__(self, games_dataset_path, releases_dataset_path, count):
        self.games = open_json(games_dataset_path)
        self.releases = open_json(releases_dataset_path)
        self.count = count

        super().__init__([games_dataset_path, releases_dataset_path], "wikidata")

    def build_dataset(self, outfilename):
        if not LEMONGRAB_AVAILABLE:
            raise RuntimeError("lemongrab is required to use this function!")
        self._load_lemongrab_datasets()

        dataset = []

        for title, links in self.games.items():
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
                if self.count:
                    entry[release["region"]] = release["count"]
                else:
                    entry[release["region"]] = release["earliest"]
                all_releases += release["count"]
            entry["n_releases"] = all_releases
            entry["platforms"] = ",".join(sorted(data["platforms"]))

            dataset.append(entry)

        df = pd.DataFrame(dataset)
        df.to_csv(outfilename)
        return outfilename

    def _load_lemongrab_datasets(self):

        try:
            dataset, id_2_slug, wiki = get_lemongrab_datasets()
        except FileNotFoundError:
            raise RuntimeError(
                "lemongrab must be initialized in this directory and datasets must built before this command can be run."
            )

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

        dataset = []
        for region, r in self.releases[game_id].items():
            release_dates = [release["date"][:4] for release in r]
            for release_date in release_dates:
                try:
                    int(release_date)
                except ValueError:
                    release_dates.remove(release_date)
            if len(release_dates):
                earliest_release = min(sorted(release_dates))
            else:
                earliest_release = 0
            dataset.append(
                {
                    "region": region + "_releases",
                    "count": len(r),
                    "earliest": earliest_release,
                }
            )

        return dataset


def build_games_data_table(
    games_dataset_path,
    releases_dataset_path,
    project_name,
    games_data_table_path,
    count,
):
    """
    Games Data Table Factory
    """
    if count:
        count_str = "count"
    else:
        count_str = "earliest"
    gdtb = GamesDataTableBuilder(games_dataset_path, releases_dataset_path, count)
    outfilename = games_data_table_path / gdtb.GAMES_DATA_TABLE_FILENAME.format(
        project_name=project_name,
        count_str=count_str
    )
    outfilename = gdtb.build(outfilename)
    return outfilename
