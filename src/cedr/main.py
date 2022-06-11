import time
import json
import random
import faulthandler
import multiprocessing

from itertools import repeat, chain
from operator import itemgetter

from environment import SimpleHabitat
from data_manager import Manager
from metrics import Metrics
from population import Population
from selection import Selector
from reproduction import Reproducer
from mutation import Mutator


def start_process():
    print('Starting', multiprocessing.current_process().name)


def evaluate_individual(cfg, seed, individual):
    individual = individual["instance"]

    start = time.perf_counter()

    env = SimpleHabitat(cfg, seed, individual)

    n_steps = env.fps * cfg["run_time"]
    i = 0
    while i < n_steps:
        individual.calculate_fitness()
        env.space.step(env.dt)
        i += 1

    for shape in env.space.shapes:
        env.space.remove(shape)
        shape.body = None

    finish = time.perf_counter()
    elapsed = finish - start
    print(f"{elapsed=}")

    return (individual.id, individual.fitness)


if __name__ == "__main__":
    faulthandler.enable()

    with open("config.json") as json_data_file:
        cfg = json.load(json_data_file)

    io_manager = Manager()
    io_manager.make_output_dir()

    # Initialise population
    #   a) Randomly initialise
    population = Population(cfg["gene_pool"])
    population.init_gene_pool()
    population.individuate_genomes()
    population.generate_individuals()

    #   b) Load from checkpoint
    #   ADD THIS

    metrics = Metrics()
    selection = Selector(cfg["selection"])
    reproduction = Reproducer(cfg["crossover"], population.cohort)
    mutation = Mutator(cfg["mutation"])

    pool = multiprocessing.Pool(initializer=start_process)

    for generation in range(cfg["species"]["n_generations"]):
        io_manager.make_output_dir(generation)

        seed = random.randint(0, 100000)

        results = pool.starmap(
            evaluate_individual,
            zip(repeat(cfg["environment"]), repeat(seed), population.cohort.values())
        )

        # Sort individuals by descending fitness
        results.sort(key=itemgetter(1), reverse=True)


        fitness_values = [result[1] for result in results]
        metrics.mean_fitness(fitness_values)
        metrics.median_fitness(fitness_values)
        metrics.cutoff_fitness(fitness_values, cfg["selection"]["survival_rate"])

        ranked_genomes = [population.cohort[result[0]]["genome"] for result in results] 
        metrics.population_diversity(ranked_genomes)
        metrics.population_mean_diversity()
        metrics.update_run_stats(generation)
        print(metrics.generation_stats)

        breeding_individuals = selection.methods[cfg["selection"]["method"]](ranked_genomes)

        breeding_pairs = selection.form_pairs_randomly(breeding_individuals)

        offspring = [reproduction.single_point_crossover(pair) for pair in breeding_pairs]
        offspring = list(chain.from_iterable(offspring))

        gene_pool = "".join(offspring)
        mutated_gene_pool = mutation.random_mutation(gene_pool)

        # We need to do this to avoid segfaults when multiprocessing
        population.clear_pymunk_objects_from_memory()

        population.gene_pool = mutated_gene_pool
        population.individuate_genomes()
        population.generate_individuals()
