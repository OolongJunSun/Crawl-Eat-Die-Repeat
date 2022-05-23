import uuid
import pygame
from organism import Organism
from environment import Environment

if __name__ == "__main__":
    genome = "ac17b1 2d25d4 eb65a9 db2069 a9e34d 11e6e9 2bce38 d36858 51dd93 7fe9fb 9b6695 0e74ae 1107f3"

    organism = Organism(genome, uuid.uuid4())
    env = Environment(organism)

    i = 0
    n_steps = env.fps * 10
    while i < n_steps:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ERROR_KEK
        print(i)
        organism.calculate_fitness()
        env.draw()
        env.space.step(env.dt)
        env.clock.tick(env.fps)
        i += 1

