import math

import pygame

import settings


class PowerUp:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.time: float = 0.0
 
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.x),
            round(self.y),
            settings.POWERUP_SIZE,
            settings.POWERUP_SIZE,
        )

    def collides(self, rect: pygame.Rect) -> bool:
        return self.get_rect().colliderect(rect)

    def is_out_of_game(self) -> bool:
        return self.x < -settings.POWERUP_SIZE

    def update(self, dt: float, scroll_speed: float) -> None:
        self.time += dt
        self.x += -scroll_speed * dt

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["powerup"], self.get_rect())
