# Copyright 2022-TODAY Francesco Apruzzese <cescoap@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from os import makedirs
from os.path import join, expanduser, exists
import click

from rich._emoji_codes import EMOJI
from rich.panel import Panel

from textual import events
from textual.app import App
from textual.widgets import ScrollView, TreeControl, TreeClick
from textual.widgets import Button, ButtonPressed
from textual.keys import Keys

from widgets.info import Info
from widgets.title import Title
from widgets.ville import VilleArea
from widgets.log import Logs

from classes.db import Db
from classes.map import Map
from classes.king import King
from classes.castle import Castle
from classes.hourglass import Hourglass
from classes.event import Event
from classes.god import God
from classes.resource import Resource
from classes.building import Building

from consts.consts import BUILD, VERSION


class NerdVille(App):

    def __init__(self, *args, dev_mode, **kwargs):
        self.dev_mode = dev_mode
        self.pending_event = None
        super().__init__(*args, **kwargs)

    async def on_load(self, event: events.Load) -> None:
        # Game Shortcuts
        await self.bind(Keys.ControlQ, "quit", "Quit")
        await self.bind(Keys.PageUp, "time_speed_up", "Time Speed Up")
        await self.bind(Keys.PageDown, "time_speed_down", "Time Speed Down")
        await self.bind("p", "pause", "Pause")
        await self.bind(Keys.ControlG, "switch_element_style",
                        "Switch Element Style")
        await self.bind(Keys.Escape, "undo_pending_event",
                        "Cancel pending event")
        # Map Shortcuts
        await self.bind(Keys.ControlR, "refresh_map", "Refresh")
        # King Shortcuts
        await self.bind("w", "move_up", "Move Up")
        await self.bind(Keys.Up, "move_up", "Move Up")
        await self.bind("s", "move_down", "Move Down")
        await self.bind(Keys.Down, "move_down", "Move Up")
        await self.bind("a", "move_left", "Move Left")
        await self.bind(Keys.Left, "move_left", "Move Up")
        await self.bind("d", "move_right", "Move Right")
        await self.bind(Keys.Right, "move_right", "Move Up")
        await self.bind("c", "move_to_castle", "Move to Castle")
        await self.bind("0", "move_to_origin", "Move to Origin")

    def show_info(self) -> None:
        self.info_area.king_position_info()

    # Binding Functions for Keyboard

    def action_refresh_map(self) -> None:
        self.ville_area.render()
        self.log_area.update(f'Dev Mode {self.dev_mode}')
        self.log_area.update('[MAP] Refresh. Can you feel the wind?')

    def action_switch_element_style(self) -> None:
        actual_style = self.db.get_game_value("element_style")
        if actual_style == "ASCII":
            style = "EMOJI"
            self.db.set_game_value("element_style", "EMOJI")
        else:
            style = "ASCII"
        self.db.set_game_value("element_style", style)
        self.ville_area.element_style = style
        self.log_area.update(f"[GRAPH] Switched to {style} mode")

    def action_undo_pending_event(self) -> None:
        self.pending_event = None
        self.button_area.visible = False

    def action_pause(self) -> None:
        if self.hourglass.speed == 0:
            self.hourglass.speed = 1
            self.log_area.update('[PAUSE] OFF')
        else:
            self.hourglass.speed = 0
            self.log_area.update('[PAUSE] ON')

    def action_time_speed_up(self) -> None:
        if self.hourglass.speed <= 4:
            self.hourglass.speed += 1
            self.log_area.update(
                f'[TIME SPEED UP] {self.hourglass.speed}')
        else:
            self.log_area.update(
                f'[TIME SPEED DOWN] The speed of light is our limit')

    def action_time_speed_down(self) -> None:
        if self.hourglass.speed > 1:
            self.hourglass.speed -= 1
            self.log_area.update(
                f'[TIME SPEED DOWN] {self.hourglass.speed}')
        else:
            self.log_area.update(
                f'[TIME SPEED DOWN] You can\'t go back in time')

    def action_move_up(self) -> None:
        # self.ville_area.king_move_up()
        self.king.move_up()
        self.show_info()

    def action_move_down(self) -> None:
        self.king.move_down()
        self.show_info()

    def action_move_left(self) -> None:
        self.king.move_left()
        self.show_info()

    def action_move_right(self) -> None:
        self.king.move_right()
        self.show_info()

    def action_move_to_castle(self) -> None:
        self.king.move_to_castle()
        self.show_info()

    def action_move_to_origin(self) -> None:
        self.king.move_to_origin()
        self.show_info()

    # Menu called function

    def build(self, data) -> None:
        building = data['building']
        response = self.map.build(building=building)
        message = ''
        if response['type'] == 'occupied_land':
            message = 'OPS! Land already occupied'
        elif response['type'] == 'new_building':
            message = 'Construction was successful'
        if message:
            self.log_area.update(
                f'{message} in {self.ville_area.king_position}')
            self.show_info()

    def menu_build(self, data) -> None:
        self.info_area.element_info(element=data['building'])
        self.button_area.label = 'Confirm Build'
        self.button_area.visible = True
        self.pending_event = {'function': 'build', 'data': data}

    def menu_demolish(self, data=None) -> None:
        response = self.map.demolish()
        if response == 'nothing_to_demolish':
            message = 'We love the nature! Nothing to demolish here!'
        elif response == 'ok':
            message = 'Demolish was successful'
        elif response == 'impossible_castle':
            message = 'OMG! It\'s impossible to destroy the castle!'
        else:
            message = 'Unknow error for demolish'
        self.log_area.update(
            f'{message} in {self.ville_area.king_position}')
        self.show_info()

    def menu_upgrade(self, data=None) -> None:
        message = 'Upgrade'
        self.log_area.update(
            f'{message} in {self.ville_area.king_position}')
        self.show_info()

    def menu_switch_element_style(self, data={}):
        self.action_switch_element_style()

    def menu_resources_log(self, data={}):
        """
            Geneate a file to share with devs to balance resources
        """
        resources = Resource().get_all()
        resources_contents = [f"{r.resource},{r.amount}"
                              for r in resources.values()]
        buildigs_content = [f"{b._building},{b.level}"
                            for b in Building().get_all()]
        hourglass_contents = [
            f"{h_name},{h_value}"
            for h_name, h_value in
            self.hourglass.values.items()
            ]
        filename = join(self.base_path, "resources_log.csv")
        with open(filename, 'w') as resources_log:
            resources_log.write("::Nerdville::\n")
            resources_log.write(f"version,{VERSION}\n")
            resources_log.write(f"build,{BUILD}")
            resources_log.write("\n::Hourglass::\n")
            resources_log.write("\n".join(hourglass_contents))
            resources_log.write("\n::Resources::\n")
            resources_log.write("\n".join(resources_contents))
            resources_log.write("\n::Buildings::\n")
            resources_log.write("\n".join(buildigs_content))
        self.log_area.update(
            f"Resources Log file generated in {filename}")

    # Textual functions

    async def on_mount(self, event: events.Mount) -> None:
        self.base_path = join(expanduser("~"), '.nerdville')
        if not exists(self.base_path):
            makedirs(self.base_path)
        self.db = Db(
            path=self.base_path,
            name='nerdville.db'
        )
        # Create ScroolView to containt the map
        self.body = ScrollView(auto_width=True)
        # Window grid system
        grid = await self.view.dock_grid(edge="left", name="left")
        # Columns
        grid.add_column(fraction=3, name="left", min_size=20)
        grid.add_column(fraction=14, name="center")
        grid.add_column(fraction=2, name="right")
        # Rows
        grid.add_row(fraction=1, name="top")
        grid.add_row(fraction=10, name="middle")
        grid.add_row(fraction=2, name="bottom")
        # Areas
        grid.add_areas(
            title_area="left-start|right-end,top",
            menu_area="left,middle-start|bottom-end",
            game_area="center,middle",
            info_area="right,middle",
            log_area="center,bottom",
            button_area="right,bottom"
        )
        # Define widget to compose the window
        self.title_area = Title()
        self.log_area = Logs()
        self.info_area = Info()
        self.button_area = Button(
            "",
            name="execute_pending_event",
            style="white on rgb(51,51,51)",
            )
        self.button_area.visible = False
        # Define the Menu
        menu = TreeControl("Menu", {})
        await menu.add(
            menu.root.id,
            f"{EMOJI['hammer_and_wrench']}  Build", {},
            )
        await menu.add(
            menu.root.id,
            f"{EMOJI['eyeglasses']}  View", {},
            )
        if self.dev_mode:
            await menu.add(
                menu.root.id,
                f"{EMOJI['computer']}  Dev", {},
                )
            await menu.add(
                menu.root.id + 3,
                f"{EMOJI['file_folder']} Resources Log",
                {"menu_function": "menu_resources_log",
                 "menu_function_data": {}},
                )
        # Build node sub-menus
        await menu.add(
            menu.root.id + 1,
            f"{EMOJI['house']} House",
            {"menu_function": "menu_build",
             "menu_function_data": {'building': "buildings-house"}},
            )
        await menu.add(
            menu.root.id + 1,
            f"{EMOJI['ear_of_rice']} Farm",
            {"menu_function": "menu_build",
             "menu_function_data": {'building': "buildings-farm"}},
            )
        await menu.add(
            menu.root.id + 1,
            f"{EMOJI['axe']} Lumberjack",
            {"menu_function": "menu_build",
             "menu_function_data": {'building': "buildings-lumberjack"}},
            )
        await menu.add(
            menu.root.id + 1,
            f"{EMOJI['fishing_pole']} fisherman",
            {"menu_function": "menu_build",
             "menu_function_data": {'building': "buildings-fisherman"}},
            )
        await menu.add(
            menu.root.id + 1,
            f"{EMOJI['beers']} Tavern",
            {"menu_function": "menu_build",
             "menu_function_data": {'building': "buildings-tavern"}},
            )
        await menu.add(
            menu.root.id + 1,
            f"{EMOJI['hospital']} Hospital",
            {"menu_function": "menu_build",
             "menu_function_data": {'building': "buildings-hospital"}},
            )
        await menu.add(
            menu.root.id + 1,
            f"{EMOJI['church']} Church",
            {"menu_function": "menu_build",
             "menu_function_data": {'building': "buildings-church"}},
            )
        await menu.add(
            menu.root.id + 1,
            f"{EMOJI['hammer']} Demolish",
            {"menu_function": "menu_demolish", "menu_function_data": {}},
            )
        await menu.add(
            menu.root.id + 1,
            f"{EMOJI['up_arrow']} Upgrade",
            {"menu_function": "menu_upgrade", "menu_function_data": {}},
            )
        # View node sub-menus
        await menu.add(
            menu.root.id + 2,
            f"{EMOJI['arrows_counterclockwise']} ASCII/EMOJI Mode",
            {"menu_function": "menu_switch_element_style",
             "menu_function_data": {}},
            )
        await menu.root.expand()
        await menu.nodes[menu.root.id + 1].expand()
        await menu.nodes[menu.root.id + 2].expand()
        if self.dev_mode:
            await menu.nodes[menu.root.id + 3].expand()
        # Fill the grid
        grid.place(
            title_area=self.title_area,
            menu_area=menu,
            game_area=self.body,
            info_area=self.info_area,
            log_area=self.log_area,
            button_area=self.button_area,
        )
        # Define classes
        self.castle = Castle()
        self.king = King()
        self.hourglass = Hourglass()
        self.map = Map()
        self.event = Event()
        self.god = God()

        # Put the map in the ScrollView
        async def add_content():
            self.ville_area = VilleArea()
            await self.body.update(self.ville_area)

        await self.call_later(add_content)

        self.title_area.update_info()
        self.show_info()

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        data = message.node.data
        if data:
            getattr(self, data['menu_function'])(data['menu_function_data'])

    def handle_button_pressed(self, message: ButtonPressed) -> None:
        """A message sent by the button widget"""

        assert isinstance(message.sender, Button)
        button = message.sender
        if button.name == 'execute_pending_event':
            if self.pending_event:
                getattr(self,
                        self.pending_event['function'])\
                    (self.pending_event['data'])
            self.pending_event = None
            self.button_area.visible = False


@click.command()
@click.option('--dev', is_flag=True)
def start(dev):
    NerdVille.run(
        title="NerdVille",
        dev_mode=dev,
    )


if __name__ == '__main__':
    start()
