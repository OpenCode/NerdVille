# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from random import randint


VERSION = '0.1.0+1'


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
}


BUILDINGS = {
    'castle': {
        "name": "Castle",
        "symbol": "[bold]O[/bold]",
        "emoji": ":castle:",
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
        },
    "lumberjack": {
        "name": "Lumberjack",
        "symbol": "[bold green]T[/bold green]",
        "emoji": ":deciduous_tree:",
        },
    "tavern": {
        "name": "Tavern",
        "symbol": "[bold]U[/bold]",
        "emoji": ":beers:",
        },
    "church": {
        "name": "Church",
        "symbol": "[bold]+[/bold]",
        "emoji": ":church:",
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
        [integer, deefault 0]
        Gold used to build the element,
    "block" ->
        [boolean, default False]
        If True, characters can't pass through it
}
'''


ELEMENTS = {
    'characters': CHARACTERS,
    'environments': ENVIRONMENTS,
    'buildings': BUILDINGS,
}
