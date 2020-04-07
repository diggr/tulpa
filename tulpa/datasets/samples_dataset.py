import random
from ..config import get_config
from ..utils import save_json, open_yaml

config = get_config()

def draw_gamelist_sample(sample_size, out):
    """
    Draw a random sample from the tulpa gamelist file.

    The sample of uniform probability, i.e. every entry in the gamelist has the
    same chance to appear in it.
    """
    games = open_yaml(config.gamelist_file)
    choices = random.choices(list(games.keys()), k=sample_size)
    sample = { choice:games[choice] for choice in choices }

    if out is not None:
        outfilename = config.dirs["samples_dataset"] / out
    else:
        outfilename = config.datasets["samples"]

    save_json(sample, outfilename)
    return outfilename
