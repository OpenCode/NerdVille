# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual._context import active_app


class Element:

    code = ''
    category = ''
    name = ''
    symbol = ''
    block = False
    _app = None
    _db = None

    def __init__(self, code):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db
        self.code = code
        data = self.get_data()
        self.category = data["category"]
        self.name = data["name"]
        if self._db.get_game_value("element_style") == 'EMOJI':
            self.symbol = data["emoji"] or data["symbol"]
        else:
            self.symbol = data["symbol"]
        self.block = bool(data['block'])

    def get_data(self):
        self._db.cursor.execute(
            "SELECT * FROM element "
            "WHERE code = :code",
            {'code': self.code, }
            )
        return self._db.cursor.fetchone()
