import time
import json
import random
import faulthandler
import multiprocessing

from itertools import repeat, chain, product
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

    for seeds in product(
        cfg["environment"]["seed"],
        cfg["gene_pool"]["seed"],
        cfg["selection"]["seed"],
        cfg["crossover"]["seed"],
        cfg["mutation"]["seed"]
    ):
        print(seeds)

        io_manager = Manager()
        io_manager.make_output_dir()
        io_manager.save_run_config(cfg)

        env_rng = random.Random(seeds[0])

        # Initialise population
        if cfg["gene_pool"]["load_from_checkpoint"] == "True":
            #   1) Load from checkpoint
            PATH = "D:\\02_Projects\\03_Active\EvolutionV2\\CEDR_REWRITE\\src\\cedr\\runs\\2022-06-12_01-18-29\\generation-6"
            gene_pool = io_manager.load_population(PATH)
        else:
            #   2) Randomly initialise
            population = Population(cfg["gene_pool"], seeds[1])
            population.init_gene_pool()
            population.individuate_genomes()
            population.generate_individuals()


        metrics = Metrics()
        selection = Selector(cfg["selection"], seeds[2])
        reproduction = Reproducer(cfg["crossover"], seeds[3], population.cohort)
        mutation = Mutator(cfg["mutation"], seeds[4])

        pool = multiprocessing.Pool(initializer=start_process)

        for generation in range(cfg["species"]["n_generations"]):
            io_manager.make_output_dir(generation)

            if cfg["environment"]["STATIC"]:
                env_seed = cfg["environment"]["seed"]
            else:
                env_seed = env_rng.randint(0, 100000)

            results = pool.starmap(
                evaluate_individual,
                zip(repeat(cfg["environment"]), repeat(env_seed), population.cohort.values())
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

            io_manager.output_data(population.cohort, results, metrics.generation_stats, metrics.run_stats)

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

            if metrics.generation_stats["mean_diversity"] < 50:
                break
