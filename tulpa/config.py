import yaml
from pathlib import Path

PROVIT_AGENT = "tulpa_0.1.0"

CONFIG_FILE = "config.yml"

CONFIG_TEMPLATE = {
    "project_name": "tulpa",
    "daft": ""
}

def init_config():
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(CONFIG_TEMPLATE, f, default_flow_style=False)

class Config:

    def __init__(self):
        with open(CONFIG_FILE) as f:
            cf = yaml.safe_load(f)
        
        datasets_dir = Path("datasets")
        visualizations_dir = Path("visualizations")
        import_dir = Path('import')

        self.dirs = {
            "datasets": datasets_dir,
            "visualizations": visualizations_dir,
            "games_dataset": datasets_dir / "games",
            "releases_dataset": datasets_dir / "releases",
            "credits_network": visualizations_dir / "credits_network",
            "release_timeline": visualizations_dir / "release_timeline",
            "staff_heatmap": visualizations_dir / "staff_heatmap"
        }

        self.datasets = {
            "games": self.dirs["games_dataset"] / "{}_games.json".format(cf["project_name"]),
            "releases": self.dirs["releases_dataset"] / "{}_releases.json".format(cf["project_name"])
        }

        
        self.project_name = cf["project_name"]
        self.daft = cf["daft"]

def get_config():
    if Path(CONFIG_FILE).exists():
        return Config()
    else:
        raise FileExistsError("config.yml does not exists")