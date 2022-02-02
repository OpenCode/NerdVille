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
        # Check resources used for the build
        insufficent_resources = []
        for resource_name, cost in element.cost.items():
            resource = Resource().get(resource_name)
            if resource.amount < cost:
                insufficent_resources.append(resource_name)
            else:
                resource.decrement(cost)
        if insufficent_resources:
            self._app.get().log_area.update(
                f"Insufficent resources: {', '.join(insufficent_resources)}")
            return None
        # Check building constraints
        game_map = self._app.get().map
        can_build = True
        for constraint_name, constraint in \
                element.building_constraints.items():
            # Check sides constraints
            if constraint_name.startswith('side-'):
                side = constraint_name.split('-')[1]
                if side in ('all', 'any'):
                    positions = [
                        game_map.position(row-1, col),
                        game_map.position(row+1, col),
                        game_map.position(row, col-1),
                        game_map.position(row, col+1),
                    ]
                    position_elements = [
                        p.element.code == constraint
                        for p in positions
                        if p
                    ]
                    if position_elements and side == 'all':
                        can_build = all(position_elements)
                    elif position_elements and side == 'any':
                        can_build = any(position_elements)
                    else:
                        can_build = False
                else:
                    if side == 'up':
                        position = game_map.position(row-1, col)
                        if position and position.element.code == constraint:
                            can_build = True
                    elif side == 'down':
                        position = game_map.position(row+1, col)
                        if position and position.element.code == constraint:
                            can_build = True
                    elif side == 'left':
                        position = game_map.position(row, col-1)
                        if position and position.element.code == constraint:
                            can_build = True
                    elif side == 'right':
                        position = game_map.position(row, col+1)
                    if position and position.element.code == constraint:
                        can_build = True
        if not can_build:
            self._app.get().log_area.update(f"Constraints not respected")
            return None
        return self._build(row, col, building)

    def build_castle(self):
        castle = self._app.get().castle
        # Bypass every check for the castle
        return self._build(castle.row, castle.col, 'buildings-castle')

    def _build(self, row, col, building):
        # Build with Bob the Builder!
        # https://www.youtube.com/watch?v=l-epqIHe4w0
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
