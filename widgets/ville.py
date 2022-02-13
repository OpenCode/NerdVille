# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from textual.widget import Widget
from rich.table import Table
from rich.console import RenderableType
from textual.reactive import Reactive
from textual._context import active_app

from classes.element import Element


class VilleArea(Widget):

    # Actual King position
    # king_position = [
    #   ROW (from 0 to MAP_ROW_LIMIT),
    #   COL (from 0 to MAP_COL_LIMIT),
    #   ]
    king_position = Reactive([0, 0])
    element_style = Reactive("ASCII")

    def render(self) -> RenderableType:
        self.table = Table(
            show_header=False,
            show_footer=False,
            show_lines=False,
            box=None,
            )
        db = active_app.get().db
        king = active_app.get().king
        game_map = active_app.get().map
        self.king_position = [king.row, king.col]
        # Render table
        db.cursor.execute('SELECT "row" FROM "position" p GROUP BY "row"; ')
        rows = db.cursor.fetchall()
        for row_info in rows:
            row = row_info["row"]
            db.cursor.execute(
                'SELECT "col", "type" FROM "position" p '
                'WHERE "row" = :row ORDER BY "col";',
                {"row": row, })
            records = db.cursor.fetchall()
            row_content = []
            for element in records:
                col = element["col"]
                if king.row == row and king.col == col:
                    cell_content = Element().get('characters-king').symbol
                else:
                    position = game_map.position(row, col)
                    cell_content = position.element.symbol
                row_content.append(cell_content)
            self.table.add_row(*row_content)
        return self.table
