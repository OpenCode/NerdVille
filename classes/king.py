# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual._context import active_app


class King:

    _row = 0
    _col = 0
    _app = None
    _db = None

    def __init__(self):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db
        self._row = int(db.get_game_value("king_position_row"))
        self._col = int(db.get_game_value("king_position_col"))

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._db.set_game_value("king_position_row", value)
        self._row = value

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, value):
        self._db.set_game_value("king_position_col", value)
        self._col = value

    def move_up(self):
        game_map = self._app.get().map
        if game_map.rows_limit >= self.row > 0:
            next_row = self.row - 1
            next_column = self.col
            if game_map.can_move_here(next_row, next_column):
                self.row -= 1
                self._app.get().ville_area.render()

    def move_down(self):
        game_map = self._app.get().map
        if game_map.rows_limit > self.row >= 0:
            next_row = self.row + 1
            next_column = self.col
            if game_map.can_move_here(next_row, next_column):
                self.row += 1
                self._app.get().ville_area.render()

    def move_left(self):
        game_map = self._app.get().map
        if game_map.cols_limit >= self.col > 0:
            next_row = self.row
            next_column = self.col - 1
            if game_map.can_move_here(next_row, next_column):
                self.col -= 1
                self._app.get().ville_area.render()

    def move_right(self):
        game_map = self._app.get().map
        if game_map.cols_limit > self.col >= 0:
            next_row = self.row
            next_column = self.col + 1
            if game_map.can_move_here(next_row, next_column):
                self.col += 1
                self._app.get().ville_area.render()

    def move_to_castle(self):
        castle = self._app.get().castle
        self.row = castle.row
        self.col = castle.col
        self._app.get().ville_area.render()

    def move_to_origin(self):
        self.row = 0
        self.col = 0
        self._app.get().ville_area.render()
