# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual._context import active_app

from classes.element import Element


class Building:

    id = 0
    row = 0
    col = 0
    level = 0
    element = None
    _building = ''
    _app = None
    _db = None

    def __init__(self, building_id):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db
        self.id = building_id
        data = self.get_data()
        self.row = data["row"]
        self.col = data["col"]
        self.level = data["level"]
        self._building = data['building']
        self.element = Element(self._building)

    def get_data(self):
        self._db.cursor.execute(
            "SELECT * FROM building "
            "WHERE id = :id",
            {'id': self.id, }
            )
        return self._db.cursor.fetchone()
