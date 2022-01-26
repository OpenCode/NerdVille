# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual._context import active_app


class Castle:

    _row = 0
    _col = 0
    _app = None
    _db = None

    def __init__(self):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db
        self._row = int(db.get_game_value("castle_position_row"))
        self._col = int(db.get_game_value("castle_position_col"))

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._db.set_game_value("castle_position_row", value)
        self._row = value

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, value):
        self._db.set_game_value("castle_position_col", value)
        self._col = value
