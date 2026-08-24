"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class LogPair: a top log
(rendered flipped upside down) and a bottom log, a variable number of
pixels apart, that scroll left together and score once the bird passes
them. A pair may oscillate its gap (open and close) when its difficulty
strategy requests it.
"""

import math
import random

from typing import Optional

import pygame

import settings
from src.Difficulty import Difficulty, Normal


class LogPair:
    MOVE_AMPLITUDE = 22.0

    def __init__(
        self,
        x: float,
        y: float,
        gap: Optional[int] = None,
        difficulty: Optional[Difficulty] = None, #paso la dificultad al constructor
        move_amplitude: float = 0.0,
        move_speed: float = 0.0,
    ) -> None:
        self.x: float = x
        self.y: float = y
        self.scored: bool = False
        self.difficulty: Difficulty = difficulty if difficulty is not None else Normal()
        self.base_gap: int = settings.LOGS_GAP if gap is None else gap
        self.move_amplitude: float = move_amplitude
        self.move_speed: float = move_speed
        self.phase: float = random.uniform(0.0, math.tau)

    def get_gap(self) -> float:
        if self.move_amplitude <= 0:
            return self.base_gap

        max_gap = (
            settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT - settings.LOG_HEIGHT - self.y
        )
        gap = self.base_gap + self.move_amplitude * math.sin(self.phase)
        return max(settings.LOGS_MIN_GAP, min(gap, max_gap))

    def get_top_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), settings.LOG_WIDTH, settings.LOG_HEIGHT)

    def get_bottom_rect(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.x),
            round(self.y + self.get_gap() + settings.LOG_HEIGHT),
            settings.LOG_WIDTH,
            settings.LOG_HEIGHT,
        )

    def collides(self, rect: pygame.Rect) -> bool:
        return self.get_top_rect().colliderect(rect) or self.get_bottom_rect().colliderect(rect)

    def update(self, dt: float) -> None:
        self.x += -self.difficulty.scroll_speed() * dt
        if self.move_amplitude > 0:
            self.phase += self.move_speed * dt

    def is_out_of_game(self) -> bool:
        return self.x < -settings.LOG_WIDTH

    def update_scored(self, rect: pygame.Rect) -> bool:
        if self.scored:
            return False

        if rect.left > self.x + settings.LOG_WIDTH:
            self.scored = True
            return True

        return False

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["log_inverted"], self.get_top_rect())
        surface.blit(settings.TEXTURES["log"], self.get_bottom_rect())
