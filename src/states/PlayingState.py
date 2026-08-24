"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class PlayingState.
"""

from typing import Optional

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World


class PlayingState(BaseState):
    def enter(self,
              world: Optional[World] = None,
              bird : Optional[Bird] = None,
              score : Optional[int] = None) -> None:
        
        self.world = world if world is not None else World()
        self.world.reset(True)

        # recibe un pajaro si es el inicio del juego y no se recibe nada pues
        # crea el ave, sino entonces viene de un estado de pausa y recibe las coordenadas
        # guardadas

        self.bird = bird if bird is not None else Bird(
            settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
            settings.BIRD_WIDTH,
            settings.BIRD_HEIGHT,
            #tomamos la dificultad del mundo y se la pasamos al ave
            difficulty=self.world.difficulty,
        )
        self.score = score if score is not None else 0

    def update(self, dt: float) -> None:
        self.bird.update(dt)
        self.world.update(dt)

        if self.world.collides(
            self.bird.get_rect(), ignore_logs=self.bird.is_ghost()
        ):
            settings.SOUNDS["explosion"].play()
            settings.SOUNDS["hurt"].play()
            self.state_machine.change("count_down", difficulty=self.world.difficulty)
            return

        powerup = self.world.collides_powerup(self.bird.get_rect())
        if powerup is not None:
            self.world.remove_powerup(powerup)
            self.bird.activate_ghost(settings.POWERUP_DURATION)
            settings.SOUNDS["score"].play()

        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

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
            self.world.difficulty.name(),
            settings.FONTS["medium"],
            20,
            36,
            settings.COLOR_YELLOW,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "jump" and input_data.pressed:
            self.bird.jump()
        elif input_id in ("move_left", "move_right"):
            self.bird.handle_move(input_id, input_data)
        elif input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "pause", world=self.world, bird=self.bird, score=self.score
            )
