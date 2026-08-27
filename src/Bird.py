"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class Bird. Its physics
parameters come from a Difficulty strategy; when the strategy allows
horizontal movement, the bird can be steered left/right.
"""

from typing import Optional

from gale.input_handler import InputData

import pygame

import settings
from src.Difficulty import Difficulty, Normal


class Bird:
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        difficulty: Optional[Difficulty] = None,
    ) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0
        self.vx: float = 0.0
        self.jumping: bool = False
        self.difficulty: Difficulty = difficulty if difficulty is not None else Normal()
        self.moving_left: bool = False
        self.moving_right: bool = False
        self.ghost_timer: float = 0.0
        self._ghost_texture: Optional[pygame.Surface] = None

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def jump(self) -> None:
        self.jumping = True

    def handle_move(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_left":
            self.vx = -self.difficulty.horizontal_speed() if input_data.pressed else 0.0
        elif input_id == "move_right":
            self.vx = self.difficulty.horizontal_speed() if input_data.pressed else 0.0

    #manejo de modo fantasma
    def activate_ghost(self, duration: float) -> None:
        self.ghost_timer = duration

    def is_ghost(self) -> bool:
        return self.ghost_timer > 0

    def update(self, dt: float) -> None:
        self.vy += self.difficulty.gravity() * dt
        
        if self.jumping:
            settings.SOUNDS["jump"].play()
            self.vy = -self.difficulty.jump_takeoff_speed()
            self.jumping = False

        self.y += self.vy * dt
        self.x = max(0.0,min(self.x + self.vx * dt, settings.VIRTUAL_WIDTH - self.width),)

        if self.ghost_timer > 0:
            #la funcion max acota el tiempo entre 0 y el tiempo - dt
            self.ghost_timer = max(0.0, self.ghost_timer - dt)
        
         

    def render(self, surface: pygame.Surface) -> None:
        texture = settings.TEXTURES["bird"]
        if self.is_ghost():
            if self._ghost_texture is None:
                self._ghost_texture = texture.copy()
                self._ghost_texture.set_alpha(110)
            texture = self._ghost_texture
        surface.blit(texture, self.get_rect())
