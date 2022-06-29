import random
from typing import List, Tuple


class Reproducer():
    def __init__(self, cfg, cohort) -> None:
        self.cfg = cfg
        self.methods = {
            "n-point": self.n_point_crossover
        }
        self.cohort = cohort
        self.rng = random.Random(cfg['seed'])

    def single_point_crossover(self, pair: Tuple[str]) -> List[str]:
        assert len(pair[0]) == len(pair[1])

        alleles_1 = pair[0].split(" ")
        alleles_2 = pair[1].split(" ")

        position = self.rng.randint(1, len(alleles_1)- 1)

        offspring_1_alleles = alleles_1[:position] + alleles_2[position:]
        offspring_2_alleles = alleles_2[:position] + alleles_1[position:]
        
        offspring_1 = "".join(offspring_1_alleles)
        offspring_2 = "".join(offspring_2_alleles)

        assert len(offspring_1) == len(offspring_2)

        return offspring_1, offspring_2

    def n_point_crossover(self):
        pass