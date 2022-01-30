# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual.widget import Widget
from textual.reactive import Reactive
from textual._context import active_app
from rich.panel import Panel

from consts.consts import BUILD, VERSION


class Title(Widget):

    actual_hourglass = Reactive(0)
    actual_year = Reactive(0)
    actual_month = Reactive(0)
    actual_day = Reactive(0)
    time_speed = Reactive(1)

    def on_mount(self):
        self.set_interval(1, self.update_info)

    def update_info(self) -> None:
        hourglass = active_app.get().hourglass
        hourglass.step()
        actual_speed = hourglass.speed
        info = hourglass._hourglass_to_dates()
        self.time_speed = actual_speed
        self.actual_year = info[0]
        self.actual_month = info[1]
        self.actual_day = info[2]

    def render(self) -> Panel:
        time_info = [
            f"Year [bold]{self.actual_year}[/bold]",
            f"Month [bold]{self.actual_month}[/bold]",
            f"Day [bold]{self.actual_day}[/bold]",
            f"(x{self.time_speed})" if self.time_speed > 0 else "(:zzz:)",
            ]
        return Panel(
            ":bar_chart: [bold]0[/bold] | :money_bag: [bold]100[/bold]",
            title=f"NerdVille {VERSION}-b{BUILD}",
            subtitle=" ".join(time_info)
            )
