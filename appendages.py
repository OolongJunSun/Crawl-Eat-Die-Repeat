import math
import random
import pymunk
from dataclasses import dataclass


class Organ():
    def hex_to_bin(self) -> None:
        scale = 16  ## equals to hexadecimal
        n_bits = 4
        self.gene_bin = bin(int(self.gene, scale))[2:].zfill(len(self.gene) * n_bits)

    def normalize(self, char) -> float:
        return (int(char, 2) / 2 ** len(char))

    def scale(self, norm_value, MAX, MIN) -> int:
        return max(MIN, norm_value * MAX)

@dataclass
class Head(Organ):
    id: str
    HEAD_POSITION: tuple = (256, 256)
    HEAD_MASS: int = 1000
    HEAD_RADIUS: int = 10
    CONNECTION_POINTS: int = 8

    def __post_init__(self) -> None:
        self.create()
            
    def create(self) -> None:
        self.matter = pymunk.Body()
        self.matter.position = self.HEAD_POSITION

        self.shape = pymunk.Circle(self.matter, self.HEAD_RADIUS)
        self.shape.mass = self.HEAD_MASS
        self.shape.color = (0, 0, 0, 100)

@dataclass
class Limb(Organ):
    gene: str
    id: str 
    MAX_LENGTH: int = 48
    MIN_LENGTH: int = 12
    MAX_RADIUS: int = 4
    MIN_RADIUS: int = 1

    def __post_init__(self):
        self.hex_to_bin()
        self.decode_gene()
        self.create()

    def decode_gene(self) -> None:
        v_x = self.gene_bin[:4]
        v_y = self.gene_bin[4:8]
        radius = self.gene_bin[8:10]
        x_direction = self.gene_bin[10]
        y_direction = self.gene_bin[11]

        self.v_x = self.scale(
            self.normalize(v_x), 
            self.MAX_LENGTH,
            self.MIN_LENGTH
        )
        self.v_y = self.scale(
            self.normalize(v_y),
            self.MAX_LENGTH,
            self.MIN_LENGTH
        )

        if not x_direction:
            self.v_x = -self.v_x
        if not y_direction:
            self.v_y = -self.v_y

        self.radius = self.scale(
            self.normalize(radius),
            self.MAX_RADIUS,
            self.MIN_RADIUS
        )

        length = math.sqrt(self.v_x**2 + self.v_y**2)
        self.mass = int(self.radius*length)
       
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


@dataclass
class Hand(Organ):
    gene: str
    id: str
    grip_strength: float = 0
    endurance: float = 0
    speed: float = 0

    
