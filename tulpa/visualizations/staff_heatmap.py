import json
import sys
import pandas as pd
import requests
import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from provit import Provenance
from collections import defaultdict, Counter
from ..config import get_config, PROVIT_AGENT

PROVIT_ACTIVITY = "build_staff_heatmap"
PROVIT_DESCRIPTION = (
    "Heatmap of the top {n} staffmembers working on most games in the dataset."
)


class StaffHeatmap:
    def __init__(self, n=30, out_format="png", title="Staff Heatmap"):

        self.plot_title = title
        self._n = n
        self.out_format = out_format

        self.cf = get_config()
        self.daft = self.cf.daft + "/mobygames/slug/{slug}"

        with open(self.cf.datasets["games"]) as f:
            self.games = json.load(f)

        self.build_heatmap()

    def find_vips(self):
        vips = Counter()
        for entry in self.dataset:
            credits = entry["credits"]
            for (name, roles) in credits:
                vips[self.developers[name]] += 1  # len(roles) #1
        return vips

    # build credits dataset
    def build_heatmap(self):
        self.dataset = []
        self.developers = {}

        for title, links in self.games.items():
            years = []

            current = {}
            new = defaultdict(set)

            for slug in links["mobygames"]:

                try:
                    rsp = requests.get(self.daft.format(slug=slug))
                    data = rsp.json()["entry"]
                    raw = data["raw"]
                except:
                    print("{} not in dataset\n".format(slug))
                    continue

                current_platform = ""
                for platform in raw["platforms"]:
                    years.append(platform["first_release_date"][:4])
                    for credits in platform["credits"]:
                        for credit in credits["credits"]:
                            if credit["developer_id"]:
                                new[credit["developer_id"]].add(credits["role"])
                                self.developers[credit["developer_id"]] = credit["name"]

            if len(new) > 0:
                sorted_credits = sorted(
                    [(x, list(y)) for x, y in dict(new).items()],
                    key=lambda x: len(x[1]),
                    reverse=True,
                )
                if len(title) < 30:
                    title = "{} | {}".format(sorted(years)[0], title)
                else:
                    title = "{} | {} ...".format(sorted(years)[0], title[:28])

                if len(new) > 0:
                    self.dataset.append(
                        {"slug": slug, "title": title, "credits": sorted_credits}
                    )

        vips = self.find_vips()

        credits_map = defaultdict(dict)
        for entry in self.dataset:
            game = entry["title"]
            credits = entry["credits"]
            for (name, roles) in credits:
                credits_map[self.developers[name]][game] = len(roles)

        # build final dataset
        df = pd.DataFrame(credits_map)
        df = df.sort_index().transpose()
        df = df.sort_values(by=list(df.columns), ascending=False, na_position="last")[
            ::-1
        ]
        topn = [x[0] for x in vips.most_common(self._n)]
        dataset = df.loc[df.index.isin(topn)].fillna(0)

        # create plot
        fig, ax = plt.subplots(figsize=(len(self.games) / 3, self._n / 3))
        c = plt.pcolor(dataset, cmap="hot")
        plt.title(self.plot_title, y=1.03)
        plt.yticks(np.arange(0.5, len(dataset.index), 1), dataset.index)
        plt.xticks(np.arange(0.5, len(dataset.columns), 1), dataset.columns)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=-45, ha="left")
        cb = plt.colorbar(c, ticks=range(int(max(dataset.max())) + 1))

        # save plot
        filepath = self.cf.dirs["staff_heatmap"] / "{}_staff_heatmap_topn_{}.{}".format(
            self.cf.project_name, self._n, self.out_format
        )
        plt.tight_layout()
        plt.savefig(filepath)

        print("\nSave visualization ...")
        print("File location: {}".format(filepath))

        prov = Provenance(filepath, overwrite=True)
        prov.add(
            agents=[PROVIT_AGENT],
            activity=PROVIT_ACTIVITY,
            description=PROVIT_DESCRIPTION,
        )
        prov.add_sources([self.cf.datasets["games"]])
        prov.add_primary_source("mobygames")
        prov.save()
