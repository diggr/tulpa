"""
Tulpa command line interface

Command structure:

tulpa   gamelist    build
                    update
        dataset     games
                    releases
                    companies
        vis         release-timeline
                    staff-heatmap
                    credits-network
                    company-network

"""

import os
import click
import tulpa as tp

@click.group()
def cli():
    pass

@cli.command()
def init():
    tp.initialize_project()

@cli.command()
def datasets():
    tp.show_datasets()


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
    tp.update_gamelist(force)

#
# dataset commands
#

@cli.group()
def dataset():
    pass

@dataset.command()
@click.option('--force/--no-force', default=False)
def games(force):
    tp.build_games_dataset(force)

@dataset.command()
@click.option('--force/--no-force', default=False)
def releases(force):
    tp.build_release_dataset(force)

@dataset.command()
@click.option('--force/--no-force', default=False)
def companies(force):
    tp.CompanyDatasetBuilder()

#
# vis commands
#

@cli.group()
def vis():
    pass

@vis.command()
@click.option("--title", "-t", default="Release Timeline")
def release_timeline(title):
    tp.build_release_timeline(title)

@vis.command()
@click.option("-n", default=30)
@click.option("--output_format", "-o", default="png" )
def staff_heatmap(n, output_format):
    tp.build_staff_heatmap(n, output_format)

@vis.command()
def credits_network():
    tp.build_credits_network()

@vis.command()
def staff_size():
    tp.build_staff_size_chart()

@vis.command()
def games_data_table():
    tp.build_games_data_table()
