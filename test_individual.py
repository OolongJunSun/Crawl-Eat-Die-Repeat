import uuid
import pygame
from organism import Organism
from g_env import Environment

if __name__ == "__main__":
    genome = "976546D E15ADBB 85181D0 B6505A3 E0DE7D4 BB8F5CE A7AE5E1 648A457 656BDC4"

    organism = Organism(genome, uuid.uuid4())
    env = Environment(organism)

    i = 0
    n_steps = env.fps * 60
    while i < n_steps:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ERROR_KEK
        print(i)
        organism.calculate_fitness()
        env.draw()
        env.obj_wrap(organism)
        env.space.step(env.dt)
        env.clock.tick(env.fps)
        i += 1

        print(organism.fitness)