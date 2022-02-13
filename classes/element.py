# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual._context import active_app


class Element:

    code = None
    category = None
    name = None
    symbol = None
    block = None
    cost = None
    production = None
    production_on_build = None
    building_constraints = None
    _app = None
    _db = None

    def __init__(self):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db

    def get(self, code):
        self.code = code
        data = self.get_data()
        self.category = data["category"]
        self.name = data["name"]
        if self._db.get_game_value("element_style") == 'EMOJI':
            self.symbol = data["emoji"] or data["symbol"]
        else:
            self.symbol = data["symbol"]
        self.block = data['block']
        self.cost = data['cost']
        self.production = data['production']
        self.production_on_build = data['production_on_build']
        self.building_constraints = data['building_constraints']
        return self

    def _get_raw_data(self):
        self._db.cursor.execute(
            "SELECT * FROM element "
            "WHERE code = :code",
            {'code': self.code, }
            )
        return self._db.cursor.fetchone()

    def get_data(self):
        raw_data = self._get_raw_data()
        structured_data = {}
        for data in raw_data.keys():
            if data in ('block'):
                structured_data[data] = bool(raw_data[data])
            elif data in ('cost',
                          'production', 'production_on_build',
                          'building_constraints'):
                structured_data[data] = self._db._from_database_to_dict(
                    raw_data[data])
            else:
                structured_data[data] = raw_data[data]
        return structured_data
