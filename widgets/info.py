# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from rich.panel import Panel
from textual._context import active_app
from textual.reactive import Reactive
from textual.widget import Widget


class Info(Widget):

    value = Reactive('')

    def render(self) -> Panel:
        return Panel(str(self.value))

    def update(self) -> None:
        king = active_app.get().king
        game_map = active_app.get().map
        position = game_map.position(king.row, king.col)
        element = position.element
        values = [
            f"[bold]{element.name}[/bold]",
            "",
            ]
        building = position.building
        building_values = []
        if building:
            building_values = [
                f"[bold]LEVEL: [/bold]{building.level}",
            ]
            # Show building cost
            if building.element.cost:
                building_values.append("[bold]COST: [/bold]")
                for cost in building.element.cost:
                    building_values.append(
                        f"  {cost.title()}: {building.element.cost[cost]}")
            # Show building production
            if building.element.production:
                building_values.append("[bold]PRODUCTION: [/bold]")
                for production in building.element.production:
                    building_values.append(
                        f"  {production.title()}: "
                        f"{building.element.production[production]}")
            # Show building consumption
            if building.element.consumption:
                building_values.append("[bold]CONSUMPTION: [/bold]")
                for consumption in building.element.consumption:
                    building_values.append(
                        f"  {consumption.title()}: "
                        f"{building.element.consumption[consumption]}")
            # Show building constraints
            if building.element.building_constraints:
                building_values.append("[bold]BUILDING CONSTRAITS: [/bold]")
                for constrain in building.element.building_constraints:
                    constraint_data = constrain.split('-')
                    contraint_val = \
                        building.element.building_constraints[constrain]
                    building_values.append(
                        f"  {constraint_data[0].title()} "
                        f"{constraint_data[1].title()}: "
                        f"{contraint_val.split('-')[1].title()}")
        self.value = "\n".join(values + building_values)
