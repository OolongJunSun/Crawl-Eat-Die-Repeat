import time
import pygame
import uuid

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment import Environment
from organism import Organism

if __name__ == "__main__":
    genome = "8FBB6DA 3D8FCEE BFBC24A DCC0D95 A6A6DA8 BACE55F FB1AB89 50CD8FD BD1887B"

    organism = Organism(genome, uuid.uuid4())

    start = time.perf_counter()
    
    draw = True
    env = Environment(organism, draw=draw)

    n_steps = 600

    i = 0
    while i < n_steps:
        if draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ERROR_KEK

            env.draw()
            env.clock.tick(env.fps)

        env.space.step(env.dt)
        

        i += 1

    for shape in env.space.shapes:
        env.space.remove(shape)
        shape.body = None

    finish = time.perf_counter()
    elapsed=finish-start

    print(f"{elapsed=}")