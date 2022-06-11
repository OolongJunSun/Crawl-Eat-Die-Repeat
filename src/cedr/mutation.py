import random
from utils.encoding import hex_to_bin


class Mutator():
    def __init__(self, cfg) -> None:
        self.cfg = cfg

    def random_mutation(self, gene_pool: str) -> str:
        gene_bin = hex_to_bin(gene_pool)

        mutated_genes = []
        for base_pair in gene_bin:
            if random.uniform(0, 1) > self.cfg["mutation_rate"]:
                mutated_genes.append(base_pair)
            else:
                base_pair = str(int(not int(base_pair)))
                mutated_genes.append(base_pair) 

        mutated_genes = "".join(mutated_genes)

        mutated_genes = '%0*X' % ((len(mutated_genes) + 3) // 4, int(mutated_genes, 2))

        return mutated_genes