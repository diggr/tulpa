import yaml
from pathlib import Path

PROVIT_AGENT = "tulpa_0.1.0"

CONFIG_FILE = "config.yml"

CONFIG_TEMPLATE = {
    "project_name": "tulpa",
    "daft": "",
    "lemongrab_dir": ""
}

def init_config(project_name=None, daft_url=None, lemongrab_dir=None):
    config = CONFIG_TEMPLATE.copy()

    config["project_name"] = project_name if project_name else ""
    config["daft"] = daft_url if daft_url else ""
    config["lemongrab_dir"] = lemongrab_dir if lemongrab_dir else ""

    with open(CONFIG_FILE, "w") as config_file:
        yaml.dump(config, config_file, default_flow_style=False)

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
            "samples_dataset": datasets_dir / "samples",
            "companies_dataset": datasets_dir / "companies",
            "releases_dataset": datasets_dir / "releases",
            "credits_network": visualizations_dir / "credits_network",
            "release_timeline": visualizations_dir / "release_timeline",
            "staff_heatmap": visualizations_dir / "staff_heatmap",
            "games_data_table": visualizations_dir / "games_data_table"
        }

        self.datasets = {
            "samples": self.dirs["samples_dataset"] / "{}_samples.json".format(cf["project_name"]),
            "games": self.dirs["games_dataset"] / "{}_games.json".format(cf["project_name"]),
            "companies": self.dirs["companies_dataset"] / "{}_companies.json".format(cf["project_name"]),
            "releases": self.dirs["releases_dataset"] / "{}_releases.json".format(cf["project_name"])
        }


        self.project_name = cf["project_name"]
        self.daft = cf["daft"]
        self.lemongrab = cf["lemongrab_dir"]
        self.gamelist_file = "{}.yml".format(self.project_name)

def get_config():
    if Path(CONFIG_FILE).exists():
        return Config()
    else:
        raise FileExistsError("config.yml does not exists")
