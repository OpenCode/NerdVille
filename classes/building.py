# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual._context import active_app

from classes.element import Element
from classes.resource import Resource


class Building:

    id = None
    row = 0
    col = 0
    level = 0
    element = None
    _building = ''
    _app = None
    _db = None

    def __init__(self):
        app = active_app
        db = app.get().db
        self._app = app
        self._db = db

    def get(self, building_id):
        self.id = building_id
        data = self.get_data()
        self.row = data["row"]
        self.col = data["col"]
        self.level = data["level"]
        self._building = data['building']
        self.element = Element().get(self._building)
        return self

    def get_data(self):
        self._db.cursor.execute(
            "SELECT * FROM building "
            "WHERE id = :id",
            {'id': self.id, }
            )
        return self._db.cursor.fetchone()

    def get_all(self):
        self._db.cursor.execute("SELECT id FROM building WHERE id > 0")
        buildings = []
        records = self._db.cursor.fetchall()
        for record in records:
            buildings.append(Building().get(record['id']))
        return buildings

    def build(self, building, row, col):
        element = Element().get(building)
        insufficent_resources = []
        for resource_name, cost in  element.cost.items():
            resource = Resource().get(resource_name)
            if resource.amount < cost:
                insufficent_resources.append(resource_name)
            else:
                resource.decrement(cost)
        if insufficent_resources:
            self._app.get().log_area.update(
                f"Insufficent resources: {', '.join(insufficent_resources)}")
            return None
        self._db.cursor.execute(
            "INSERT OR REPLACE INTO building "
            "(row, col, building) "
            "VALUES "
            "(:row, :col, :building)",
            {"row": row, "col": col, "building": building}
            )
        building_id = self._db.cursor.lastrowid
        self._db.cursor.execute(
            "UPDATE position SET building_id = :last_id WHERE "
            "row = :row AND col = :col",
            {'last_id': building_id,
            'row': row,
            'col': col,
            }
        )
        self._db.connection.commit()
        return self.get(building_id)

    def produce(self):
        if self.element.production:
            for resource_name in self.element.production.keys():
                resource = Resource().get(resource_name)
                resource.increment(self.element.production[resource_name])
