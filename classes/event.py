# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual._context import active_app


class Event:
    """
        Class that manage the events
    """

    _app = None
    _db = None

    def __init__(self):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db

    def register(self, event_type, value=None) -> int:
        hourglass = self._app.get().hourglass
        hg_values = hourglass.values
        timestamp = hg_values['timestamp']
        year = hg_values['year']
        month = hg_values['month']
        day = hg_values['day']
        self._db.cursor.execute(
            "INSERT INTO event "
            "(timestamp, year, month, day, type, value) "
            "VALUES "
            "(:timestamp, :year, :month, :day, :type, :value)",
            {"timestamp": timestamp, "year": year, "month": month,
             "day": day, "type": event_type, "value": str(value) or ""}
            )
        event_id = self._db.cursor.lastrowid
        self._db.connection.commit()
        return event_id
