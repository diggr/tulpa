import json
import requests
import os

from dateutil.parser import parse
from jinja2 import Template
from ..config import PROVIT_AGENT
from pathlib import Path
from provit import Provenance
from ..utils import open_json


class ReleaseTimelineBuilder:

    PROVIT_ACTIVITY = "build_release_timeline"
    PROVIT_DESCRIPTION = "Interactive release timeline based on GameFAQs release information."

    def __init__(self, title, games_dataset_path, releases_dataset_path, diggr_api_url):
        self.title = title
        self.daft = diggr_api_url + "/mobygames/slug/{slug}"
        self.games_dataset_path = games_dataset_path
        self.games = open_json(games_dataset_path)
        self.releases_dataset_path = releases_dataset_path
        self.releases = open_json(releases_dataset_path)


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

    def get_date(self, info, region):
        if not region in info:
            return None

        release = sorted(info[region], key=lambda x: x["date"])[0]
        release["region"] = region
        if release["date"] != "Canceled":
            if parse(release["date"]):
                return release

        return None


    def build_dataset(self):

        self.years = set()
        self.dataset = []
        for title, info in self.releases.items():
            releases = []

            cover = self.getCover(title)

            release = self.get_date(info, "JP")
            if release:
                releases.append(release)
                self.years.add(int(release["date"][:4]))

            release = self.get_date(info, "US")
            if release:
                releases.append(release)
                try:
                    self.years.add(int(release["date"][:4]))
                except:
                    print("invalid date format {}".format(release["date"]))

            release = self.get_date(info, "EU")
            if release:
                releases.append(release)
                self.years.add(int(release["date"][:4]))


            self.dataset.append([title, releases, cover])


    def build_vis(self, outfilename, template):

        visualization = template.render(
            dataset=repr(json.dumps(self.dataset)),
            years=repr(json.dumps(list(self.years))),
            title=self.title
        )

        with open(outfilename, "w") as outfile:
            outfile.write(visualization)

        prov = Provenance(outfilename, overwrite=True)
        prov.add(
            agents=[ PROVIT_AGENT ],
            activity=self.PROVIT_ACTIVITY,
            description=self.PROVIT_DESCRIPTION
        )
        prov.add_sources([self.games_dataset_path, self.releases_dataset_path])
        prov.add_primary_source("mobygames")
        prov.save()

        return outfilename

def build_release_timeline(title, games_dataset_path, releases_dataset_path, diggr_api_url,
        project_name, release_timeline_path):
    """
    Release Timeline Factory
    """
    template_path = Path(__file__).parent / "templates" / "release_vis.html"
    with open(template_path) as template_file:
        template = Template(template_file.read())
    rtb = ReleaseTimelineBuilder(title, games_dataset_path, releases_dataset_path, diggr_api_url)
    rtb.build_dataset()
    outpath = release_timeline_path / f"{project_name}_release_timeline.html"
    return rtb.build_vis(outpath, template)
