from pathlib import Path
from ..utils import open_json, save_yaml


def build_import_dataset(games_dataset_path, gamelist_file, force=False):
    if Path(gamelist_file).exists() and not force:
        raise FileExistsError("Gamelist file exists. Use --force to overwrite.")
    return save_yaml(open_json(games_dataset_path), gamelist_file)
