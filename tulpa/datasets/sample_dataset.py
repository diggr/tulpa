import random
from ..utils import save_json, open_yaml

def build_sample_dataset(sample_size, sample_dataset_filename, gamelist_filename):
    """
    Draw a random sample from the tulpa gamelist file.

    The sample of uniform probability, i.e. every entry in the gamelist has the
    same chance to appear in it.
    """
    games = open_yaml(gamelist_filename)
    choices = random.choices(list(games.keys()), k=sample_size)
    sample = {choice: games[choice] for choice in choices}

    save_json(sample, sample_dataset_filename)
    return sample_dataset_filename
