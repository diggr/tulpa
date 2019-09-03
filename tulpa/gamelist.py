import requests
import yaml
from .config import get_config
from tqdm import tqdm

class GamelistGenerator():

    def mobygames_entries(self):

        rsp = requests.get(self.cf.daft+"/mobygames")
        ids = rsp.json()["ids"]
        for mg_id in ids:
            rsp = requests.get(self.cf.daft+"/mobygames/{}".format(mg_id))
            data = rsp.json()
            yield data["entry"]

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
            rsp = requests.get(self.cf.daft+"/mobygames/{}".format(id_))
            data = rsp.json()
            url = data["entry"]["raw"]["moby_url"]
            return url.split("/")[-1]
        elif dataset_name = "gamefaqs":
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
            rsp = requests.get(self.cf.daft+"/mobygames/{}/links".format(entry["id"]))
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
        with open(self.cf.gamelist_file, "w") as f:
            yaml.dump(final_ds, f, default_flow_style=False)

    def __init__(self, query, company):
        self.query = query
        self.company = company
        self.cf = get_config()

        mg = []
        print("searching in mobygames dataset ...")
        for entry in tqdm(self.mobygames_entries()):
            added = False
            if query:
                for title in self.iter_titles(entry):
                    if query.lower() in title.lower():
                        mg.append({
                            "title": entry["title"],
                            "id": entry["id"]
                        })
                        print("\n- "+entry["title"])
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
                            print("\n- "+entry["title"])                            
                            break

        self.build_gamelist(mg)
