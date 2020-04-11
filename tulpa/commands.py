from pathlib import Path
from .config import get_config
from .datasets.games_dataset import check_games_dataset, build_games_dataset
from .datasets.samples_dataset import draw_gamelist_sample
from .datasets.company_dataset import CompanyDatasetBuilder
from .datasets.releases_dataset import ReleasesDatasetBuilder
from .datasets.import_dataset import build_import_dataset
from .visualizations.credits_network import CreditsNetwork
from .visualizations.release_timeline import ReleaseTimelineBuilder
from .visualizations.staff_heatmap import StaffHeatmap
from .visualizations.staff_size import StaffSizeChart
from .visualizations.games_data_table import GamesDataTableBuilder
from .utils import print_last_prov_entry
from .gamelist import GamelistGenerator
from .config import get_config


def draw_sample(sample_size):
    cfg = get_config()
    gg = GamelistGenerator(cfg.daft, cfg.gamelist_file)
    gg.draw_sample(sample_size)


def build_company_dataset():
    cdb = CompanyDatasetBuilder()


def build_gamelist(query, company):
    cfg = get_config()
    gg = GamelistGenerator(cfg.daft, cfg.gamelist_file)
    gg.build_by_query_or_company(query, company)


def show_datasets():
    cf = get_config()

    print("Available datasets:\n")
    for name, dataset in cf.datasets.items():
        if Path(dataset).exists():
            print("\t- [{}] {}".format(name, dataset))

            print_last_prov_entry(dataset)


def build_release_timeline(title):
    print("building timeline ...")
    ReleaseTimelineBuilder(title)


def build_staff_heatmap(n, out_format):
    print("building heatmap ...")
    StaffHeatmap(n, out_format)

def build_credits_network():
    print("building network ...")
    CreditsNetwork()

def build_staff_size_chart():
    print("building staff size chart")
    StaffSizeChart()


def build_release_dataset(force):
    cf = get_config()

    if Path(cf.datasets["releases"]).exists() and not force:
        print("Dataset already exists. Use '--force' option to rebuild the dataset.")
    else:
        print("building dataset ...")
        ReleasesDatasetBuilder()

def update_gamelist(force):
    print("update gamelist ...")
    build_import_dataset()

def build_games_data_table():
    print("Bulding games data table ...")
    gdt = GamesDataTableBuilder()
