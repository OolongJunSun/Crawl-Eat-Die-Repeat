import numpy as np
from typing import Any, Dict, List
from cedr.utils.encoding import hex_to_bin

class Metrics():
    def __init__(self) -> None:
        self.runs = {}
        self.run_stats = {}
        self.generation_stats: Dict[str, Any] = {}

    def update_hall_of_fame(self):
        pass

    def mean_fitness(self, fitnesses: List[float]) -> None:
        self.generation_stats.update(
            {
                "mean_fitness": sum(fitnesses) / len(fitnesses)
            }
        )

    def median_fitness(self, fitnesses: List[float]) -> None:
        self.generation_stats.update(
            {
                "median_fitness": fitnesses[len(fitnesses)//2]
            }
        )

    def cutoff_fitness(self, fitnesses: List[float], survival_rate: float) -> None:
        cutoff_idx = int(len(fitnesses) * survival_rate)

        self.generation_stats.update(
            {
                "cutoff_fitness": fitnesses[cutoff_idx]
            }
        )

    def population_diversity(self, genomes: List[str]) -> None:        
        genomes = [genome.replace(" ", "") for genome in genomes]
        binary_genes = [np.fromstring(hex_to_bin(genome[7:]),'u1') - ord('0') for genome in genomes]

        diversity_list = [
            np.sum([np.count_nonzero(base_genome!=comparison_genome) for base_genome in binary_genes]) / len(genomes)
            for comparison_genome in binary_genes
        ]
        self.diversity_list = diversity_list 

    def mean_diversity(self) -> None:
        self.generation_stats.update(
            {
                "mean_diversity": sum(self.diversity_list) / len(self.diversity_list)
            }
        )

    def update_run_stats(self, key: str) -> None:
        self.run_stats.update(
            {
               key: {
                   "mean_fitness": self.generation_stats['mean_fitness'],
                   "median_fitness": self.generation_stats['median_fitness'],
                   "cutoff_fitness": self.generation_stats['cutoff_fitness'],
                   "mean_diversity": self.generation_stats['mean_diversity'],
                   'diversity': self.diversity_list
               }
            }
        )

    def add_to_runs(self, key: str) -> None:
        self.runs.update({
            key: self.run_stats
        })
        self.run_stats = {}
