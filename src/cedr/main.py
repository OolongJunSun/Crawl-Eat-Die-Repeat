import time
import json
import random
import faulthandler
import multiprocessing
from itertools import repeat
from operator import itemgetter
from environment import SimpleHabitat
from geneaology import History
from population import Population
from selection import Selector
from reproduction import MatchMaker


def start_process():
    print('Starting', multiprocessing.current_process().name)


def evaluate_individual(cfg, seed, individual):
    individual = individual["instance"]

    start = time.perf_counter()

    env = SimpleHabitat(cfg, seed, individual)

    n_steps = env.fps * 60
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

    species = History()
    species.make_output_dir()

    # Initialise population
    #   a) Randomly initialise
    population = Population(cfg["gene_pool"])
    population.init_gene_pool()
    population.individuate_genomes()
    population.generate_individuals()

    #   b) Load from checkpoint
    #   ADD THIS

    selection = Selector(cfg["selection"])
    matcher = MatchMaker()

    pool = multiprocessing.Pool(initializer=start_process)

    for generation in range(cfg["species"]["n_generations"]):
        species.make_output_dir(generation)

        seed = random.randint(0, 100000)

        results = pool.starmap(
            evaluate_individual,
            zip(repeat(cfg["environment"]), repeat(seed), population.cohort.values())
        )

        # Sort individuals by descending fitness
        results.sort(key=itemgetter(1), reverse=True)

        breeding_individuals = selection.methods[cfg["selection"]["method"]](results)

        breeding_pairs = matcher.form_breeding_pairs()

        # We need to do this to avoid segfaults when multiprocessing
        population.clear_pymunk_objects_from_memory()
