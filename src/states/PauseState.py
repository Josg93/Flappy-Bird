from typing import Optional

import settings
import pygame

from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text

#debo importar el mundo y el pajarito:
from src.World import World
from src.Bird import Bird 

class PauseState(BaseState):
    def enter(self, 
              world : Optional[World] = None,
              bird : Optional[Bird] = None,
              score : Optional[int] = None):
        
        self.world = world if world is not None else World()
        self.bird = bird if bird is not None else Bird(
            settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
            settings.BIRD_WIDTH,
            settings.BIRD_HEIGHT,)
        self.score = score
    
    def update(self, dt : float):
        self.bird.vy=0
        self.world.background_x= self.world.background_x 
        settings.SOUNDS["pause"].play() 
    
    #El renderizado deberia ser igual que el del playing state 
    def render(self, surface : pygame.Surface):
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
    
    def on_input(self, input_id : str , input_data : InputData)-> None:
        if input_id == "pause" and input_data.pressed:
            self.state_machine.change("playing" ,world = self.world, bird= self.bird, score = self.score)
            
            