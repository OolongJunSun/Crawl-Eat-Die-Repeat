import os
import time
import pygame
import argparse
from itertools import islice
from datetime import datetime
from multiprocessing import Process, Manager
from experiment import Experiment
from population_loader import Loader
from environment import Environment
from generation import Cohort

# parser = argparse.ArgumentParser(description='.')
# parser.add_argument('-lg', '--load_gen', type=str, help='relative path to generation folder')

# args = parser.parse_args()
# print(args.lg)

def chunks(data, SIZE=64):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}

def main_loop():
    pass

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
    n_individuals = 2**8
    sim_time = 10
    surviving_genes = ""

    # checkpoint_path = "D:\\02_Projects\\03_Active\\Evolution\\CEDR\\runs\\12_00"
    # loader = Loader(checkpoint_path)
    # surviving_genes = loader.gene_pool

    for n in range(n_generations):
        population = Cohort(n_individuals, surviving_genes)


        gen_folder = f"{output_folder}/gen-{n}"
        try:
            os.mkdir(gen_folder)
        except FileExistsError:
            print("Output folder for this generation already exists.")
        

        process_manager = manager = Manager()
        return_dict = manager.dict()

        runs = []
        processes = []
        chunk_size = 32
        # Multiprocessing approach
        for idx, chunk in enumerate(chunks(population.cohort, chunk_size)):
            # print(f"Starting process {idx}...")
            runs.append(Experiment(chunk,  sim_time, gen_folder, idx))
            processes.append(Process(target=runs[idx].main_loop, args=(return_dict,)))

        for process in processes:
            process.start()
        
        for process in processes:
            process.join()

        population = Cohort(n_individuals, surviving_genes, return_dict)
        
        total_fitness = 0
        for individual in population.cohort.values():
            total_fitness += individual["fitness"]

        mean_fitness = total_fitness / len(population.cohort)
        with open(f"{gen_folder}/avg_fitness={str(mean_fitness)}.txt", "w") as f:
            pass

        population.selection()
        surviving_genes = population.reproduction()
        surviving_genes = population.mutation(surviving_genes)

    print("goes hererererer")
  
