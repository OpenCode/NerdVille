# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from json import dumps, loads
import sqlite3
from os.path import join

from consts.consts import \
    VERSION, BUILD, \
    ELEMENTS, RESOURCES


class Db:

    path = ''
    name = 'nerdville.db'
    connection = None
    cursor = None

    def _convert_in_boolean(self, value):
        if value:
            return 1
        else:
            return 0

    def _from_dict_to_database(self, value):
        if not value:
            return ""
        else:
            return dumps(value)

    def _from_database_to_dict(self, value):
        if not value:
            return {}
        else:
            return loads(value)

    # Game values

    def get_game_value(self, key):
        self.cursor.execute(
            f'SELECT "value" FROM "game" WHERE key = "{key}"; ')
        value = self.cursor.fetchone()["value"]
        return value

    def init_game_value(self, key, value):
        self.cursor.execute(
            f"INSERT OR IGNORE INTO game (key, value) VALUES "
            f"('{key}', '{value}')")
        self.connection.commit()

    def set_game_value(self, key, value):
        self.cursor.execute(
            f"INSERT OR REPLACE INTO game (key, value) VALUES "
            f"('{key}', '{value}')")
        self.connection.commit()

    def __init__(self, path, name='nerdville.db'):
        self.path = path
        self.name = name
        self.connection = sqlite3.connect(join(self.path, self.name))
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        # SQLite has foreign key triggers turned off by default
        self.cursor.execute(
            "PRAGMA foreign_keys = ON"
        )
        # Create tables if don't exist
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS "
            "building ("
            "id INTEGER PRIMARY KEY , "
            "row INTEGER, "
            "col INTEGER, "
            "level INTEGER DEFAULT 0, "
            "building TEXT, "
            "UNIQUE(row, col)"
            ") "
            )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS "
            "position ("
            "row INTEGER, "
            "col INTEGER, "
            "type TEXT, "
            "building_id INTEGER, "
            "FOREIGN KEY(building_id) REFERENCES building(id) "
            "ON DELETE SET NULL "
            "UNIQUE(row, col)"
            ") "
            )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS "
            "game "
            "(key TEXT NOT NULL UNIQUE, value TEXT)"
            )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS "
            "element ("
            "code TEXT NOT NULL UNIQUE, "
            "category TEXT NOT NULL, "
            "name TEXT NOT NULL UNIQUE, "
            "cost TEXT, "
            "production TEXT, "
            "production_on_build TEXT, "
            "building_constraints TEXT, "
            "consumption TEXT, "
            "recovery_on_demolish TEXT, "
            "block INTEGER, "
            "symbol TEXT NOT NULL UNIQUE, "
            "emoji TEXT"
            ")"
            )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS "
            "resource ("
            "resource TEXT NOT NULL UNIQUE, "
            "amount INTEGER, "
            "symbol TEXT NOT NULL UNIQUE"
            ")"
            )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS "
            "event ("
            "id INTEGER PRIMARY KEY , "
            "timestamp INTEGER, "
            "year INTEGER, "
            "month INTEGER, "
            "day INTEGER, "
            "type TEXT, "
            "value TEXT "
            ")"
            )
        # Set Version information
        self.set_game_value("version", VERSION)
        self.set_game_value("build", BUILD)
        # Define the map dimension
        self.init_game_value("map_rows", 0)
        self.init_game_value("map_cols", 0)
        # Define start position for the king
        self.init_game_value("king_position_row", "0")
        self.init_game_value("king_position_col", "0")
        # Define start position for the the castle
        self.init_game_value("castle_position_row", 0)
        self.init_game_value("castle_position_col", 0)
        # Create the time counter
        self.init_game_value("hourglass_value", "1")
        self.init_game_value("hourglass_speed", "1")
        self.init_game_value("hourglass_frequency", "60") # In seconds
        # Create graph configurations
        self.init_game_value("element_style", "ASCII")
        # Create resources counter
        for resource_name in RESOURCES:
            resource = RESOURCES[resource_name]
            self.cursor.execute(
                "INSERT OR IGNORE INTO resource ("
                "resource, amount, symbol"
                ") VALUES ("
                f"'{resource_name}', "
                f"{resource['amount']}, "
                f"'{resource['symbol']}' "
                ")")
        # Create the buildings models data
        for element_type in ELEMENTS:
            elements = ELEMENTS[element_type]
            for element_name in elements:
                element = elements[element_name]
                cost = self._from_dict_to_database(
                    element.get('cost'))
                production = self._from_dict_to_database(
                    element.get('production'))
                production_on_build = self._from_dict_to_database(
                    element.get('production_on_build'))
                building_constraints = self._from_dict_to_database(
                    element.get('building_constraints'))
                consumption = self._from_dict_to_database(
                    element.get('consumption'))
                recovery_on_demolish = self._from_dict_to_database(
                    element.get('recovery_on_demolish'))
                self.cursor.execute(
                    "INSERT OR IGNORE INTO element ("
                    "code, category, name, "
                    "cost, "
                    "production, production_on_build, "
                    "building_constraints, "
                    "consumption, "
                    "recovery_on_demolish, "
                    "symbol, emoji, block"
                    ") VALUES ("
                    f"'{element_type}-{element_name}', "
                    f"'{element_type}', "
                    f"'{element['name']}', "
                    f"'{cost}', "
                    f"'{production}', "
                    f"'{production_on_build}', "
                    f"'{building_constraints}', "
                    f"'{consumption}', "
                    f"'{recovery_on_demolish}', "
                    f"'{element['symbol']}', "
                    f"'{element.get('emoji', '')}', "
                    f"{self._convert_in_boolean(element.get('block', False))}"
                    ")")
        self.connection.commit()
