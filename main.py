import os
import random
import pygame
import pymunk
from datetime import datetime
from environment import Environment
from generation import Cohort

if __name__ == "__main__":
    pygame.init()

    date_time = datetime.now()
    current_time = "_".join(str(date_time).split(' ')[1].split(".")[0].split(":")[:-1])
    
    output_folder_root = f"runs/{current_time}"
    os.mkdir(output_folder_root)
    
    n_generations = 100
    sim_time = 10
    survivors = ""
    for g in range(n_generations):

        population = Cohort(2**7, survivors)
    
        generation_folder = f"/gen-{g}"
        output_folder = output_folder_root + generation_folder
        os.mkdir(output_folder)
        gen_avg_fitness = 0
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
            n_steps = env.fps * sim_time
            while i < n_steps:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        ERROR_KEK

                organism.calculate_fitness()
                env.draw()
                env.space.step(env.dt)
                env.clock.tick(env.fps)
                i+=1

            
            with open(f"{output_folder}/{str(int(organism.fitness))}_{organism.id}.txt", "w") as f:
                f.write(f"{organism.genes}\n")
                f.write(str(organism.fitness))
            f.close()

            metrics["fitness"] = organism.fitness
            gen_avg_fitness += organism.fitness
        with open(f"{output_folder}/avg_fitness={str(gen_avg_fitness/128)}.txt", "w") as f:
            pass
        f.close()

        population.selection()
        survivors = population.reproduction()