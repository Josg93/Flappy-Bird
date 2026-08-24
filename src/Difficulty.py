"""
ISPPV1 2023
Study Case: Flappy Bird

This file contains the Strategy pattern for the game difficulties
(Normal and Hard). Every entity reads its parameters from a Difficulty
strategy instead of the globals in settings.py.
"""

from abc import ABC, abstractmethod
from typing import Tuple

import settings

#aplicamos el patron strategy.
#creamos una clase abstracta Difficulty que toma los posibles valores de variables
#de settings y sus clases hijas pueden tomarlos o usar otros especificos por la dificultad
class Difficulty(ABC):
    @abstractmethod
    def scroll_speed(self) -> float: ...

    @abstractmethod
    def back_scroll_speed(self) -> float: ...

    @abstractmethod
    def gravity(self) -> float: ...

    @abstractmethod
    def jump_takeoff_speed(self) -> float: ...

    @abstractmethod
    def spawn_time_range(self) -> Tuple[float, float]: ...

    @abstractmethod
    def gap_range(self) -> Tuple[int, int]: ...

    @abstractmethod
    def y_variation_range(self) -> Tuple[int, int]: ...

    @abstractmethod
    def moving_ratio(self) -> float: ...

    @abstractmethod
    def horizontal_speed(self) -> float: ...

    @abstractmethod
    def powerup_ratio(self) -> float: ...

    @abstractmethod
    def name(self) -> str: ...


class Normal(Difficulty):
    def scroll_speed(self) -> float:
        return settings.MAIN_SCROLL_SPEED

    def back_scroll_speed(self) -> float:
        return settings.BACK_SCROLL_SPEED

    def gravity(self) -> float:
        return settings.GRAVITY

    def jump_takeoff_speed(self) -> float:
        return settings.JUMP_TAKEOFF_SPEED

    def spawn_time_range(self) -> Tuple[float, float]:
        return (settings.TIME_TO_SPAWN_LOGS, settings.TIME_TO_SPAWN_LOGS)

    def gap_range(self) -> Tuple[int, int]:
        return (settings.LOGS_GAP, settings.LOGS_GAP)


    #variacion de altura de troncos
    def y_variation_range(self) -> Tuple[int, int]:
        return (-20, 20)

    def moving_ratio(self) -> float:
        return 0.0

    def horizontal_speed(self) -> float:
        return 0.0

    def powerup_ratio(self) -> float:
        return 0.0

    def name(self) -> str:
        return "Normal"


class Hard(Difficulty):
    SPAWN_TIME_RANGE = (1.2, 2.0)
    GAP_RANGE = (70, 105)
    Y_VARIATION_RANGE = (-60, 60)
    MOVING_RATIO = 0.25
    HORIZONTAL_SPEED = 120.0
    POWERUP_RATIO = 0.2

    def scroll_speed(self) -> float:
        return settings.MAIN_SCROLL_SPEED

    def back_scroll_speed(self) -> float:
        return settings.BACK_SCROLL_SPEED

    def gravity(self) -> float:
        return settings.GRAVITY

    def jump_takeoff_speed(self) -> float:
        return settings.JUMP_TAKEOFF_SPEED

    # atributos modificados de la dificultad dificil 
    def spawn_time_range(self) -> Tuple[float, float]:
        return self.SPAWN_TIME_RANGE

    def gap_range(self) -> Tuple[int, int]:
        return self.GAP_RANGE

    def y_variation_range(self) -> Tuple[int, int]:
        return self.Y_VARIATION_RANGE

    def moving_ratio(self) -> float:
        return self.MOVING_RATIO

    def horizontal_speed(self) -> float:
        return self.HORIZONTAL_SPEED

    def powerup_ratio(self) -> float:
        return self.POWERUP_RATIO

    def name(self) -> str:
        return "Difícil"
