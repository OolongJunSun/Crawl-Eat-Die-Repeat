import math
import pymunk
from pymunk.vec2d import Vec2d
from dataclasses import dataclass


class Organ():
    def hex_to_bin(self) -> None:
        scale = 16  ## equals to hexadecimal
        n_bits = 4
        self.gene_bin = bin(int(self.gene, scale))[2:].zfill(len(self.gene) * n_bits)

    def normalize(self, char) -> float:
        return (int(char, 2) / 2 ** len(char))

    def scale(self, norm_value, MAX, MIN) -> float:
        return max(MIN, norm_value * MAX)


@dataclass
class Head(Organ):
    id: str

    def __post_init__(self) -> None:
        self.HEAD_POSITION = (256, 256)
        self.DENSITY = 3
        self.HEAD_RADIUS = 12

        self.create()
            
    def create(self) -> None:
        self.matter = pymunk.Body()
        self.matter.position = self.HEAD_POSITION

        self.shape = pymunk.Circle(self.matter, self.HEAD_RADIUS)
        self.shape.density = self.DENSITY
        self.shape.color = (0, 0, 0, 100)


@dataclass
class Limb(Organ):
    gene: str
    id: str 

    def __post_init__(self):
        self.MAX_LENGTH = 24
        self.MIN_LENGTH = 4
        self.MAX_RADIUS = 5
        self.MIN_RADIUS = 2
        self.DENSITY = 1.2
        self.FRICTION = 0.5

        self.hex_to_bin()
        self.decode_gene()
        self.create()

    def decode_gene(self) -> None:
        v_x = self.gene_bin[:4]
        v_y = self.gene_bin[4:8]
        radius = self.gene_bin[8:10]
        flip_x = int(self.gene_bin[10])
        flip_y = int(self.gene_bin[11])
        self.rotary_lim = int(self.gene_bin[12])
        self.motor = int(self.gene_bin[13:15], 2)
        # self.pin = int(self.gene_bin[14])
        self.side = int(self.gene_bin[15]) # left = 0, right = 1

        # self.pin_selector = int(self.gene_bin[2:6])
        

        v_x = self.scale(
            self.normalize(v_x), 
            self.MAX_LENGTH,
            self.MIN_LENGTH
        )
        v_y = self.scale(
            self.normalize(v_y),
            self.MAX_LENGTH,
            self.MIN_LENGTH
        )

        if flip_x:
            v_x = -v_x
        if flip_y:
            v_y = -v_y

        self.v = Vec2d(v_x, v_y)
        
        self.radius = self.scale(
            self.normalize(radius),
            self.MAX_RADIUS,
            self.MIN_RADIUS
        )
       
        # we nee to do this as a consequence of pymunks quirky
        # center of gravity calcs when creating segments
        # see: http://www.pymunk.org/en/latest/overview.html#center-of-gravity 
        self.end_1 = (-v_x/2, -v_y/2)
        self.end_2 = (v_x/2, v_y/2)
        
    def create(self) -> None:
        self.matter = pymunk.Body()
        # DONT INIT POSITION YET -> IT DEPENDS ON THE PARENT POS
            
        self.shape = pymunk.Segment(
            self.matter,
            self.end_1,
            self.end_2,
            self.radius
        )

        self.shape.density = self.DENSITY
        self.shape.friction = self.FRICTION
        self.shape.elasticity = 0
        self.shape.color = (0,0,0,100)


@dataclass
class Hand():
    gene: str
    id: str
    grip_strength: float = 0
    endurance: float = 0
    speed: float = 0


