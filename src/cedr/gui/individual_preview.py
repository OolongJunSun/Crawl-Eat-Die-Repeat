import time
import json
import uuid
import pygame

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cedr.environment import SimpleHabitat
from cedr.individual import BasicProtein

class Previewer():
    def __init__(self, cfg: str = None) -> None:
        with open("simulation_config.json") as json_data_file:
            self._cfg = json.load(json_data_file)

        self._genome = None
        
    @property
    def genome(self):
        return self._genome

    @genome.setter
    def genome(self, value):
        self._genome = value

    @genome.deleter
    def genome(self):
        del self._genome    

    @property
    def cfg(self):
        return self._cfg

    @cfg.setter
    def cfg(self, category, key, value):
        self._cfg[category][key] = value

    @cfg.deleter
    def cfg(self, category, key):
        del self._cfg[category][key]    

    def create_individual(self):
        self.individual = BasicProtein(self.genome, uuid.uuid4())

    def create_environment(self):
        self.env = SimpleHabitat(
            self.cfg["environment"], 
            seed=56, 
            individual=self.individual, 
            draw=True
        )

    def simulate(self):
        n_steps = self.cfg['environment']['run_time'] * self.env.fps

        i = 0
        while i < n_steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.individual.calculate_fitness()
            print(self.individual.fitness)
                
            self.env.draw()
            self.env.clock.tick(self.env.fps)
            i += 1
            print(i)

            self.env.space.step(self.env.dt)

        pygame.quit()