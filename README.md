# TULPA

Build visualizations and analysis for a list of video games (with 
their identifiers in various databases). The list can be created with tulpa,
by giving the *build* command a query for a game or a company. These lists can 
also be used in [lemongrab](https://git.sc.uni-leipzig.de/ubl/diggr/general/lemongrab)
to build, visualize and inspect company networks.

## Requirements

* Python 3.7
* [unified api](https://git.sc.uni-leipzig.de/ubl/diggr/infrastructure/unifiedapi)

## Setup

Clone repository and install the package.

```zsh
$ git clone https://git.sc.uni-leipzig.de/ubl/diggr/general/tulpa
$ pip install ./tulpa
```

## Dataset Creation

This chapter is a short introduction into the arguments, configuration files
and possible use cases for tulpa.

### Project directory

*tulpa* requires project directory to run on. If you don't have one, create 
a new directory on your filesystem and run the `init` command from within.

```zsh
$ mkdir new_project
$ cd new_project && tulpa init
```

This command generates a `config.yml` file as well as the directories for the 
datasets and visualizations. Feel free to customize the `config.yml` to your
needs.

### Configuration file  `config.yml`

*tulpa* requires access to the [unified api](https://git.sc.uni-leipzig.de/ubl/diggr/infrastructure/unifiedapi),
the correct address needs to be specified in the `config.yml` along with the 
project name.
In order to use the games-data-table command, the path to your lemongrab directory is needed.

```yaml
daft: 'http://127.0.0.1:6660'
project_name: FromSoftware
lemongrab_dir: ''
```

### Build a gamelist

The following command creates a yaml file contianing all games in the project. 
It is mandatory to create this list first in order to be able to build the other 
datasets and visualizations.

```zsh
$ tulpa gamelist build -q "final fantasy"
```
> Note: It is mandatory to supply this command with either the -c or the -q option. 

Options:

* `-q`  Include all games with this term in the title
* `-c` Include all games where this company was part of the production

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

### Build release dataset

```zsh
$ tulpa dataset releases
```

Generates a dataset containing the releases of the games dataset in various regions 
(based on GameFAQs data).

### Build a company dataset

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

### Show all datasets

To show all generated datsets inside the project folder use:

```zsh
$ tulpa datasets
```

You will get the location, name, date and time of the generated datasets.

### Draw a sample

Tulpa has a feature to draw a random sample of variable size with respect
to different datasets. The first option is (starting from da blank project)
to draw a random sample from mobygames. This will create a gamelist file
containing as many games as you would like. 

The second option is, to sample an already existing gamelist file. This 
option will also draw a uniformly random sample from all games in the 
gamelist file. 

Both functions use the random.choices() function of python to draw the
uniformly random samples of size SIZE. With either option all entries (
either every mobygames ID or every game in the gamelist) has the same 
probability to appear in the sample.


The command 

```zsh
$ tulpa sample draw 100
```

will draw a random sample with 100 entries from all mobygames IDs and create 
a gamelist. Whereas 

```zsh
$ tulpa sample draw-from-gamelist 100
```

uses the projects existing gamelist to draw a random sample of 100 entries from.

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
- 2019, Universitätsbibliothek Leipzig <info@ub.uni-leipzig.de>

## Authors
- P. Mühleder <muehleder@ub.uni-leipzig.de>
- F. Rämisch <raemisch@ub.uni-leipzig.de>

## Licence
- GNU General Public License v3 (Software)
