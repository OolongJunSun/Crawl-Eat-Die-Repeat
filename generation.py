import random
import uuid
from organism import Organism

class Cohort():
    def __init__(self, n_indiviuals, surviving_genes) -> None:
        self.gene_size = 6
        self.n_genes = 13
        self.genome_length = int(self.n_genes*self.gene_size)

        self.cohort = {}
        self.cohort_size = n_indiviuals
        self.survival_rate = 0.20
        self.mutation_rate = 0.01 / (self.gene_size * self.n_genes)
        self.n_elite = 6

        self.gene_pool = self.initialize_genepool(self.cohort_size, surviving_genes)

        self.cohort = self.generate_cohort(self.gene_pool)


    def initialize_genepool(self, n_individuals, surviving_genes="") -> str:
        gene_length = len(surviving_genes)

        pool_size = int(n_individuals * self.n_genes * self.gene_size - gene_length)
        gene_pool = f'%0{pool_size}x' % random.randrange(int(16**pool_size))
        gene_pool = surviving_genes + gene_pool
        gene_pool =  ' '.join(gene_pool[i:i+self.genome_length] for i in range(0, len(gene_pool), self.genome_length))
        
        return gene_pool

    def generate_cohort(self, gene_pool) -> dict:
        cohort = {}
        genomes = gene_pool.split(" ") 
        for genome in genomes:
            print(genome)
            genes = ' '.join(genome[i:i+self.gene_size] for i in range(0, len(genome), self.gene_size))
            print(genes)
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
        
        self.reproducing_individuals = []
        for idx, individual in enumerate(sorted_cohort[::-1]):
            if idx >= int(self.cohort_size*self.survival_rate):
                break

            self.reproducing_individuals.append(individual)  

        self.elite_individuals = self.reproducing_individuals[0:self.n_elite]

        
    def reproduction(self) -> None:
        breeding_pair = []
        children = []

        for _ in range(int(1/self.survival_rate)):
            random.shuffle(self.reproducing_individuals)
            for idx, individual in enumerate(self.reproducing_individuals):
                metrics = individual[1]
                genome = metrics["genome"]

                breeding_pair.append(genome)
                if (idx+1) % 2 == 0:
                    k = random.randint(1,2)
                    child_1, child_2 = self.k_point_crossover(k, breeding_pair, 2)
                    children.append(child_1)
                    children.append(child_2)
                    breeding_pair = []

        # elistism
        surviving_gene_pool = surviving_gene_pool + self.elite_individuals
        
        surviving_gene_pool = "".join(children)

        surviving_gene_pool = self.mutate(surviving_gene_pool)

        return surviving_gene_pool


    def k_point_crossover(self, k, breeding_pair, n_offspring):
        crossover_points = [0]
        for _ in range(k):
            point = random.randint(1, self.n_genes-1) * 4
            crossover_points.append(int(point))

        crossover_points = sorted(set(crossover_points))

        gene_1 = breeding_pair[0]
        gene_2 = breeding_pair[1]

        parts_1 = [gene_1[i:j] for i,j in zip(crossover_points, crossover_points[1:]+[None])]
        parts_2 = [gene_2[i:j] for i,j in zip(crossover_points, crossover_points[1:]+[None])]

        offspring_1 = []
        offspring_2 = []
        for idx, p1, p2 in enumerate(zip(parts_1, parts_2)):
            if idx % 2 == 0:
                offspring_1.append(p2)
                offspring_2.append(p1)
            else:
                offspring_1.append(p1)
                offspring_2.append(p2)
        
        offspring_1 = "".join(offspring_1)
        offspring_2 = "".join(offspring_2)

        return offspring_1, offspring_2

    def mutation(self, gene_pool):
        i = random.uniform(0, 1)

        print(gene_pool)
        scale = 16  ## equals to hexadecimal
        n_bits = 4
        gene_bin = bin(int(gene_pool, scale))[2:].zfill(len(gene_pool) * n_bits)
        print(gene_bin)
        mutated_genes = [
            base_pair if i > self.mutation_rate else hex(int(base_pair, 16) + 1) \
            for base_pair in gene_pool
        ]

        return mutated_genes


