# tulpa

Build visualizations and analysis for a list of video games (with 
their identifiers in various databases). The list can be created with tulpa,
by giving the *build* command a query for a game or a company. These lists can 
also be used in [lemongrab](https://git.sc.uni-leipzig.de/ubl/diggr/general/lemongrab)
to build, visualize and inspect company networks.

![tulpa logo](assets/tulpa_header.png?raw=true "tulpa")

## Requirements

* Python 3.7
* [unified api](https://git.sc.uni-leipzig.de/ubl/diggr/infrastructure/unifiedapi)

## Prerequisites

It is recommended to install *tulpa* in a virtual Python environment such as
Pipenv, virtualenv, or venv.

*tulpa* requires access to the [unified api](https://git.sc.uni-leipzig.de/ubl/diggr/infrastructure/unifiedapi), the correct address needs to be specified in the `settings.py` file. In order to use the games-data-table command, lemongrab needs to be installed in the same virtual environment.

## Installation

Clone the repository.

```zsh
$ git clone https://git.sc.uni-leipzig.de/ubl/diggr/general/tulpa
$ cd tulpa
```

Open *tulpa/settings.py* with an editor of your choice and edit the value
of *DIGGR_API* to the address of your instance of the *UnifiedAPI*. Save the file
and install tulpa.

```zsh
$ pip install .
```

## Initial setup / Create a project

Create a folder and initialize tulpa.

```zsh
$ mkdir testproject && cd testproject
$ tulpa init
```

> Note: lemongrab can be initialized alongside in the same directory!

This will create various directories. You are now ready to build or import a gamelist. 

## Start / Build a gamelist

The base dataset tulpa uses is a gamelist. A gamelist can be created from 
withing tulpa in two ways, either by fetching matching entries (query or company)
from mobygames and build a dataset therefrom, or by random sampling mobygames.
It is mandatory to create a gamliest in order to be able to build the other 
datasets and visualizations.

### Build Gamelist

```zsh
$ tulpa gamelist build -q "final fantasy"
```
> Note: It is mandatory to supply this command with either the -c or the -q option. 

Options:

* `-q`  Include all games with this term in the title
* `-c` Include all games where this company was part of the production

### Sample Gamelist

The second option is to create a gamelist, by ranomly sampling mobygames. Just give
a sample size. The following command will create a sample with 100 entries. 

```zsh
$ tulpa gamelist sample 100
```

### Gamelist File

The resulting yaml file has a name and links for each game entry. The following
metadata ressources are used:
* Mobygames: List of slugs (e.g. `dark-souls`)
* GameFAQs: List of slugs (e.g. `ps3/606312-dark-souls`)
* Media Art DB: List of IDs (GPIr, e.g.`0392133400819`)

The resulting file might look like this (obviously for a search related to *Zelda*):

```yaml
The Legend of Zelda:
  gamefaqs:
  - nes/563433-the-legend-of-zelda
  mediaartdb:
  - '392100100105'
  - '392134100837'
  - '392144600139'
  mobygames:
  - legend-of-zelda
```


## Dataset Creation

This chapter is a short introduction into the arguments, configuration files
and possible use cases for tulpa.

### Build a games dataset

The previously generated yaml file can now be converted into a json file using
the following command. 

```zsh
$ tulpa dataset games
```

> Note: This command command also fetches the internal mobygames id for each
mobygames slug and stores it into the json file.

The result might look like so:

```json
{
    "Dark Souls": {
        "mobygames": [
            "dark-souls-limited-edition",
            "dark-souls"
        ],
        "mediaartdb": [
            "392133400819"
        ],
        "gamefaqs": [
            "ps3/606312-dark-souls",
            "xbox360/608635-dark-souls"
        ]
    }
}
```

The games dataset will be stored in the `datasets/games` directory and uses the 
following filename template: `<project_name>_games.json`.

With this games dataset you can now create the other datasets and visualizations.

### Build a releases dataset

```zsh
$ tulpa dataset releases
```

Generates a dataset containing the releases of the games dataset in various regions 
(based on GameFAQs data).

### Build a companies dataset

To generate all available company information from previously generated yaml file for each game use the following command.

```zsh
$ tulpa dataset companies
```

Result might look like:

```
{
    "Ace Combat 04: Shattered Skies": [
        {
            "company_id": 1043,
            "company_name": "Namco Limited",
            "role": "Published by",
            "release_countries": [
                "Japan"
            ],
            "platform": "Sony PlayStation 2"
        },
        {
            "company_id": 1043,
            "company_name": "Namco Limited",
            "role": "Developed by",
            "release_countries": [
                "Japan"
            ],
            "platform": "Sony PlayStation 2"
        }
    ]
}
```

### Draw a sample dataset

This feature draws a random sample of variable size from the gamelist.
A uniformly random sample from all games in the gamelist file is created.
The random.choices() function of python is used to draw the uniformly 
random samples of size SIZE. With either option all entries in the gamelist
have the same probability to appear in the sample.

```zsh
$ tulpa dataset sample 100
```

will draw a random sample with 100 entries from the gamelist.

### Show all datasets

To show all generated datsets inside the project folder use:

```zsh
$ tulpa datasets
```

You will get the location, name, date and time of the generated datasets.


## Visualizations

With the datasets created, you can now build visualizations.

### Staff Heatmap

A heatmap that visualizes which staff member worked on what game. It chooses the 
n most active (worked on the highest number of games) staff members. The color 
indicates the number of roles the person held during the game's production. 
The heatmap will be saved either as a png image or a pdf file.

```zsh
$ tulpa vis staff-heatmap
```

Options:

* `-o`  Output format, either `pdf` or `png`
* `-n`  Number of persons considered in the visualizations

### Staff Size Development

```zsh
$ tulpa vis staff-size
```

### Credits Network

A network graph showing how mucht the development staff of the games overlap. 
The command generates a `graphml` file which can be loaded into Gephi.
The similarity between two games is calculated by: 
|union(GameA, GameB)| / min(|GameA|, |GameB|)

```zsh
$ tulpa vis credits-network
```

### Release Timeline

Builds an interactive Timeline showing the games' releases in the various regions. 
The temporal distance between the releases is represented by the colored area 
between the releases. The visualization will be saved as a html file.

```zsh
$ tulpa vis release-timeline
```

### Games Data Table

Build a csv table with game metadata:
* Title
* Platform
* Number of companies
* Companies per country

```zsh
$ tulpa vis games-data-table
```

## Copyright
- 2019-2020, Universitätsbibliothek Leipzig <info@ub.uni-leipzig.de>

## Authors
- P. Mühleder <muehleder@saw-leipzig.de>
- F. Rämisch <raemisch@ub.uni-leipzig.de>

## Licence
- GNU General Public License v3 (Software)
