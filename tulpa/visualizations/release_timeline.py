import json
import requests
import os
from provit import Provenance
from jinja2 import Environment, FileSystemLoader
from ..config import get_config, PROVIT_AGENT

PROVIT_ACTIVITY = "build_release_timeline"
PROVIT_DESCRIPTION = "Interactive release timeline based on GameFAQs release information."


class ReleaseTimelineBuilder:

    def __init__(self, title):
        self.title = title

        self.cf = get_config()

        self.daft = self.cf.daft + "/mobygames/slug/{slug}"

        with open(self.cf.datasets["games"]) as f:
            self.games = json.load(f)

        with open(self.cf.datasets["releases"]) as f:
            self.releases = json.load(f)

        self.build_dataset()
        self.build_vis()

    def getCover(self, title):
        
        try:
            mobygames_id = self.games[title]["mobygames"][0]
            rsp = requests.get(self.daft.format(slug=mobygames_id))
            data = rsp.json()["entry"]["raw"]
            for platform in data["platforms"]:
                for cover_group in platform["cover_groups"]:
                    for cover in cover_group["covers"]:
                        if cover["scan_of"] == "Front Cover":
                            return cover["image"]
            return ""
        except:
            return ""    


    def build_dataset(self):

        self.years = set()           
        self.dataset = []
        for title, info in self.releases.items():
            releases = []
            
            cover = self.getCover(title)
            try:
                release = sorted(info["JP"], key=lambda x: x["date"])[0]
                release["region"] = 'JP'
                releases.append(release)
                self.years.add(int(release["date"][:4]))
            except:
                print("no JP release for ", title)
                
            try:
                release = sorted(info["US"], key=lambda x: x["date"])[0]
                release["region"] = 'US'     
                if release["date"] != 'Canceled':
                    releases.append(release)
                    self.years.add(int(release["date"][:4]))
            except:
                print("no US release for ", title)

            try:
                release = sorted(info["EU"], key=lambda x: x["date"])[0]
                release["region"] = 'EU'        
                releases.append(release)
                self.years.add(int(release["date"][:4]))
            except:
                print("no EU release for ", title)
                
            self.dataset.append([title, releases, cover])        


    def build_vis(self):

        root = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(root, 'templates')
        env = Environment( loader = FileSystemLoader(templates_dir) )
        template = env.get_template('release_vis.html')

        filepath = self.cf.dirs["release_timeline"] / "{}_release_timeline.html".format(self.cf.project_name)

        with open(filepath, 'w') as f:
            f.write(template.render(
                dataset=repr(json.dumps(self.dataset)),
                years=repr(json.dumps(list(self.years))),
                title=self.title
            ))

        print("\nSave visualization ...")
        print("File location: {}".format(filepath))

        prov = Provenance(filepath, overwrite=True)
        prov.add(
            agents=[ PROVIT_AGENT ],
            activity=PROVIT_ACTIVITY,
            description=PROVIT_DESCRIPTION
        )
        prov.add_sources([self.cf.datasets["games"], self.cf.datasets["releases"]])
        prov.add_primary_source("mobygames")
        prov.save()            