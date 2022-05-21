import time
import pygame
from datetime import datetime

from environment import Environment

class Experiment():
    def __init__(self, population, sim_time, output_folder, process_idx) -> None:
        self.population = population
        self.sim_time = sim_time
        self.output_folder = output_folder
        self.process_idx = process_idx

    def main_loop(self, return_dict):
        for organism, metrics in self.population.items():
            env = Environment(organism)

            start = time.perf_counter()
            
            i=0
            n_steps = env.fps * self.sim_time
            while i < n_steps:
                # for event in pygame.event.get():
                #     if event.type == pygame.QUIT:
                #         ERROR_KEK

                organism.calculate_fitness()
                # env.draw()
                # env.display_fps()
                env.space.step(env.dt)
                env.clock.tick(env.fps)
                i+=1



            finish = time.perf_counter()
            elapsed=finish-start

            with open(f"{self.output_folder}/{str(int(organism.fitness))}_{organism.id}.txt", "w") as f:
                f.write(f"{organism.genes}\n")
                f.write(str(organism.fitness))


            print(f"{self.process_idx=}")
            print(f"{elapsed=}")
            print("")
            
            return_dict.update(
                {
                    organism: {
                        "fitness": organism.fitness,
                        "genome": metrics["genome"]}})
