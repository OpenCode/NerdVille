# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual._context import active_app

from consts.consts import RESOURCES


class Resource:

    resource = None
    symbol = None
    _amount = None
    _app = None
    _db = None

    def __init__(self):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db

    def get(self, resource):
        self.resource = resource
        data = self.get_data()
        self.symbol = data['symbol']
        self._amount = data['amount']
        return self

    def get_data(self):
        self._db.cursor.execute(
            "SELECT * FROM resource "
            "WHERE resource = :resource",
            {'resource': self.resource, }
            )
        return self._db.cursor.fetchone()

    @staticmethod
    def get_all():
        resources = {}
        for resource in RESOURCES.keys():
            resources[resource] = Resource().get(resource)
        return resources

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._db.cursor.execute(
            "UPDATE resource SET amount = :amount WHERE "
            "resource = :resource",
            {'amount': value,
            'resource': self.resource,
            }
        )
        self._db.connection.commit()
        self._amount = value

    def increment(self, amount):
        actual_amount = self.amount
        self.amount = actual_amount + amount

    def decrement(self, amount):
        actual_amount = self.amount
        self.amount = actual_amount - amount
