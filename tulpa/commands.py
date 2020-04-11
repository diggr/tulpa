from pathlib import Path
from .config import get_config
from .datasets.samples_dataset import draw_gamelist_sample
from .datasets.releases_dataset import ReleasesDatasetBuilder
from .visualizations.credits_network import CreditsNetwork
from .visualizations.release_timeline import ReleaseTimelineBuilder
from .visualizations.staff_heatmap import StaffHeatmap
from .visualizations.staff_size import StaffSizeChart
from .utils import print_last_prov_entry
from .gamelist import GamelistGenerator
from .config import get_config

cfg = get_config()

def draw_sample(sample_size):
    cfg = get_config()
    gg = GamelistGenerator(cfg.daft, cfg.gamelist_file)
    gg.draw_sample(sample_size)


def build_gamelist(query, company):
    cfg = get_config()
    gg = GamelistGenerator(cfg.daft, cfg.gamelist_file)
    gg.build_by_query_or_company(query, company)


def show_datasets():
    for name, dataset in cfg.datasets.items():
        if Path(dataset).exists():
            print(f"\t- [{name}] {dataset}")
            print_last_prov_entry(dataset)


def build_release_timeline(title):
    print("building timeline ...")
    ReleaseTimelineBuilder(title)


def build_staff_heatmap(n, out_format):
    print("building heatmap ...")
    StaffHeatmap(n, out_format)


def build_release_dataset(force):
    cf = get_config()

    if Path(cf.datasets["releases"]).exists() and not force:
        print("Dataset already exists. Use '--force' option to rebuild the dataset.")
    else:
        print("building dataset ...")
        ReleasesDatasetBuilder()
