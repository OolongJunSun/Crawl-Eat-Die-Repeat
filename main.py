import os
import time
import multiprocessing
from datetime import datetime
from multiprocessing import Pool

from environment import Environment
from population import Population
from utils import make_dir_w_exception
import faulthandler

def evaluate_individual(organism):
    start = time.perf_counter()
    env = Environment(organism[1]["instance"])

    n_steps = env.fps * 30
    i = 0
    while i < n_steps:
        organism[1]["instance"].calculate_fitness()
        env.space.step(env.dt)
        env.obj_wrap(organism[1]["instance"])
        i += 1

    for shape in env.space.shapes:
        env.space.remove(shape)
        shape.body = None


    finish = time.perf_counter()
    elapsed=finish-start
    print(f"{elapsed=}")

    fit = organism[1]["instance"].fitness
    id = organism[1]["instance"].id
    
    return (id, fit)

def load_gene_pool(PATH):
    gene_pool = ""
    for file in os.listdir(PATH):
        if not file.startswith("a"):
            with open(os.path.join(PATH,file), "r") as f:
                genome = f.readline()
                gene_pool += genome.replace(" ","").strip("\n") 
    return gene_pool        

def start_process():
    print('Starting', multiprocessing.current_process().name)


if __name__ == "__main__":
    faulthandler.enable()

    # # e.g datetime.now format -> '2022-05-20 10:20:34.168220'
    current_time = str(datetime.now())
    current_time = current_time.replace(" ","_").replace(":","-").split(".")[0]
    output_folder = f"runs/{current_time}"

    # Evolution configs
    n_generations = 200
    n_individuals = 10
    surviving_genes = ""

    load_from_folder = False
    gen = 10

    population = Population(n_individuals)

    if load_from_folder:
        output_folder = "D:\\02_Projects\\03_Active\\Evolution\\Crawl-Eat-Die-Repeat-broken\\runs\\2022-05-29_13-43-39"
        save_path = os.path.join(output_folder, f"gen-{gen}")
        gen += 1
        gene_pool = load_gene_pool(save_path)
        gene_pool = population.divide_genepool(gene_pool)
    else:
        output_folder = f"runs/{current_time}"
        make_dir_w_exception(output_folder)
        gen = 0
        gene_pool = population.initialize_genepool()
    
    population.generate_individuals(gene_pool)
    
    pool = Pool(initializer=start_process)   

    for n in range(n_generations):
        gen_folder = f"{output_folder}/gen-{n+gen}"
        make_dir_w_exception(gen_folder)

        # with Pool(initializer=start_process) as pool:
        results = pool.map(evaluate_individual, population.cohort.items())

        print(results)
        for organism in population.cohort.values():
            for limb in organism["instance"].body.structure.values():
                limb["obj"].matter = None
                limb["obj"].shape = None
                for joint in limb["joints"]:
                    joint = None 

        
        results_list = []
        for result in results:
            population.cohort[result[0]]["fitness"] = result[1]

            i_string = f"{str(result[1])} - {population.cohort[result[0]]['genome']}\n"
            results_list.append(i_string)
            
        with open(f"{gen_folder}/individuals.txt", "w") as f:
            for result in results_list:
                print(result)
                f.write(result)
            # f.write(f"{population.cohort[result[0]]['genome']}\n")
            # f.write(str(result[1]))

        total_fitness = 0
        for individual in population.cohort.values():
            total_fitness += individual["fitness"]

        mean_fitness = total_fitness / len(population.cohort)
        with open(f"{gen_folder}/avg_fitness={str(mean_fitness)}.txt", "w") as f:
            pass

        print(f"{mean_fitness=}")

        population.selection()
        offspring = population.reproduction()
        offspring = population.mutation(offspring)

        next_generation = population.initialize_genepool(offspring)
        population.generate_individuals(next_generation)
