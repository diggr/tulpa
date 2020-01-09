import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from provit import Provenance
from collections import defaultdict, Counter
from ..config import get_config, PROVIT_AGENT

PROVIT_ACTIVITY = "build_staff_heatmap"
PROVIT_DESCRIPTION = "Heatmap of the top {n} staffmembers working on most games in the dataset."

class StaffSizeChart:
    def __init__(self, title="Staff Size Development"):
        self.title = title

        self.cf = get_config()
        self.daft = self.cf.daft + "/mobygames/{id}"

        with open(self.cf.datasets["games"]) as f:
            self.games = json.load(f)

        self.build_staff_size_chart()


    def build_staff_size_chart(self):
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

        labels = [ x[0] for x in sorted_dataset if x[1] > 0 ]
        y_pos = np.arange(len(labels))
        values = [ x[1] for x in sorted_dataset  if x[1] > 0 ]

        fig, ax = plt.subplots(figsize=(len(labels)/1,12))

        plt.bar(y_pos, values, align='center', alpha=0.5)
        plt.xticks(y_pos, labels)
        plt.ylabel('Staff size')
        plt.title(self.title)
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=-45, ha="left" )
        plt.gcf().subplots_adjust(bottom=0.3 )


        plt.show()

        print(dataset)
