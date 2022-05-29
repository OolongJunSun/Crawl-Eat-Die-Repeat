import uuid
import pygame
from organism import Organism
from g_env import Environment

if __name__ == "__main__":
    genome = "ED27D6B EFDDF7B DEDBFF3 DEDA056 FD5BFD5 FF9E5DB EF0B696 9EBBCAB 58515D5"
    # genome = "53546ec fd04ce5 c470685 f723a3f 97269e7 c776e5d 53c64c9 4d63e71 f4bc592"
    # A0D42E7 C2F5DDB 6691A19 C7AF175 E57BFC2 3F41CD6 986DFD9 76A2996 A263CF9 <- pop exploiter
    genome = "EFB9E9B FFC197F 2E165F9 97C15E5 DEF687A D54641C ECE5D8B 1B964B3 E0C6FC0"

    organism = Organism(genome, uuid.uuid4())
    env = Environment(organism)

    i = 0
    n_steps = env.fps * 30
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
        print(organism.fitness)
        i += 1

    for shape in env.space.shapes:
        env.space.remove(shape)
        shape.body = None
        