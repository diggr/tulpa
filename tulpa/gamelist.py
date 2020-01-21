import requests
import yaml

from requests.compat import urljoin
from tqdm import tqdm

MOBYGAMES = "mobygames"

class GamelistGenerator():

    def len_mobygames_entries(self):
        rsp = self.s.get(self.mobygames_url)
        self.ids = rsp.json()["ids"]
        return len(self.ids)

    def mobygames_entries(self):
        if not hasattr(self, "ids"):
            rsp = self.s.get(self.mobygames_url)
            self.ids = rsp.json()["ids"]
        for mg_id in self.ids:
            rsp = self.s.get(self.mobygames_url + f"/{mg_id}")
            data = rsp.json()
            try:
                yield data["entry"]
            except:
                print(data)
                raise

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
            rsp = self.s.get(self.mobygames_url + f"/{id_}")
            data = rsp.json()
            url = data["entry"]["raw"]["moby_url"]
            return url.split("/")[-1]
        elif dataset_name == "gamefaqs":
            return id_.replace("__","/")
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
                    dataset[clustername][dataset_name].add(self.std_id(dataset_name, link["id"]))        

    def build_gamelist(self, mg):
        dataset = {}
        for entry in mg:
            rsp = self.s.get(self.mobygames_url + f"/{entry['id']}/links")
            links = rsp.json()["links"]

            slug = self.std_id("mobygames", entry["id"])

            clustername = self.find_cluster(dataset, slug)
            if not clustername:
                clustername = entry["title"]
                dataset[clustername] = {
                    "mobygames": set([ slug ]),
                    "mediaartdb": set(),
                    "gamefaqs": set()
                }

            self.add_links(links, "mobygames", dataset, clustername)
            self.add_links(links, "mediaartdb", dataset, clustername)
            self.add_links(links, "gamefaqs", dataset, clustername)

        ds = []
        for name, links in dataset.items():
            ds.append({
                "title": name,
                "links": {
                    "mobygames": list(links["mobygames"]),
                    "gamefaqs": list(links["gamefaqs"]),
                    "mediaartdb": list(links["mediaartdb"])
                }
            })
        ds = sorted(ds, key=lambda x: x["title"])

        final_ds = { x["title"]: x["links"] for x in ds }
        with open(self.gamelist_filename, "w") as f:
            yaml.dump(final_ds, f, default_flow_style=False)

    def __init__(self, query, company, daft_url, gamelist_filename, mobygames=MOBYGAMES):
        self.query = query
        self.company = company
        self.daft_url = daft_url
        self.gamelist_filename = gamelist_filename
        self.s = requests.Session()
        self.mobygames_url = urljoin(self.daft_url, mobygames)

        mg = []
        print("searching in mobygames dataset ...")
        for entry in tqdm(self.mobygames_entries(), total=self.len_mobygames_entries()):
            added = False
            if query:
                for title in self.iter_titles(entry):
                    if query.lower() in title.lower():
                        mg.append({
                            "title": entry["title"],
                            "id": entry["id"]
                        })
                        tqdm.write("- "+entry["title"])
                        added = True
                        
                        break
            if not added: 
                if company:
                    for company_name in self.iter_mobygames_companies(entry):
                        if company.lower() in company_name.lower():
                            mg.append({
                                "title": entry["title"],
                                "id": entry["id"]                            
                            })
                            tqdm.write("- "+entry["title"])                            
                            break

        self.build_gamelist(mg)
