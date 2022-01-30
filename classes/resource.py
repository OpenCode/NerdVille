# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual._context import active_app

from consts.consts import RESOURCES


def get_all():
    resources = {}
    for resource in RESOURCES.keys():
        resources[resource] = Resource(resource)
    return resources


class Resource:

    resource = ''
    symbol = ''
    _amount = 0
    _app = None
    _db = None

    def __init__(self, resource):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db
        self.resource = resource
        data = self.get_data()
        self.symbol = data['symbol']
        self._amount = data['amount']

    def get_data(self):
        self._db.cursor.execute(
            "SELECT * FROM resource "
            "WHERE resource = :resource",
            {'resource': self.resource, }
            )
        return self._db.cursor.fetchone()

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
