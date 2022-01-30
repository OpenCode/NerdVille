# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual.widget import Widget
from rich.panel import Panel
from textual.reactive import Reactive
from textual._context import active_app


class Logs(Widget):

    value = Reactive('')

    def update(self, message) -> None:
        title = active_app.get().title_area
        message = \
            f"{str(title.actual_year).rjust(2, '0')}-" \
            f"{str(title.actual_month).rjust(2, '0')}-" \
            f"{str(title.actual_day).rjust(2, '0')} | " \
            f"{message}"
        actual_values = self.value.split('\n')
        new_values = [message, ] + actual_values[0:5]
        self.value = '\n'.join(new_values)

    def render(self) -> Panel:
        return Panel(self.value)
