# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import csv
from collections import namedtuple
from random import choice

from textual._context import active_app

from classes.element import Element
from classes.building import Building


class Map:

    rows_number = 0
    cols_number = 0
    rows_limit = 0
    cols_limit = 0
    _app = None
    _db = None

    def __init__(self):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db
        self.rows_number = int(db.get_game_value("map_rows"))
        self.rows_limit = self.rows_number - 1
        self.cols_number = int(db.get_game_value("map_cols"))
        self.cols_limit = self.cols_number - 1
        # If is a new database (position is empty), create a new map
        self._db.cursor.execute("select count(*) from position")
        positions = self._db.cursor.fetchone()
        if positions[0] == 0:
            self.generate_map()

    def generate_map(self):
        self._db.cursor.execute("DELETE FROM building;")
        self._db.cursor.execute("DELETE FROM position;")
        # TODO: Move maps in the hidden application folder
        # and use coiche on random result of the folder content
        # so user can add personal maps, too
        maps = ("river", "sea")
        with open(f"maps/{choice(maps)}.csv", newline="") as map_csv:
            map_reader = csv.reader(map_csv, delimiter=',', quotechar='"')
            for row_number, row in enumerate(map_reader):
                if row_number == 0:
                    map_version = row[0].split(":")[1]
                    rows = row[1].split(":")[1]
                    cols = row[2].split(":")[1]
                    castle_row = row[3].split(":")[1]
                    castle_col = row[4].split(":")[1]
                else:
                    for col_number, col in enumerate(row):
                        self._db.cursor.execute(
                            f"INSERT INTO position "
                            f"(row, col, type)"
                            f" VALUES "
                            f" ({row_number-1}, {col_number}, '{col}') "
                            )
            self._db.set_game_value("map_rows", rows)
            self._db.set_game_value("map_cols", cols)
            self._db.set_game_value("castle_position_row", castle_row)
            self._db.set_game_value("castle_position_col", castle_col)
            # Auto-build the castle
            castle = self._app.get().castle
            self.build(castle.row, castle.col, "buildings-castle")
            self._db.connection.commit()

    def can_move_here(self, row, col):
        """
            Return True if a charater can move here as next move
        """
        can_move = True
        position_content = self.position(row, col)
        element = position_content.element
        if element.block:
            can_move = False
        return can_move

    def position(self, row=None, col=None):
        if row is None:
            row = self._app.get().king.row
        if col is None:
            col = self._app.get().king.col
        self._db.cursor.execute(
            "SELECT type, building_id FROM position "
            "WHERE row = :row AND col = :col",
            {'row': row, 'col': col, }
            )
        record = self._db.cursor.fetchone()
        if not record:
            return None
        if record["building_id"]:
            building = Building().get(record["building_id"])
        else:
            building = None
        if building:
            element = building.element
        else:
            element = Element().get(record["type"])
        Position = namedtuple('Position', ['type', 'building', 'element'])
        position_object = Position(
            record["type"], building, element
        )
        return position_object

    def build(self, row=None, col=None, building=''):
        if not row:
            row = self._app.get().king.row
        if not col:
            col = self._app.get().king.col
        position_info = self.position(row, col)
        response = {'type': 'None', 'id': None}
        if not position_info.building:
            building = Building().build(building, row, col)
            if building:
                response['type'] = 'new_building'
                response['id'] = building.id
        else:
            response['type'] = 'occupied_land'
        return response

    def demolish(self, row=None, col=None):
        if not row:
            row = self._app.get().king.row
        if not col:
            col = self._app.get().king.col
        castle = self._app.get().castle
        if row == castle.row and col == castle.col:
            response = 'impossible_castle'
            return response
        position_info = self.position(row, col)
        response = 'None'
        if position_info.building:
            self._db.cursor.execute(
                "DELETE FROM building WHERE id = :id",
                {'id': position_info.building.id}
                )
            response = 'ok'
        else:
            response = 'nothing_to_demolish'
        return response
