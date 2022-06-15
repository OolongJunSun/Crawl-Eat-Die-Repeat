import numpy as np
from typing import List, Tuple

class Selector():
    def __init__(self, cfg, seed) -> None:
        self.cfg = cfg
        self.methods = {
            "truncation": self.truncation
        }
        self.pairs_per_individual = int(1 / cfg["survival_rate"])
        self.rng = np.random.RandomState(seed)

    def form_pairs_randomly(self, individuals) -> List[Tuple]:
        pairs: List[Tuple] = []

        for _ in range(self.pairs_per_individual):
            indicies = self.rng.choice(
                len(individuals), 
                size=(len(individuals)//2, 2), 
                replace=False
            )

            pairs += [(individuals[idx[0]], individuals[idx[1]]) for idx in indicies]

        return pairs

    def truncation(self, individuals: List[str]) -> List[str]:
        n_breeders = int(len(individuals)*self.cfg["survival_rate"])

        # We always want an even number of breeding individuals
        if n_breeders % 2 != 0:
            n_breeders += 1

        return individuals[:n_breeders]
