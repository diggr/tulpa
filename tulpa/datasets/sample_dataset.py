import random

from .builder import Builder
from ..utils import save_json, open_yaml

class SampleDatasetBuilder(Builder):
    """
    Draw a random sample from the tulpa gamelist file.

    The sample of uniform probability, i.e. every entry in the gamelist has the
    same chance to appear in it.
    """

    PROVIT_ACTIVITY = "draw_sample"
    PROVIT_DESCRIPTION = "Drawing a uniformly random sample from the gamelist"

    def __init__(self, sample_size, gamelist_file):
        self.sample_size = sample_size
        self.games = open_yaml(gamelist_file)
        super().__init__([gamelist_file])

    def build_dataset(self, outfilename):
        choices = random.choices(list(self.games.keys()), k=self.sample_size)
        sample = {choice: self.games[choice] for choice in choices}
        save_json(sample, outfilename)
        return outfilename


def build_sample_dataset(sample_size, sample_dataset_filename, gamelist_file):
    """
    Sample Dataset Factory
    """
    sdb = SampleDatasetBuilder(sample_size, gamelist_file)
    outfilename = sdb.build(sample_dataset_filename)
    return outfilename
