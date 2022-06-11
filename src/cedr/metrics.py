import numpy as np
from typing import Any, Dict, List
from utils.encoding import hex_to_bin

class Metrics():
    def __init__(self) -> None:
        self.run_stats: Dict[str, Dict[str, Any]] = {}
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
        genomes.sort()

        print(genomes)
        genomes = [genome.replace(" ", "") for genome in genomes]
        binary_genes = [np.fromstring(hex_to_bin(genome),'u1') - ord('0') for genome in genomes]

        diversity_list = [
            np.sum([np.count_nonzero(base_genome!=comparison_genome) for base_genome in binary_genes]) / len(genomes)
            for comparison_genome in binary_genes
        ]
        print(diversity_list)
        self.diversity_list = diversity_list 

    def population_mean_diversity(self) -> None:
        self.generation_stats.update(
            {
                "population_diversity": sum(self.diversity_list)
            }
        )

    def update_run_stats(self, n: int) -> None:
        self.run_stats.update(
            {
                f"generation{n}": self.generation_stats
            }
        )