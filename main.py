import os
import pygame
import pymunk
import argparse
from datetime import datetime

from environment import Environment
from generation import Cohort

# parser = argparse.ArgumentParser(description='.')
# parser.add_argument('-lg', '--load_gen', type=str, help='relative path to generation folder')

# args = parser.parse_args()
# print(args.lg)

if __name__ == "__main__":
    pygame.init()

    # e.g datetime.now format -> '2022-05-20 10:20:34.168220'
    current_time = str(datetime.now())
    current_time = current_time.replace(" ","_").replace(":","-").split(".")[0]
    output_folder = f"runs/{current_time}"
    try:
        os.mkdir(output_folder)
    except FileExistsError:
        print("Output folder for this run already exists.")

    n_generations = 100
    n_individuals = 2**4
    sim_time = 0.1
    surviving_genes = ""
    for n in range(n_generations):
        population = Cohort(n_individuals, surviving_genes)

        gen_folder = f"{output_folder}/gen-{n}"
        try:
            os.mkdir(gen_folder)
        except FileExistsError:
            print("Output folder for this generation already exists.")
        

        gen_avg_fitness = 0
        for organism, metrics in population.cohort.items():
            print(gen_avg_fitness)
            env = Environment(organism)

            i=0
            n_steps = env.fps * sim_time
            while i < n_steps:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        ERROR_KEK

                organism.calculate_fitness()
                # env.draw()
                env.space.step(env.dt)
                env.clock.tick(env.fps)
                i+=1

            
            with open(f"{output_folder}/{str(int(organism.fitness))}_{organism.id}.txt", "w") as f:
                f.write(f"{organism.genes}\n")
                f.write(str(organism.fitness))


            metrics["fitness"] = organism.fitness
            gen_avg_fitness += organism.fitness
        with open(f"{output_folder}/avg_fitness={str(gen_avg_fitness/n_individuals)}.txt", "w") as f:
            pass


        population.selection()
        surviving_genes = population.reproduction()
        print(surviving_genes)