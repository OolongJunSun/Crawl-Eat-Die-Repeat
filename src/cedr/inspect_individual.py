import time
import json
import uuid
import pygame

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment import SimpleHabitat
from individual import BasicProtein

if __name__ == "__main__":
    genome = "0A9DE08 14FDC75 9C6B37B C4DFE95 3E50B6C 056F175 DA6D083 417F77E D4078F1"

    with open("config.json") as json_data_file:
        cfg = json.load(json_data_file)

    organism = BasicProtein(genome, uuid.uuid4())

    start = time.perf_counter()
    
    draw = True
    env = SimpleHabitat(cfg["environment"], seed=27, individual=organism, draw=draw)
    print("OK")
    n_steps = 3600

    i = 0
    while i < n_steps:
        if draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ERROR_KEK
            organism.calculate_fitness()
            print(organism.fitness)
            
            env.draw()
            env.clock.tick(env.fps)

        env.space.step(env.dt)
        
        print(i)
        i += 1

    for shape in env.space.shapes:
        env.space.remove(shape)
        shape.body = None

    finish = time.perf_counter()
    elapsed=finish-start

    print(f"{elapsed=}")