import json
import yaml

from provit import Provenance

def initialize(dirs):
    for path in dirs.values():
        try:
            path.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            raise RuntimeError(
                f"{path} exists. It is a file, but needs to be a directory of the same name"
            )


def save_json(data, outfilename):
    """
    Wrapper around json.dump().
    Accepts data and filename.
    """
    with open(outfilename, "w") as outfile:
        json.dump(data, outfile, indent=4)


def open_json(infilename):
    """
    Wrapper around json.load().
    Accepts a filename.
    """
    with open(infilename) as infile:
        return json.load(infile)


def open_yaml(infilename):
    """
    Wrapper around yaml.safe_load().
    Accepts a filename and returns a Python object (list, dict, ...)
    """
    with open(infilename, "r") as infile:
        return yaml.safe_load(infile)


def save_yaml(data, outfilename):
    """
    Wrapper around yaml.dump().
    Accepts data and filename and returns the filename.
    """
    with open(outfilename, "w") as outfile:
        return yaml.dump(data, outfile, default_flow_style=False)


def prov_slug(uri):
    return uri.split("/")[-1]


def print_last_prov_entry(filepath):

    prov = Provenance(filepath)
    last_entry = prov.tree()
    if not last_entry:
        print("\n\t  No provenance information available")
    else:
        print(
            "\n\t  Last provenance entry ({}):\n\t  '{}' ({})\n".format(
                last_entry["ended_at"],
                last_entry["activity_desc"],
                ", ".join([prov_slug(x) for x in last_entry["agent"]]),
            )
        )
