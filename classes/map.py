# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from collections import namedtuple

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
        # Create the map
        for i in range(self.rows_number):
            cell_content = 'environments-grass'
            for j in range(self.cols_number):
                if i in (10, 11, 12):
                    if j in (3, 4):
                        cell_content = 'buildings-bridge'
                    else:
                        cell_content = 'environments-sea'
                else:
                    cell_content = 'environments-grass'
                self._db.cursor.execute(
                    f"INSERT INTO position "
                    f"(row, col, type)"
                    f" VALUES "
                    f" ({i}, {j}, '{cell_content}') "
                    )
        # Auto-build the castle
        castle = self._app.get().castle
        self.build(castle.row, castle.col, 'buildings-castle')
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
