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

@cli.command()
@click.argument("dataset")
def check(dataset):
    tp.check_dataset(dataset)

@cli.group()
def build():
    pass

@build.command()
@click.argument("visualization")
@click.option("--title", "-t", default="Release Timeline")
@click.option("-n", default=30)
@click.option("--output_format", "-o", default="png" )
def vis(visualization, title, n, output_format):
    tp.build_visualization(visualization, title, n, output_format)


@build.command()
@click.argument("dataset")
@click.option('--force/--no-force', default=False)
def dataset(dataset, force):
    tp.build_dataset(dataset, force)    