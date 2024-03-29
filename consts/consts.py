# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

VERSION = '0.2.1'
BUILD = 4


COLS_NUMBER = 20
COLS_LIMIT = COLS_NUMBER - 1
ROWS_NUMBER = 20
ROWS_LIMIT = ROWS_NUMBER - 1


CHARACTERS = {
    'king': {
        "name": "King",
        "symbol": "[bold red]W[/bold red]",
        "emoji": ":crown:",
        },
}


RESOURCES = {
    'population': {
        "amount": 2,
        "symbol": ":bar_chart:",
        },
    'free_worker': {
        "amount": 2,
        "symbol": ":construction_worker:",
        },
    'gold': {
        "amount": 100,
        "symbol": ":money_bag:",
        },
    'hay': {
        "amount": 0,
        "symbol": ":corn:",
        },
    'wood': {
        "amount": 0,
        "symbol": ":deciduous_tree:",
        },
    'fish': {
        "amount": 0,
        "symbol": ":fish:",
        },
    'health': {
        "amount": 0,
        "symbol": ":medical_symbol:",
        },
    'happiness': {
        "amount": 0,
        "symbol": ":smiley:",
        },
    'spirituality': {
        "amount": 0,
        "symbol": ":pray:",
        },
}


ENVIRONMENTS = {
    "sea": {
        "name": "Sea",
        "symbol": "[bold blue]~[/bold blue]",
        "block": True,
        "emoji": ":water_wave:",
        },
    "grass": {
        "name": "Free Space",
        "symbol":"[green].[/green]",
        },
    "rock": {
        "name": "Rock",
        "symbol":"[bold grey]*[/bold grey]",
        "block": True,
        },
    "tree": {
        "name": "Tree",
        "symbol":"[green]A[/green]",
        "emoji": ":deciduous_tree:",
        },
}


BUILDINGS = {
    'castle': {
        "name": "Castle",
        "symbol": "[bold]O[/bold]",
        "emoji": ":castle:",
        "production": {"gold": {"population": 2}},
        },
    'house': {
        "name": "House",
        "symbol": "[bold]X[/bold]",
        "emoji": ":house:",
        "cost": {"gold": 10},
        "production_on_build": {"population": 2, "free_worker": 2},
        "consumption": {"fish": 2},
        },
    'hospital': {
        "name": "Hospital",
        "symbol": "[bold]H[/bold]",
        "emoji": ":hospital:",
        "cost": {"gold": 100, "free_worker": 10},
        "production": {"health": 1},
        "recovery_on_demolish": {"free_worker": 10},
        },
    "bridge": {
        "name": "Bridge",
        "symbol": "[bold brown]=[/bold brown]",
        "emoji": ":brown_square:",
        },
    "farm": {
        "name": "Farm",
        "symbol": "[bold yellow]#[/bold yellow]",
        "emoji": ":ear_of_rice:",
        "cost": {"gold": 30, "wood": 100, "free_worker": 5},
        "production": {"hay": 1},
        "recovery_on_demolish": {"free_worker": 5},
        },
    "lumberjack": {
        "name": "Lumberjack",
        "symbol": "[bold green]T[/bold green]",
        "emoji": ":axe:",
        "cost": {"gold": 30, "free_worker": 1},
        "production": {"wood": 1},
        "building_constraints": {"build-on": 'environments-tree'},
        "recovery_on_demolish": {"free_worker": 1},
        },
    "fisherman": {
        "name": "Fisherman",
        "symbol": "[bold blue]F[/bold blue]",
        "emoji": ":fishing_pole:",
        "cost": {"gold": 30, "wood": 5, "free_worker": 1},
        "production": {"fish": 3},
        "building_constraints": {"side-any": 'environments-sea'},
        "recovery_on_demolish": {"free_worker": 1},
        },
    "tavern": {
        "name": "Tavern",
        "symbol": "[bold]U[/bold]",
        "emoji": ":beers:",
        "cost": {"gold": 100, "wood": 200, "free_worker": 3},
        "production": {"happiness": 1},
        "recovery_on_demolish": {"free_worker": 3},
        },
    "church": {
        "name": "Church",
        "symbol": "[bold]+[/bold]",
        "emoji": ":church:",
        "cost": {"gold": 1000, "wood": 2000, "free_worker": 2},
        "production": {"spirituality": 1},
        "recovery_on_demolish": {"free_worker": 2},
        },
}


'''
Elements structure
{
    "name" ->
        [string, mandatory]
        Name to show in the info
    "symbol" ->
        [string, mandatory]
        Symbol show on game map in ASCII mode,
    "emoji" ->
        [string, default EMPTY]
        Emoji code to show on game map in EMOJI mode.
        If empty shows symbol.
        Available code here:
            https://github.com/Textualize/rich/blob/master/rich/_emoji_codes.py
    "cost" ->
        [dict, default None]
        Resources used to build the element.
        F.E. {"gold": 10, "wood": 20}
    "production" ->
        [dict, default None]
        Resources created by the building on every loop.
        It can be an integer to increment a value directly
            F.E. {"wood": 20, "happiness": 1}
        or can be a dict to increment a value based on other resources
            F.E. {"gold": {"population": 2}}
                 -> 2 gold will be created for every population
                 {"gold": {"population": 2, "wood": 1}}
                 -> 2 gold will be created for every population and 1
                    for every wood
    "production_on_build" ->
        [dict, default None]
        Resources created by the building at the build moment.
        F.E. {"gold": 1, "population": 2}
    "consumption" ->
        [dict, default None]
        Resources consumed by the building on every loop.
        It can be an integer to decrement a value directly
            F.E. {"wood": 20, "happiness": 1}
        or can be a dict to decrement a value based on other resources
            F.E. {"gold": {"population": 2}}
                 -> 2 gold will be consumed for every population
                 {"gold": {"population": 2, "wood": 1}}
                 -> 2 gold will be consumed for every population and 1
                    for every wood
    "block" ->
        [boolean, default False]
        If True, characters can't pass through it
    "building_constraints" ->
        [dict, default None]
        Constraints for element building. It can be:
            - side-SIDE:
                the cell in the relative side SIDE
                must be of the indicated type.
                SIDE can be:
                    - up: above cell
                    - down: below cell
                    - left: cell on the left
                    - right: cell on the right
                    - any: any position
                    - all: all the positions
            - build-on:
                the cell must be of the indicated type.
}
'''


ELEMENTS = {
    'characters': CHARACTERS,
    'environments': ENVIRONMENTS,
    'buildings': BUILDINGS,
}
