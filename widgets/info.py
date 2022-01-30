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
            if building.element.cost:
                building_values.append("[bold]COST: [/bold]")
                for cost in building.element.cost:
                    building_values.append(
                        f"  {cost.title()}: {building.element.cost[cost]}")
            if building.element.production:
                building_values.append("[bold]PRODUCTION: [/bold]")
                for production in building.element.production:
                    building_values.append(
                        f"  {production.title()}: "
                        f"{building.element.production[production]}")
        self.value = "\n".join(values + building_values)
