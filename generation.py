import random
import uuid
from organism import Organism

class Cohort():
    def __init__(self, n_indiviuals) -> None:
        self.n_individuals = n_indiviuals

        self.cohort = {}

        self.gene_size = 4
        self.n_genes = 28
        self.genome_length = self.n_genes*self.gene_size

        gene_pool = self.initialize_genepool()

        self.cohort = self.generate_cohort(gene_pool)


    def initialize_genepool(self) -> str:
        gene_pool = '%012480x' % random.randrange(16**12480)
        gene_pool =  ' '.join(gene_pool[i:i+self.genome_length] for i in range(0, len(gene_pool), self.genome_length))
       
        return gene_pool

    def generate_cohort(self, gene_pool) -> dict:
        cohort = {}
        genomes = gene_pool.split(" ") 
        for genome in genomes:
            genes = ' '.join(genome[i:i+self.gene_size] for i in range(0, len(genome), self.gene_size))
            individual = Organism(genes, uuid.uuid4())
            cohort.update({
                individual: {
                    "fitness": 0,
                    "parents": None,
                    "genome": genome
                }
            })
        return cohort