import requests
import random
import yaml

from diggrtoolbox.unified_api import DiggrAPI
from requests.compat import urljoin
from tqdm import tqdm

MOBYGAMES = "mobygames"


class GamelistGenerator:
    def __init__(self, daft_url, gamelist_filename, mobygames=MOBYGAMES):
        self.diggr_api = DiggrAPI(daft_url, get_on_item=True).dataset(mobygames)
        self.daft_url = daft_url
        self.gamelist_filename = gamelist_filename
        self.s = requests.Session()
        self.mobygames_url = urljoin(self.daft_url, mobygames)

    def mobygames_entries(self):
        if not hasattr(self, "ids"):
            self.ids = self.diggr_api.get()
        for mg_id in self.ids:
            yield self.diggr_api.item(mg_id)

    def iter_titles(self, entry):
        yield entry["title"]
        for alt_title in entry["alt_titles"]:
            yield alt_title

    def iter_mobygames_companies(self, entry):
        for platform in entry["raw"]["platforms"]:
            for release in platform["releases"]:
                for company in release["companies"]:
                    yield company["company_name"]

    def std_id(self, dataset_name, id_):
        if dataset_name == "mobygames":
            url = self.diggr_api.item(id_)["raw"]["moby_url"]
            return url.split("/")[-1]
        elif dataset_name == "gamefaqs":
            return id_.replace("__", "/")
        else:
            return id_

    def find_cluster(self, dataset, slug):
        for name, links in dataset.items():
            for id_ in links["mobygames"]:
                if id_ == slug:
                    return name
        return None

    def add_links(self, links, dataset_name, dataset, clustername):
        if dataset_name in links:
            for link in links[dataset_name]:
                if link["value"] > 0.9:
                    dataset[clustername][dataset_name].add(
                        self.std_id(dataset_name, link["id"])
                    )

    def build_gamelist(self, mg):
        dataset = {}
        for entry in mg:
            mg_links = (
                DiggrAPI(self.daft_url, get_on_item=True)
                .dataset("mobygames")
                .filter("links")
            )
            links = mg_links.item(entry["id"])

            slug = self.std_id("mobygames", entry["id"])

            clustername = self.find_cluster(dataset, slug)
            if not clustername:
                clustername = entry["title"]
                dataset[clustername] = {
                    "mobygames": set([slug]),
                    "mediaartdb": set(),
                    "gamefaqs": set(),
                }

            self.add_links(links, "mobygames", dataset, clustername)
            self.add_links(links, "mediaartdb", dataset, clustername)
            self.add_links(links, "gamefaqs", dataset, clustername)

        ds = []
        for name, links in dataset.items():
            ds.append(
                {
                    "title": name,
                    "links": {
                        "mobygames": list(links["mobygames"]),
                        "gamefaqs": list(links["gamefaqs"]),
                        "mediaartdb": list(links["mediaartdb"]),
                    },
                }
            )
        ds = sorted(ds, key=lambda x: x["title"])

        final_ds = {x["title"]: x["links"] for x in ds}
        with open(self.gamelist_filename, "w") as f:
            yaml.dump(final_ds, f, default_flow_style=False)

    def draw_sample(self, sample_size):
        self.sample_size = sample_size

        mg = []
        choices = random.choices(self.diggr_api.get(), k=self.sample_size)

        for mg_id in tqdm(choices):
            entry = self.diggr_api.item(mg_id)
            mg.append({"title": entry["title"], "id": entry["id"]})
            tqdm.write("- " + entry["title"])
        self.build_gamelist(mg)

    def build_by_query_or_company(self, query, company):
        """
        This function wraps the gamelist generation process.
        """
        self.query = query
        self.company = company

        mg = []
        for entry in tqdm(self.mobygames_entries(), total=len(self.diggr_api.get())):
            added = False
            if self.query:
                for title in self.iter_titles(entry):
                    if self.query.lower() in title.lower():
                        mg.append({"title": entry["title"], "id": entry["id"]})
                        tqdm.write("- " + entry["title"])
                        added = True

                        break
            if not added:
                if self.company:
                    for company_name in self.iter_mobygames_companies(entry):
                        if self.company.lower() in company_name.lower():
                            mg.append({"title": entry["title"], "id": entry["id"]})
                            tqdm.write("- " + entry["title"])
                            break

        self.build_gamelist(mg)


def draw_sample(sample_size, diggr_api_url, gamelist_filename):
    """
    Draws a sample of sample_size from mobygames and saves it to gamelist_filename
    """
    gg = GamelistGenerator(diggr_api_url, gamelist_filename)
    gg.draw_sample(sample_size)
    return gg.gamelist_filename


def build_gamelist(query, company, diggr_api_url, gamelist_filename):
    """
    Creates a gamelist from a query or company and saves it to gamelist_filename.
    """
    gg = GamelistGenerator(diggr_api_url, gamelist_filename)
    gg.build_by_query_or_company(query, company)
    return gg.gamelist_filename
