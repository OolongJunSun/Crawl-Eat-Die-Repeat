import numpy as np


class MatchMaker():
    def __init__(self) -> None:
        pass

    def form_breeding_pairs(self, individuals):
        indicies = np.random.choice(len(individuals), size=(len(individuals)//2, 2), replace=False)

        return [[individuals[idx[0]], individuals[idx[1]]] for idx in indicies]
