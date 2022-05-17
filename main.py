import random
import pygame
import pymunk

from environment import Environment
from organism import Organism

if __name__ == "__main__":
    pygame.init()

    for _ in range(1000):
        env = Environment()

        # in the future genomes will be produced by both
        # a) random function
        # b) reproduction
        gene_length = 4
        genome = '%052x' % random.randrange(16**52)
        genome =  ' '.join(genome[i:i+gene_length] for i in range(0, len(genome), gene_length))
        # genome = "903d 8054 c9a5 237b 8620 a023 9b91 8f8f 2e5e"
        adam = Organism(genome)

        env.space.add(adam.body.head.matter, adam.body.head.shape)

        adam.body.head.shape.filter = pymunk.ShapeFilter(group=2)

        for part in adam.body.structure.values():
            env.space.add(part["obj"].matter, part["obj"].shape)

            part["obj"].shape.filter = pymunk.ShapeFilter(group=2)
            
            for joint in part["joints"]:
                env.space.add(joint)

        i=0
        n_steps = env.fps * 15
        while i < n_steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ERROR_KEK

            adam.calculate_fitness()
            env.draw()
            env.space.step(env.dt)
            env.clock.tick(env.fps)
            # print(i)
            i+=1

        with open(f"organisms/{str(int(adam.fitness))}_{genome}.txt", "w") as f:
            f.write(str(adam.fitness))
