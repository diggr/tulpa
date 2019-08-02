import json
from ..config import get_config
from ..utils import print_last_prov_entry


def check_games_dataset():
    
    cf = get_config()
    dataset_file = cf.datasets["games"]

    print("\nFile location: {}\n".format(dataset_file))

    with open(dataset_file) as f:
        ds = json.load(f)

    print("Number of games: {}".format(len(ds)))

    no_ids = {
        "gamefaqs": [],
        "mediaartdb": [],
        "mobygames":  []
    }

    for game_title, links in ds.items():

        if "mobygames" not in links:
            no_ids["mobygames"].append(game_title)
        else:
            if len(links["mobygames"]) == 0:
                no_ids["mobygames"].append(game_title)

        if "mediaartdb" not in links:
            no_ids["mediaartdb"].append(game_title)
        else:
            if len(links["mediaartdb"]) == 0:
                no_ids["mediaartdb"].append(game_title)

        if "gamefaqs" not in links:
            no_ids["gamefaqs"].append(game_title)
        else:
            if len(links["gamefaqs"]) == 0:
                no_ids["gamefaqs"].append(game_title)                                
        
    
    print("\t ... without Media Art DB entry: {}".format(len(no_ids["mediaartdb"])))
    for title in no_ids["mediaartdb"]:
        print("\t\t - {}".format(title))
    print("\t ... without Mobygames entry: {}".format(len(no_ids["mobygames"])))
    for title in no_ids["mobygames"]:
        print("\t\t - {}".format(title))        
    print("\t ... without GameFAQs entry: {}".format(len(no_ids["gamefaqs"])))
    for title in no_ids["gamefaqs"]:
        print("\t\t - {}".format(title))        


    print_last_prov_entry(dataset_file)