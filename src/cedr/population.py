
import uuid
import random
from individual import BasicProtein


class Population():
    def __init__(self, cfg) -> None:
        self.cfg = {}
        for key in cfg:
            self.cfg.update({key: cfg[key]})

    def init_gene_pool(self) -> None:
        pool_length = self.cfg["n_individuals"] * self.cfg["n_alleles"] * self.cfg["allele_length"]

        if isinstance(self.cfg["seed"], int):
            random.seed(self.cfg["seed"])

        self.gene_pool = f'%0{pool_length}x' % random.randrange(int(16**pool_length))

    def individuate_genomes(self) -> None:
        genome_length = self.cfg["n_alleles"] * self.cfg["allele_length"]

        self.genomes = [self.gene_pool[i:i+genome_length] for i in range(0, len(self.gene_pool), genome_length)]

    def generate_individuals(self) -> None:
        self.cohort = {}

        for genome in self.genomes:
            genes = ' '.join(genome[i:i+self.cfg["allele_length"]] for i in range(0, len(genome), self.cfg["allele_length"]))

            individual = BasicProtein(genes, str(uuid.uuid4()))

            self.cohort.update({
                individual.id: {
                    "instance": individual,
                    "fitness": 0,
                    "genome": genes
                }
            })

    def clear_pymunk_objects_from_memory(self):
        for individual in self.cohort.values():
            for limb in individual["instance"].body.structure.values():
                del limb["obj"].matter  # = None
                del limb["obj"].shape  # = None
                for joint in limb["joints"]:
                    del joint  # = None
