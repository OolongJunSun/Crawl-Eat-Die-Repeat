import os
from typing import Dict, List
from collections import namedtuple
# from data_manager import load_population

class Analyzer():
    def __init__(self) -> None:
        self.population = []
        self.populations = {}
        # self.population_counter = 0

        columns = ['fitness', 'genome']
        self.population_columns = namedtuple("Columns", " ".join(columns))

    """
        Load a population into the classes storage dictionary -> self.populations
    """
    def load_population(self, path, pop_counter):
        self.population = []
        
        with open(path, 'r') as f:
            lines = f.readlines()

        genomes = [line.split("-")[1][1:].strip() for line in lines]
        fitnesses = [line.split("-")[0][:-1] for line in lines]

        for fitness, genome in zip(fitnesses, genomes):
            self.population.append(self.population_columns(fitness, genome)) 
         

        self.populations.update({
            f"population-{pop_counter}": self.population
        })

    def remove_population(self, pop_id):
        pass

    """
        Calculate the diversity of the two populations individual by individual
        i.e.
            pop_a = ["abcd", "efgh", "1234"]
            pop_b = ["wxyz", "4567", "2727"]

            [diversity(i_pa, i_pb) for i_pa in pop_b for i_pb in pop_b]
    """
    def get_interpopulation_diversity(self, pop_a: List[str], pop_b: List[str]) -> float:
        pass

    """"
        Calculate how many schemata of order x there are in each population.
        Only consider schemata with at least min_inst instances. 

        returns dict w/ schemata representation + number of instances
        i.e.

    """
    def count_schemata_of_order_x(self, pop_id: str, x: int, min_inst: int) -> Dict[str, int]:
        pass

    def get_schemata_diversity(self, pop_id: str):
        pass

