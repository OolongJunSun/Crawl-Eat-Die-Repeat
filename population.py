
import uuid
import random
from organism import Organism

class Population():
    def __init__(self, n_individuals) -> None:
        self.n_individuals = n_individuals
        self.gene_size = 7
        self.n_genes = 9
        self.genome_length = int(self.n_genes*self.gene_size)

        self.cohort = {}
        self.survival_rate = 0.20
        self.mutation_rate = 0.01
        self.elite_rate = 0.002
        self.n_elite = int(self.elite_rate * self.n_individuals)


    """
        returns a space delimited string of hexadecimal digits
    """
    def initialize_genepool(self, surviving_genes="") -> str:
        gene_length = len(surviving_genes)
        pool_size = int(self.n_individuals * self.n_genes * self.gene_size - gene_length)
        
        gene_pool = f'%0{pool_size}x' % random.randrange(int(16**pool_size))
        gene_pool = surviving_genes + gene_pool

        return ' '.join(gene_pool[i:i+self.genome_length] for i in range(0, len(gene_pool), self.genome_length))
        


    def divide_genepool(self, gene_pool):
        return ' '.join(gene_pool[i:i+self.genome_length] for i in range(0, len(gene_pool), self.genome_length))
         

    def generate_individuals(self, gene_pool) -> None:
        self.cohort = {}
        genomes = gene_pool.split(" ") 

        for genome in genomes:
            genes = ' '.join(genome[i:i+self.gene_size] for i in range(0, len(genome), self.gene_size))
            individual = Organism(genes, uuid.uuid4())
            self.cohort.update({
                individual.id: {
                    "instance": individual,
                    "fitness": 0,
                    # "parents": None,
                    "genome": genes
                }
            })    


    def selection(self) -> None:
        sorted_cohort = sorted(self.cohort.items(),key=lambda k_v: k_v[1]['fitness'])
        self.reproducing_individuals = []
        n_fit_individuals = int(self.n_individuals*self.survival_rate)
        idx = self.n_individuals - n_fit_individuals - 1

        for individual in sorted_cohort[:idx:-1]:
            self.reproducing_individuals.append(individual)  

        elite_individuals = self.reproducing_individuals[0:self.n_elite]

        self.elite_genes = ""
        for individual in elite_individuals:
            self.elite_genes += " ".join(individual[1]["genome"]).strip("\n").replace(" ","")

        
    def reproduction(self) -> None:
        breeding_pair = []
        children = []

        for _ in range(int(1/self.survival_rate)-1):
            random.shuffle(self.reproducing_individuals)
            for idx, individual in enumerate(self.reproducing_individuals):
                metrics = individual[1]
                genome = metrics["genome"]

                breeding_pair.append(genome)
                if (idx+1) % 2 == 0:
                    k = random.randint(1,2)
                    child_1, child_2 = self.k_point_crossover(k, breeding_pair, 2)
                    children.append(child_1.replace(" ",""))
                    children.append(child_2.replace(" ",""))
                    breeding_pair = []

        # elistism <- replace 15 of new generation with elites
        # surviving_gene_pool = "".join(children[:-self.n_elite]) + self.elite_genes
        surviving_gene_pool = "".join(children) + self.elite_genes
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
        for idx, (p1, p2) in enumerate(zip(parts_1, parts_2)):
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
        scale = 16  
        n_bits = 4
        gene_bin = bin(int(gene_pool, scale))[2:].zfill(len(gene_pool) * n_bits)

        mutated_genes = []
        for base_pair in gene_bin:

            if random.uniform(0, 1) > self.mutation_rate:
                mutated_genes.append(base_pair)
            else:
                base_pair = str(int(not int(base_pair)))
                mutated_genes.append(base_pair) 

        mutated_genes = "".join(mutated_genes)
        mutated_genes = '%0*X' % ((len(mutated_genes) + 3) // 4, int(mutated_genes, 2))
        return mutated_genes