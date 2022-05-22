
import time
import multiprocessing
from datetime import datetime
from multiprocessing import Pool

from environment import Environment
from population import Population
from utils import make_dir_w_exception


def evaluate_individual(organism):
    start = time.perf_counter()
    env = Environment(organism[1]["instance"])

    n_steps = 60 * 10
    i = 0
    while i < n_steps:
        organism[1]["instance"].calculate_fitness()
        env.space.step(env.dt)
        i += 1

    finish = time.perf_counter()
    elapsed=finish-start
    print(f"{elapsed=}")

    fit = organism[1]["instance"].fitness
    id = organism[1]["instance"].id
    
    return (id, fit)


def start_process():
    print('Starting', multiprocessing.current_process().name)


if __name__ == "__main__":

    # # e.g datetime.now format -> '2022-05-20 10:20:34.168220'
    current_time = str(datetime.now())
    current_time = current_time.replace(" ","_").replace(":","-").split(".")[0]
    output_folder = f"runs/{current_time}"
    make_dir_w_exception(output_folder)

    # Evolution configs
    n_generations = 100
    n_individuals = 300
    surviving_genes = ""

    population = Population(n_individuals)
    gene_pool = population.initialize_genepool()
    population.generate_individuals(gene_pool)

    
    pool = Pool(initializer=start_process)   

    for n in range(n_generations):
        gen_folder = f"{output_folder}/gen-{n}"
        make_dir_w_exception(gen_folder)

        results = pool.map(evaluate_individual, population.cohort.items())
        
        for result in results:
            population.cohort[result[0]]["fitness"] = result[1]
            with open(f"{gen_folder}/{str(int(result[1]))}_{result[0]}.txt", "w") as f:
                f.write(f"{population.cohort[result[0]]['genome']}\n")
                f.write(str(result[1]))

        total_fitness = 0
        for individual in population.cohort.values():
            total_fitness += individual["fitness"]

        mean_fitness = total_fitness / len(population.cohort)
        with open(f"{gen_folder}/avg_fitness={str(mean_fitness)}.txt", "w") as f:
            pass

        print(f"{mean_fitness=}")

        population.selection()
        gene_pool = population.reproduction()
        gene_pool = population.mutation(gene_pool)
        offspring = population.divide_genepool(gene_pool)

        population.generate_individuals(offspring)
