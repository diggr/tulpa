import click
import os
import requests
import sys
import tulpa as tp

from .config import get_config
from .datasets.company_dataset import CompanyDatasetBuilder
from .datasets.games_dataset import build_games_dataset
from .datasets.import_dataset import build_import_dataset
from .datasets.releases_dataset import build_releases_dataset
from .visualizations.credits_network import CreditsNetwork
from .visualizations.games_data_table import GamesDataTableBuilder
from .visualizations.staff_size import StaffSizeChart

cfg = get_config()

@click.group()
def cli():
    """
    tulpa - Build visualizations and analysis for a list of video games.
    """
    pass


@cli.command()
def datasets():
    """
    Show available datasets.
    """
    print("Available datasets:\n")
    tp.get_datasets()


@cli.group()
def sample():
    """
    Draw samples from a gamelist or mobygames.
    """
    pass

@sample.command()
@click.argument("size", type=click.INT)
def draw(size):
    """
    Draws a random sample of SIZE.

    It uses the random.choices() function of python to draw a random sample
    of size SIZE from all mobygames_ids. I.e. every mobygames ID has the same
    probability to appear in the sample.
    """
    print(f"Drawing sample of size {size}")
    tp.draw_sample(size)

@sample.command()
@click.option("--out", default=None, help="Provide a filename for the output file")
@click.argument("size", type=click.INT)
def draw_from_gamelist(out, size):
    """
    Draws a random sample from the gamelist of SIZE.

    It uses the random.choices() function of python to draw a random sample
    of size SIZE from all games in the gamelist.

    Can be given a special
    """
    print(f"Drawing sample of size {size} from gamelist")
    outfilename = tp.draw_gamelist_sample(size, out)
    print(f"File location: {outfilename}")
#
# gamelist commands
#

@cli.group()
def gamelist():
    pass

@gamelist.command()
@click.option("--query", "-q", default=None)
@click.option("--company","-c", default=None)
def build(query, company):
    tp.build_gamelist(query, company)

@gamelist.command()
@click.option('--force/--no-force', default=False)
def update(force):
    print("Updating gamelist...")
    build_import_dataset()

#
# dataset commands
#

@cli.group()
def dataset():
    """
    Build datasets for further research (e.g. with games, releases or companies)
    """
    pass

@dataset.command()
def games():
    """
    Build games dataset from gamelist file by adding companies and links from
    mobygames.
    """
    print("Building games dataset...")
    outfilename = build_games_dataset()
    print(f"File saved to: {outfilename}")

@dataset.command()
@click.option('--force/--no-force', default=False)
def releases(force):
    """
    Build a dataset of all releases found in the games dataset.
    """
    print("Building releases dataset...")
    try:
        outfilename = build_releases_dataset(
            cfg.datasets["releases"],
            cfg.datasets["games"],
            cfg.daft,
            force
        )
    except (FileNotFoundError, FileExistsError) as e:
        sys.exit(e)
    print(f"Done. File saved to {outfilename}")

@dataset.command()
@click.option('--force/--no-force', default=False)
def companies(force):
    tp.CompanyDatasetBuilder()

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
    tp.build_release_timeline(title)

@vis.command()
@click.option("-n", default=30)
@click.option("--output_format", "-o", default="png" )
def staff_heatmap(n, output_format):
    """
    Build a heatmap showing involment of persons across games.
    """
    tp.build_staff_heatmap(n, output_format)

@vis.command()
def credits_network():
    CreditsNetwork()

@vis.command()
def staff_size():
    StaffSizeChart()

@vis.command()
def games_data_table():
    print("Building GamesDataTable...")
    GamesDataTableBuilder()
