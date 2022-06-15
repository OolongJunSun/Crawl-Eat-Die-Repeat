import random
from utils.encoding import hex_to_bin


class Mutator():
    def __init__(self, cfg, seed) -> None:
        self.cfg = cfg
        self.rng = random.Random(seed)

    def random_mutation(self, gene_pool: str) -> str:
        gene_bin = hex_to_bin(gene_pool)

        mutated_genes = [str(int(not int(base_pair))) if self.rng.random() < self.cfg["mutation_rate"] else base_pair
                         for base_pair in gene_bin]

        mutated_genes = "".join(mutated_genes)
        mutated_genes = '%0*X' % ((len(mutated_genes) + 3) // 4, int(mutated_genes, 2))
        return mutated_genes