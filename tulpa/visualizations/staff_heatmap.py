import json
import sys
import pandas as pd
import requests
import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from ..datasets.builder import Builder
from collections import defaultdict, Counter
from ..utils import open_json

class StaffHeatmapBuilder(Builder):

    PROVIT_ACTIVITY = "build_staff_heatmap"
    PROVIT_DESCRIPTION = (
        "Heatmap of the top {n} staffmembers working on most games in the dataset."
    )
    HEATMAP_FILENAME= "{project_name}_staff_heatmap_topn_{n}.{out_format}"

    def __init__(self, games_dataset_path, diggr_api_url, n, title):
        self.games = open_json(games_dataset_path)
        self.plot_title = title
        self._n = n
        self.daft = diggr_api_url + "/mobygames/slug/{slug}"

        super().__init__([games_dataset_path], "mobygames")


    def find_vips(self):
        vips = Counter()
        for entry in self.dataset:
            credits = entry["credits"]
            for (name, roles) in credits:
                vips[self.developers[name]] += 1  # len(roles) #1
        return vips

    def build_dataset(self, outfilename):
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

        plt.tight_layout()
        plt.savefig(outfilename)

        return outfilename


def build_staff_heatmap(
        games_dataset_path,
        diggr_api_url,
        project_name,
        staff_heatmap_path,
        n=30,
        out_format="png",
        title="Staff Heatmap",
    ):
        """
        Staff Heatmap Factory
        """
        shb = StaffHeatmapBuilder(games_dataset_path, diggr_api_url, n, title)
        outfilename = staff_heatmap_path / shb.HEATMAP_FILENAME.format(
            project_name = project_name,
            n = n,
            out_format = out_format
        )
        outfilename = shb.build(outfilename)
        return outfilename


