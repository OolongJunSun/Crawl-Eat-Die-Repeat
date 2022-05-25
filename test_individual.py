import uuid
import pygame
from organism import Organism
from g_env import Environment

if __name__ == "__main__":
    genome = "4006bc9 ee9d5e5 c6145ba fb967e9 ee8798f 5e774be 12775c5 e8e1e5f e8cd7da cd3f9a7 5f0dfc7 944c7fb 8ebf11d"

    organism = Organism(genome, uuid.uuid4())
    env = Environment(organism)

    i = 0
    n_steps = env.fps * 20
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

        print(organism.fitness)