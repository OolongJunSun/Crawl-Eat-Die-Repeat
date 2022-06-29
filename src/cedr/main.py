import time
import json
import random
import faulthandler
import multiprocessing

from collections import namedtuple
from itertools import repeat, chain, product
from operator import itemgetter

from environment import SimpleHabitat
from population import Population
from selection import Selector
from reproduction import Reproducer
from mutation import Mutator
from utils.data_manager import Manager
from utils.metrics import Metrics

def start_process():
    print('Starting', multiprocessing.current_process().name)


def evaluate_individual(cfg, seed, individual):
    individual = individual["instance"]

    start = time.perf_counter()

    env = SimpleHabitat(cfg, seed, individual)

    n_steps = env.fps * cfg["run-time"]
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

    Variable = namedtuple('Variable', ['category_key', 'value'])
    variables = []
    for category, field in cfg.items():
        for key, value in field.items():
            if isinstance(value, list):
                variables.append(Variable(f'{category}_{key}', value))   

    keys = [var.category_key for var in variables]

    for vars in zip(product(*[var.value for var in variables]), repeat(keys)):
        cat_keys = [k.split('_') for k in keys]
        for i, key in enumerate(cat_keys):
                cfg[key[0]][key[1]] = vars[0][i]

        io_manager = Manager(cfg, vars)
        io_manager.make_output_dir()
        io_manager.save_run_config()

        env_rng = random.Random(cfg['environment']['seed'])

        # Initialise population
        if cfg["gene-pool"]["load-from-checkpoint"] == "True":
            #   1) Load from checkpoint
            PATH = "D:\\02_Projects\\03_Active\EvolutionV2\\CEDR_REWRITE\\src\\cedr\\runs\\2022-06-12_01-18-29\\generation-6"
            gene_pool = io_manager.load_population(PATH)
        else:
            #   2) Randomly initialise
            population = Population(cfg["gene-pool"])
            population.init_gene_pool()
            population.individuate_genomes()
            population.generate_individuals()


        metrics = Metrics()
        selection = Selector(cfg["selection"])
        reproduction = Reproducer(cfg["crossover"], population.cohort)
        mutation = Mutator(cfg["mutation"])

        pool = multiprocessing.Pool(processes=3, initializer=start_process)

        for generation in range(cfg["species"]["n-generations"]):
            io_manager.make_output_dir(generation)

            if cfg["environment"]["STATIC"]:
                env_seed = cfg["environment"]["seed"]
            else:
                env_seed = env_rng.randint(0, 100000)

            results = pool.starmap(
                evaluate_individual,
                zip(repeat(cfg["environment"]), repeat(env_seed), population.cohort.values())
            )

            # Sort individuals by descending fitness-
            results.sort(key=itemgetter(1), reverse=True)

            fitness_values = [result[1] for result in results]
            metrics.mean_fitness(fitness_values)
            metrics.median_fitness(fitness_values)
            metrics.cutoff_fitness(fitness_values, cfg["selection"]["survival-rate"])

            ranked_genomes = [population.cohort[result[0]]["genome"] for result in results]
            metrics.population_diversity(ranked_genomes)
            metrics.mean_diversity()
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

            if metrics.generation_stats["mean_diversity"] < 1:
                population.clear_pymunk_objects_from_memory()
                break
