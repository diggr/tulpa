from provit import Provenance

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