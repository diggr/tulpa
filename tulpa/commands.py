from pathlib import Path
from .config import get_config, init_config
from .datasets.games_dataset import check_games_dataset, build_games_dataset
from .datasets.releases_dataset import ReleasesDatasetBuilder
from .datasets.import_dataset import build_import_dataset
from .visualizations.credits_network import CreditsNetwork
from .visualizations.release_timeline import ReleaseTimelineBuilder
from .visualizations.staff_heatmap import StaffHeatmap
from .utils import print_last_prov_entry
from .gamelist import GamelistGenerator


def build_gamelist(query, company):
    gg = GamelistGenerator(query, company)

def show_datasets():
    cf = get_config()

    print("Available datasets:\n")
    for name, dataset in cf.datasets.items():
        if Path(dataset).exists():
            print("\t- [{}] {}".format(name, dataset))

            print_last_prov_entry(dataset)
                    
def check_dataset(dataset):

    if dataset == "games":
        check_games_dataset()
    else:
        print("Dataset not available!")

def initialize_project():  
    print("initialize tulpa project")
    init_config()

    cfg = get_config()
    for directory in cfg.dirs.values():
        if not Path(directory).exists():
            Path(directory).mkdir()

def build_visualization(visualization, title, n, out_format):

    if visualization == "credits-network":
        print("building network ...")
        CreditsNetwork()
    elif visualization == "release-timeline":
        print("building timeline ...")
        ReleaseTimelineBuilder(title)
    elif visualization == "staff-heatmap":
        print("building heatmap ...")
        StaffHeatmap(n, out_format)
    else:
        print("Unknown visualization!")


def build_dataset(dataset, force):
    cf = get_config()
    if dataset == "releases":

        if Path(cf.datasets["releases"]).exists() and not force:
            print("Dataset already exists. Use '--force' option to rebuild the dataset.")
        else:
            print("building dataset ...")            
            ReleasesDatasetBuilder()

    elif dataset == "import":
        if force:
            build_import_dataset()

    elif dataset == "games":
        build_games_dataset()

    else:
        print("Unknown dataset!")        
