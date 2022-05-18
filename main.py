import random
import pygame
import pymunk

from environment import Environment
from generation import Cohort

if __name__ == "__main__":
    pygame.init()

    population = Cohort(n_indiviuals=240)

    print(population.cohort)

    for organism, metrics in population.cohort.items():
        env = Environment()

        env.space.add(organism.body.head.matter, organism.body.head.shape)
        organism.body.head.shape.filter = pymunk.ShapeFilter(group=2)
        
        for part in organism.body.structure.values():
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

            organism.calculate_fitness()
            env.draw()
            env.space.step(env.dt)
            env.clock.tick(env.fps)
            i+=1

        with open(f"organisms/{str(int(organism.fitness))}_{organism.id}.txt", "w") as f:
            f.write(f"{organism.genes}\n")
            f.write(str(organism.fitness))
        f.close()