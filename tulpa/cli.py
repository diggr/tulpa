import click
import sys

from .config import get_config
from .datasets.companies_dataset import build_companies_dataset
from .datasets.games_dataset import build_games_dataset
from .datasets.import_dataset import build_import_dataset
from .datasets.releases_dataset import build_releases_dataset
from .datasets.sample_dataset import build_sample_dataset
from .gamelist import draw_sample, build_gamelist
from pathlib import Path
from .utils import initialize, print_last_prov_entry
from .visualizations.credits_network import build_credits_network
from .visualizations.games_data_table import GamesDataTableBuilder
from .visualizations.release_timeline import build_release_timeline
from .visualizations.staff_heatmap import build_staff_heatmap
from .visualizations.staff_size import StaffSizeChart

cfg = get_config()


@click.group()
def cli():
    """
    tulpa - Build visualizations and analysis for a list of video games.
    """
    pass

@cli.command()
def init():
    """
    Initialize tulpa in the current working directory.
    """
    print("Initializing tulpa...")
    try:
        this_dir = initialize(cfg.dirs)
    except RuntimeError as e:
        sys.exit(e)
    print(f"Initialized tulpa project {cfg.project_name}")


@cli.command()
def datasets():
    """
    Show available datasets.
    """
    print("Available datasets:\n")
    for name, dataset in cfg.datasets.items():
        if Path(dataset).exists():
            print(f"\t- [{name}] {dataset}")
            print_last_prov_entry(dataset)


#
# gamelist commands
#


@cli.group()
def gamelist():
    """
    Gamelist generation by sample, query or company.
    """
    pass


@gamelist.command()
@click.option("--query", "-q", default=None)
@click.option("--company", "-c", default=None)
def build(query, company):
    """
    Builds a gamelist by fetching data from mobygames according
    to the given query and/or company.
    """
    print("Building gamelist...")
    outfilename = build_gamelist(
        query,
        company,
    )
    print(f"File saved to: {outfilename}")


@gamelist.command()
@click.option("--force/--no-force", default=False)
def update(force):
    print("Updating gamelist...")
    try:
        outfilename = build_import_dataset(
            cfg.datasets["games"],
            cfg.gamelist_file,
            force
        )
    except FileExistsError as e:
        sys.exit(e)
    print(f"Done. Gamelist saved to: {outfilename}")


@gamelist.command()
@click.argument("size", type=click.INT)
def sample(size):
    """
    Builds a gamelist by drawing a random sample of SIZE from mobygames.

    It uses the random.choices() function of python to draw a random sample
    of size SIZE from all mobygames_ids. I.e. every mobygames ID has the same
    probability to appear in the sample.
    """
    print(f"Drawing sample of size {size}")
    outfilename = draw_sample(
        size,
        cfg.daft,
        cfg.gamelist_file
    )
    print(f"Done. File saved to: {outfilename}")


@cli.group()
def dataset():
    """
    Build datasets for further research (e.g. with games, releases or companies)
    """
    pass


@dataset.command()
@click.option("--out", default=None, help="Provide a filename for the output file")
@click.argument("size", type=click.INT)
def sample(out, size):
    """
    Draws a random sample from the gamelist of SIZE.

    It uses the random.choices() function of python to draw a random sample
    of size SIZE from all games in the gamelist.

    Can be given a special
    """
    print(f"Drawing sample of size {size} from gamelist")
    if not out:
        out = cfg.datasets["sample"]
    outfilename = build_sample_dataset(
        size,
        out,
        cfg.gamelist_file
    )
    print(f"File location: {outfilename}")


@dataset.command()
def games():
    """
    Build games dataset from gamelist file by adding companies and links from
    mobygames.
    """
    print("Building games dataset...")
    outfilename = build_games_dataset(
        cfg.datasets["games"],
        cfg.gamelist_file,
        cfg.daft
    )
    print(f"File saved to: {outfilename}")


@dataset.command()
@click.option("--force/--no-force", default=False)
def releases(force):
    """
    Build a dataset of all releases found in the games dataset.
    """
    print("Building releases dataset...")
    try:
        outfilename = build_releases_dataset(
            cfg.datasets["releases"], cfg.datasets["games"], cfg.daft, force
        )
    except (FileNotFoundError, FileExistsError) as e:
        sys.exit(e)
    print(f"Done. File saved to {outfilename}")


@dataset.command()
def companies():
    print("Building companies dataset...")
    outfilename = build_companies_dataset(
        cfg.datasets["companies"],
        cfg.datasets["games"],
        cfg.daft,
    )
    print(f"Done. File saved to {outfilename}")



#
# vis commands
#


@cli.group()
def vis():
    """
    Build visualizations from the generated datasets.
    """
    pass


@vis.command()
@click.option("--title", "-t", default="Release Timeline")
def release_timeline(title):
    """
    Show releases in chronological order
    """
    print("Building release timeline...")
    outfilename = build_release_timeline(
        title,
        cfg.datasets["games"],
        cfg.datasets["releases"],
        cfg.daft,
        cfg.project_name,
        cfg.dirs["release_timeline"],
    )
    print(f"Done. File saved to {outfilename}")


@vis.command()
@click.option("-n", default=30)
@click.option("--output_format", "-o", default="png")
@click.option("--title", default="Stafft Heatmap")
def staff_heatmap(n, output_format, title):
    """
    Build a heatmap showing involment of persons across games.
    """
    print("Building staff heatmap...")
    outfilename = build_staff_heatmap(
        cfg.datasets["games"],
        cfg.daft,
        cfg.project_name,
        cfg.dirs["staff_heatmap"],
        n,
        output_format,
        title
    )
    print(f"Done. File saved to {outfilename}")


@vis.command()
def credits_network():
    print("Building crecits network...")
    outfilename, missing_credits = build_credits_network(
        cfg.datasets["games"],
        cfg.daft,
        cfg.project_name,
        cfg.dirs["credits_network"],
    )
    if missing_credits:
        for game in missing_credits:
            print(f"\tNo credits available for {game}")
    print(f"Done. File saved to {outfilename}")


@vis.command()
def staff_size():
    StaffSizeChart()


@vis.command()
def games_data_table():
    print("Building GamesDataTable...")
    GamesDataTableBuilder()
