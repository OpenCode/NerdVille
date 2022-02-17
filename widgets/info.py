# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from rich.panel import Panel
from textual._context import active_app
from textual.reactive import Reactive
from textual.widget import Widget

from classes.element import Element


class Info(Widget):

    value = Reactive('')

    def render(self) -> Panel:
        return Panel(str(self.value))

    def king_position_info(self) -> None:
        king = active_app.get().king
        game_map = active_app.get().map
        position = game_map.position(king.row, king.col)
        building = position.building
        if building:
            values = [
                f"[bold]{building.element.name}[/bold]",
                "",
                ]
        else:
            values = [
                f"[bold]{position.element.name}[/bold]",
                "",
                ]
        if building:
            # Show production
            if building.element.production:
                values.append("[bold]PRODUCTION: [/bold]")
                for production in building.element.production:
                    values.append(
                        f"  {production.title()}: "
                        f"{building.element.production[production]}")
            # Show consumption
            if building.element.consumption:
                values.append("[bold]CONSUMPTION: [/bold]")
                for consumption in building.element.consumption:
                    values.append(
                        f"  {consumption.title()}: "
                        f"{building.element.consumption[consumption]}")
        self.value = "\n".join(values)

    def element_info(self, element):
        element = Element().get(element)
        values = [
            f"[bold]{element.name}[/bold]",
            "",
            ]
        # Show cost
        if element.cost:
            values.append("[bold]COST: [/bold]")
            for cost in element.cost:
                values.append(
                    f"  {cost.title()}: {element.cost[cost]}")
        # Show production
        if element.production:
            values.append("[bold]PRODUCTION: [/bold]")
            for production in element.production:
                values.append(
                    f"  {production.title()}: "
                    f"{element.production[production]}")
        # Show consumption
        if element.consumption:
            values.append("[bold]CONSUMPTION: [/bold]")
            for consumption in element.consumption:
                values.append(
                    f"  {consumption.title()}: "
                    f"{element.consumption[consumption]}")
        self.value = "\n".join(values)
