# TULPA

Build research datasets and visualizations with videogame metadata. 

## Requirements

* Python 3.7
* unified videogame metadata api (https://git.sc.uni-leipzig.de/ubl/diggr/infrastructure/unifiedapi)

## Setup

1. Clone repository

2. Install with pip (in a new python environment)

```zsh
$ pip install .
```

## Usage

1. Create a new project directory

2. In the project directory initialize project

```zsh
$ tulpa init
```

This command generates a `config.yml` file as well as the directories for the datasets and visualizations.

3. Config `config.yml`

```yaml
daft: 'http://127.0.0.1:6660'
project_name: FromSoftware
```

Enter the daft/unified api url and choose a project name.

4. Build a games dataset

This datasets contains all games in the project. It is mandatory to create a games dataset first in order to be able to build the other datasets and visualizaitons!

Each game entry has a name and links to the following metadata ressources:
* Mobygames: List of slugs (e.g. `dark-souls`)
* GameFAQs: List of slugs (e.g. `ps3/606312-dark-souls`)
* Media Art DB: List of IDs (GPIr, e.g.`0392133400819`)

Example:

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

The games dataset needs to be located in the `datasets/games` directory and use the following filename template:
`<project_name>_games.json`.

With the games dataset you can now create the other datasets and visualizations.

You can check if the dataset is in the correct format using the following command:

```zsh
$ tulpa check games
```

4. Build release dataset

```zsh
$ tulpa build dataset releases
```

Generates a dataset containing the releases of the games in various regions (based on GameFAQs data).

5. Build visualizations

With the datasets created, you can now build visualizations.

5.1 Staff Heatmap

A heatmap that visualizes which staff member worked on what game. It chooses the n most active (worked on the highest number of games) staff members.
The color indicates the number of roles the person held during the game's production. The heatmap will be saved either as a png or a pdf file.

```zsh
$ tulpa build vis staff_heatmap
```

Options:

* `-o`  Output format, either `pdf` or `png`
* `-n`  Number of persons considered in the visualizations

5.2 Credits Network

A network graph showing how mucht the development staff of the games overlap. The command generates a `graphml` file which can be loaded into Gephi.
The similarity between two games is calculated by: |union(GameA, GameB)| / min(|GameA|, |GameB|)

```zsh
$ tulpa build vis credits_network
```

5.3 Release Timeline

Builds an interactive Timeline showing the games' releases in the various regions. The temporal distance between the releases is represented by the colored area between the releases. The visualization will be saved as a html file.

```zsh
$ tulpa build vis release_timeline
```

## Copyright
- 2019, Universitätsbibliothek Leipzig <info@ub.uni-leipzig.de>

## Authors
- P. Mühleder <muehleder@ub.uni-leipzig.de>
- F. Rämisch <raemisch@ub.uni-leipzig.de>

## Licence
- GNU General Public License v3 (Software)