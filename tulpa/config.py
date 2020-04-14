from pathlib import Path
from .settings import DIGGR_API

PROVIT_AGENT = "tulpa_0.1.0"
CONFIG_FILE = "config.yml"


class Config:
    def __init__(self, diggr_api_url=DIGGR_API):

        base_path = Path(".")

        datasets_dir = base_path / "datasets"
        visualizations_dir = base_path / "visualizations"

        self.project_name = base_path.resolve().name
        self.daft = diggr_api_url
        self.gamelist_file = "{}.yml".format(self.project_name)

        self.dirs = {
            "datasets": datasets_dir,
            "visualizations": visualizations_dir,
            "games_dataset": datasets_dir / "games",
            "sample_dataset": datasets_dir / "sample",
            "companies_dataset": datasets_dir / "companies",
            "releases_dataset": datasets_dir / "releases",
            "credits_network": visualizations_dir / "credits_network",
            "release_timeline": visualizations_dir / "release_timeline",
            "staff_heatmap": visualizations_dir / "staff_heatmap",
            "staff_size_chart": visualizations_dir / "staff_size_chart",
            "games_data_table": visualizations_dir / "games_data_table",
        }

        self.datasets = {
            "sample": self.dirs["sample_dataset"]
            / f"{self.project_name}_sample.json",
            "games": self.dirs["games_dataset"] / f"{self.project_name}_games.json",
            "companies": self.dirs["companies_dataset"]
            / f"{self.project_name}_companies.json",
            "releases": self.dirs["releases_dataset"]
            / f"{self.project_name}_releases.json",
        }


def get_config():
    return Config()
