import random
import pymunk
from dataclasses import dataclass

@dataclass
class Head():
    id: str

    def __hash__(self):
        return hash(self.id)

    def __post_init__(self) -> None:
        self.HEAD_POSITION = (256, 256)
        self.HEAD_MASS = 100
        self.HEAD_RADIUS = 15
        self.CONNECTION_POINTS = 8

        self.create()

        # for i in range(self.CONNECTION_POINTS):
        #     theta = int(i * (360 / self.CONNECTION_POINTS))
             
        #     print(theta)
            

    def create(self) -> None:
        self.matter = pymunk.Body()
        self.matter.position = self.HEAD_POSITION

        self.shape = pymunk.Circle(self.matter, self.HEAD_RADIUS)
        self.shape.mass = self.HEAD_MASS
        self.shape.color = (0, 0, 0, 100)


@dataclass
class Limb():
    gene: str
    id: str 
    v_x: int = 0
    v_y: int = 0
    radius: int = 0
    mass: int = 0

    def __hash__(self):
        return hash(self.id)

    def __post_init__(self):
        self.MAX_LENGTH = 32
        self.MAX_RADIUS = 3
        self.MAX_MASS = 50
        self.MIN_RADIUS = 1
        self.MIN_MASS = 10

        self.hex_to_bin()
        # print(self.gene_bin)
        self.decode_gene()
        self.create()
        
    def hex_to_bin(self) -> None:
        scale = 16  ## equals to hexadecimal
        n_bits = 4
        self.gene_bin = bin(int(self.gene, scale))[2:].zfill(len(self.gene) * n_bits)

    def normalize(self, char) -> float:
        return (int(char, 2) / 2 ** len(char))

    def scale(self, norm_value, max) -> int:
        return norm_value * max

    def decode_gene(self) -> None:
        v_x = self.gene_bin[:4]
        v_y = self.gene_bin[4:8]
        radius = self.gene_bin[8:10]
        mass = self.gene_bin[10:]

        self.v_x = self.scale(self.normalize(v_x), self.MAX_LENGTH)
        self.v_y = self.scale(self.normalize(v_y), self.MAX_LENGTH)

        # determine orientation of limb randomly for now.
        # in the future the orientation will be encoded in the gene
        x_direction = random.randint(0,1)
        y_direction = random.randint(0,1)
        
        if not x_direction:
            self.v_x = -self.v_x
        if not y_direction:
            self.v_y = -self.v_y

        self.radius = self.scale(self.normalize(radius), self.MAX_RADIUS)
        self.radius = int(max(self.MIN_RADIUS, self.radius))

        self.mass = self.scale(self.normalize(mass), self.MAX_MASS)
        self.mass = int(max(self.MIN_MASS, self.mass))
       
        # we nee to do this as a consequence of pymunks quirky
        # center of gravity calcs when creating segments
        # see: http://www.pymunk.org/en/latest/overview.html#center-of-gravity 
        self.end_1 = (int(-self.v_x/2), int(-self.v_y/2))
        self.end_2 = (int(self.v_x/2), int(self.v_y/2))
        

    def create(self) -> None:
        self.matter = pymunk.Body()
        # DONT INIT POSITION YET -> IT DEPENDS ON THE PARENT POS
            
        self.shape = pymunk.Segment(
            self.matter,
            self.end_1,
            self.end_2,
            self.radius
        )

        self.shape.mass = self.mass
        self.shape.color = (0,0,0,100)
