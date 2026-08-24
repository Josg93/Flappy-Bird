"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class PauseState. It freezes
the gameplay and keeps the world, bird, and score so the game can be
resumed exactly where it was.
"""

from typing import Optional

import pygame

import settings

from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text

from src.World import World
from src.Bird import Bird


class PauseState(BaseState):
    def enter(
        self,
        world: Optional[World] = None,
        bird: Optional[Bird] = None,
        score: Optional[int] = None,
    ) -> None:
        self.world = world if world is not None else World()
        self.bird = bird if bird is not None else Bird(
            settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
            settings.BIRD_WIDTH,
            settings.BIRD_HEIGHT,
        )
        self.score = score
        settings.SOUNDS["pause"].play()

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["flappy"],
            20,
            10,
            settings.COLOR_WHITE,
            shadowed=True,
        )
        render_text(
            surface,
            "PAUSED",
            settings.FONTS["huge"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - 40,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "playing", world=self.world, bird=self.bird, score=self.score
            )
