# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import datetime

from textual._context import active_app


# It's equal to 24 hours * 60 minutes * 60 seconds = 1 day
HOURGLASS_STEP = 24*60*60


class Hourglass:

    _value = 0
    _speed = 1
    _app = None
    _db = None

    def __init__(self):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db
        self._value = int(db.get_game_value("hourglass_value"))
        self._speed = int(db.get_game_value("hourglass_speed"))

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._db.set_game_value("hourglass_value", value)
        self._value = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if 5 >= value >= 0:
            self._db.set_game_value("hourglass_speed", value)
            self._speed = value

    def step(self):
        self.value += HOURGLASS_STEP * self.speed
        self._app.get().god.snap()

    def _hourglass_to_dates(self):
        '''
            Convert HourGlass in Year, Month, Day
        '''
        actual_dt = datetime.fromtimestamp(self.value)
        return (actual_dt.year - 1970, actual_dt.month, actual_dt.day)
