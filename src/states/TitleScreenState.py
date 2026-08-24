"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class TitleScreenState. It
shows a navigable menu to pick the difficulty (Strategy) before the
countdown starts.
"""

from typing import List

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Difficulty import Difficulty, Hard, Normal
from src.World import World


class TitleScreenState(BaseState):
    def enter(self) -> None:
        self.world = World()
        self.difficulties: List[Difficulty] = [Normal(), Hard()]
        self.selected: int = 0

    def update(self, dt: float) -> None:
        self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        render_text(
            surface,
            "Flappy Bird",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

        base_y = 2 * settings.VIRTUAL_HEIGHT / 3 - 30
        for i, difficulty in enumerate(self.difficulties):
            is_selected = i == self.selected
            label = f"> {difficulty.name()} <" if is_selected else difficulty.name()
            color = settings.COLOR_YELLOW if is_selected else settings.COLOR_WHITE
            render_text(
                surface,
                label,
                settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH / 2,
                base_y + i * 26,
                color,
                center=True,
                shadowed=True,
            )

        render_text(
            surface,
            "Arrows to select - Enter to start",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT - 30,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not input_data.pressed:
            return

        if input_id == "selection_up":
            self.selected = (self.selected - 1) % len(self.difficulties)
        elif input_id == "selection_down":
            self.selected = (self.selected + 1) % len(self.difficulties)
        elif input_id == "confirm":
            self.state_machine.change(
                "count_down", difficulty=self.difficulties[self.selected]
            )
