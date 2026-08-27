"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class World: the scrolling
background/ground, the log pairs the bird must fly through, and the
power-ups. Every parameter comes from a Difficulty strategy.
"""

import random
from typing import List, Optional

import pygame

from gale.factory import Factory

import settings
from src.Difficulty import Difficulty, Normal
from src.LogPair import LogPair
from src.PowerUp import PowerUp


class World:
    def __init__(
        self, generate_logs: bool = False, difficulty: Optional[Difficulty] = None
    ) -> None:
        # mundo
        self.generate_logs: bool = generate_logs
        self.difficulty: Difficulty = difficulty if difficulty is not None else Normal()
        self.background_x: float = 0.0
        self.ground_x: float = 0.0
        
        # troncos
        self.logs: List[LogPair] = []
        self.logs_spawn_timer: float = 0.0
        spawn_low, spawn_high = self.difficulty.spawn_time_range()
        self.spawn_interval: float = random.uniform(spawn_low, spawn_high)
        self.last_log_y: float = -settings.LOG_HEIGHT + random.randint(0, 80) + 20
        self.log_pair_factory: Factory = Factory(LogPair)
        
        # powerups
        self.powerups: List[PowerUp] = []
        self.powerup_factory: Factory = Factory(PowerUp)

    def reset(self, generate_logs: bool) -> None:
        self.generate_logs = generate_logs

    
    def collides(self, rect: pygame.Rect, ignore_logs: bool = False) -> bool:
        if rect.bottom >= settings.VIRTUAL_HEIGHT:
            return True

        if ignore_logs:
            return False

        return any(log_pair.collides(rect) for log_pair in self.logs)

    def update_scored(self, rect: pygame.Rect) -> bool:
        return any(log_pair.update_scored(rect) for log_pair in self.logs)

    def collides_powerup(self, rect: pygame.Rect) -> Optional[PowerUp]:
        for powerup in self.powerups:
            if powerup.collides(rect):
                return powerup
        return None

    def remove_powerup(self, powerup: PowerUp) -> None:
        self.powerups.remove(powerup)

    def spawn_log(self) -> None:
        
        #configurar espacio entre troncos
        gap_low, gap_high = self.difficulty.gap_range()
        gap = random.randint(gap_low, gap_high)

        #configurar altura a la que se genera el tronco  
        y_low, y_high = self.difficulty.y_variation_range()
        y = max(
            -settings.LOG_HEIGHT + 10,
            min(
                self.last_log_y + random.randint(y_low, y_high),
                settings.VIRTUAL_HEIGHT + gap - settings.LOG_HEIGHT,
            ),
        )
        self.last_log_y = y


        #troncos que se mueven
        move_amplitude = 0.0
        move_speed = 0.0
        if random.random() < self.difficulty.moving_ratio():
            move_amplitude = LogPair.MOVE_AMPLITUDE
            move_speed = random.uniform(1.5, 2.5)

        # crear con factory y añadir tronquito 
        self.logs.append(
            self.log_pair_factory.create(
                settings.VIRTUAL_WIDTH,
                y,
                {
                    "gap": gap,
                    "difficulty": self.difficulty,
                    "move_amplitude": move_amplitude,
                    "move_speed": move_speed,
                },
            )
        )

    def spawn_powerup(self) -> None:
        #margen para poner pixeles mas cerca del jugador 
        margin = 40
        #posicion del powerup
        y = random.uniform(
            margin,
            settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT - margin - settings.POWERUP_SIZE,
        )
        x = settings.VIRTUAL_WIDTH + random.randint(60, 260)
        #crear y añadir powerup
        self.powerups.append(self.powerup_factory.create(x, y))

    def update(self, dt: float) -> None:
        
        #generacion de tronquitos
        if self.generate_logs:
            self.logs_spawn_timer += dt

            #intervalos entre troncos
            if self.logs_spawn_timer >= self.spawn_interval:
                self.logs_spawn_timer = 0.0
                spawn_low, spawn_high = self.difficulty.spawn_time_range()
                self.spawn_interval = random.uniform(spawn_low, spawn_high)
                self.spawn_log()

                if random.random() < self.difficulty.powerup_ratio():
                    self.spawn_powerup()

        #movimiento del mundo
        self.background_x += -self.difficulty.back_scroll_speed() * dt
        
        if self.background_x <= -settings.BACKGROUND_LOOPING_POINT:
            self.background_x = 0
            
        self.ground_x += -self.difficulty.scroll_speed() * dt
        
        if self.ground_x <= -settings.VIRTUAL_WIDTH:
            self.ground_x = 0
            
        #actualizar powerups y troncos    
        for log_pair in self.logs:
            log_pair.update(dt)
        
        scroll_speed = self.difficulty.scroll_speed()    
        for powerup in self.powerups:
            powerup.update(dt, scroll_speed)
                
        self.logs = [log_pair for log_pair in self.logs if not log_pair.is_out_of_game()]
        self.powerups = [powerup for powerup in self.powerups if not powerup.is_out_of_game()]
        
        
             
        
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["background"], (round(self.background_x), 0))

        for log_pair in self.logs:
            log_pair.render(surface)

        for powerup in self.powerups:
            powerup.render(surface)

        surface.blit(
            settings.TEXTURES["ground"],
            (round(self.ground_x), settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT),
        )
