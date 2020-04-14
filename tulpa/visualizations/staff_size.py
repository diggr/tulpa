import datetime
import json
import requests
import numpy as np
import matplotlib
import re

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from ..datasets.builder import Builder
from collections import defaultdict, Counter
from ..utils import open_json


class StaffSizeChartBuilder(Builder):

    PROVIT_ACTIVITY = "build_staff_size"
    PROVIT_DESCRIPTION = "Building staff size chart."
    STAFF_SIZE_CHART_FILENAME = "{project_name}_staff_size_chart_{timestamp}.{out_format}"

    def __init__(self, games_dataset_path, diggr_api_url, title="Staff Size Development"):
        self.title = title
        self.games = open_json(games_dataset_path)
        self.daft = diggr_api_url + "/mobygames/{id}"

        super().__init__([games_dataset_path], "mobygames")


    def build_dataset(self, outfilename):
        dataset = []

        for title, links in self.games.items():
            developers = set()

            for mg_id in links["mobygames_ids"]:

                try:
                    rsp = requests.get(self.daft.format(id=mg_id))
                    data = rsp.json()["entry"]
                    raw = data["raw"]
                except:
                    print("{} not in dataset\n".format(mg_id))
                    continue

                years = data["years"]
                current_platform = ""
                for platform in raw["platforms"]:
                    for credits in platform["credits"]:
                        for credit in credits["credits"]:
                            if credit["developer_id"]:
                                developers.add(credit["developer_id"])

            id_ = str(min(years)) + "_" + title

            dataset.append((id_, len(developers)))

        sorted_dataset = sorted(dataset, key=lambda x: x[0])

        labels = [x[0] for x in sorted_dataset if x[1] > 0]
        y_pos = np.arange(len(labels))
        values = [x[1] for x in sorted_dataset if x[1] > 0]

        fig, ax = plt.subplots(figsize=(len(labels) / 1, 12))

        plt.bar(y_pos, values, align="center", alpha=0.5)
        plt.xticks(y_pos, labels)
        plt.ylabel("Staff size")
        plt.title(self.title)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=-45, ha="left")
        plt.gcf().subplots_adjust(bottom=0.3)

        plt.tight_layout()
        plt.savefig(outfilename)

        return outfilename

def build_staff_size_chart(
        games_dataset_path,
        diggr_api_url,
        project_name,
        staff_size_chart_path,
        out_format,
        title="Staff Size Development"
    ):
    """
    Staff Size Chart Factory
    """
    sscb = StaffSizeChartBuilder(games_dataset_path, diggr_api_url)
    timestamp = re.sub(
        r"[ :.]",
        "_",
        datetime.datetime.now().isoformat()
    )
    outfilename = sscb.STAFF_SIZE_CHART_FILENAME.format(
        project_name=project_name,
        timestamp=timestamp,
        out_format=out_format
    )
    outfilename = sscb.build(outfilename)
    return outfilename
