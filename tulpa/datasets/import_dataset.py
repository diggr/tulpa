import json
import yaml
from ..config import get_config
from ..utils import print_last_prov_entry


def build_import_dataset():
    
    cf = get_config()
    dataset_file = cf.datasets["games"]

    with open(dataset_file) as f:
        games = json.load(f)

    with open("import/games.yml", "w") as f:
        yaml.dump(games, f, default_flow_style=False)