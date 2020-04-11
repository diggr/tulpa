from pathlib import Path
from .config import get_config
from .visualizations.staff_heatmap import StaffHeatmap
from .utils import print_last_prov_entry
from .gamelist import GamelistGenerator

cfg = get_config()


def draw_sample(sample_size):
    gg = GamelistGenerator(cfg.daft, cfg.gamelist_file)
    gg.draw_sample(sample_size)


def build_gamelist(query, company):
    gg = GamelistGenerator(cfg.daft, cfg.gamelist_file)
    gg.build_by_query_or_company(query, company)


def show_datasets():
    for name, dataset in cfg.datasets.items():
        if Path(dataset).exists():
            print(f"\t- [{name}] {dataset}")
            print_last_prov_entry(dataset)


def build_staff_heatmap(n, out_format):
    print("building heatmap ...")
    StaffHeatmap(n, out_format)
