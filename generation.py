import random
import uuid
from organism import Organism

class Cohort():
    def __init__(self, n_indiviuals) -> None:
        self.cohort = {}
        self.cohort_size = n_indiviuals
        self.survival_rate = 0.5

        self.gene_size = 4
        self.n_genes = 21
        self.genome_length = self.n_genes*self.gene_size

        gene_pool = self.initialize_genepool(self.cohort_size)

        self.cohort = self.generate_cohort(gene_pool)


    def initialize_genepool(self, n_individuals) -> str:
        pool_size = int(n_individuals * self.n_genes * self.gene_size)
        gene_pool = f'%{pool_size}x' % random.randrange(16**pool_size)
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

    def selection(self) -> None:
        sorted_cohort = sorted(self.cohort.items(),key=lambda k_v: k_v[1]['fitness'])
        self.surviving_cohort = {}
        for idx, individual in enumerate(sorted_cohort[::-1]):
            print(individual)
            if idx >= int(self.cohort_size*self.survival_rate):
                break

            self.surviving_cohort.update({individual[0]: individual[1]})
        

    def reproduction(self) -> None:
        pass