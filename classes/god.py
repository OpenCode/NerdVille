# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual._context import active_app

from classes.building import get_all as building_get_all


class God:
    """
        Class that manage the entire simulation
    """

    _app = None
    _db = None

    def __init__(self):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db

    def snap(self):
        """
            Snap is the time that running out.
            Every God's snap something happens.
        """
        buildings = building_get_all()
        for building in buildings:
            building.produce()
