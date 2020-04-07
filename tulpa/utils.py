import json
import yaml
from provit import Provenance

def save_json(data, outfilename):
    """
    Wrapper around json.dump().
    Accepts data and filename.
    """
    with open(outfilename, "w") as outfile:
        json.dump(data, outfile, indent=4)

def open_yaml(infilename):
    """
    Wrapper around yaml.safe_load().
    Accepts a filename and returns a Python object (list, dict, ...)
    """
    with open(infilename, "r") as infile:
        return yaml.safe_load(infile)

def prov_slug(uri):
    return uri.split("/")[-1]

def print_last_prov_entry(filepath):

    prov = Provenance(filepath)
    last_entry = prov.tree()
    if not last_entry:
        print("\n\t  No provenance information available")
    else:
        print("\n\t  Last provenance entry ({}):\n\t  '{}' ({})\n".format(
            last_entry["ended_at"],
            last_entry["activity_desc"],
            ", ".join( [prov_slug(x) for x in last_entry["agent"] ] )))
