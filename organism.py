
import math
import uuid
import random
import pymunk
from typing import List
from pymunk.vec2d import Vec2d
from dataclasses import dataclass
from appendages import Head, Limb


class Organism():
    def __init__(self, genome="") -> None:
        self.id = uuid.uuid4()
        self.genome = genome

        self.body = Body(genome, self.id)
        # self.mind = Mind(genome, self.id)

    def fitness(self):
        pass

    def select_partner(self):
        pass

    def some_kind_of_controller(self):
        pass


@dataclass        
class Body():
    genome: str
    id: str
    
    def __post_init__(self):
        self.head = Head(str(uuid.uuid4()))
        self.structure = {}
        self.body_parts = []
        self.genes = self.genome.split(" ")

        self.generate_limbs()
        self.design_body()


    def generate_limbs(self) -> None:
        for gene in self.genes:
            limb = Limb(gene, str(uuid.uuid4()))
            self.body_parts.append(limb)

    def design_body(self) -> None:
        self.add_torso()
        for part in self.body_parts[1:]:
            parent_id = self.select_parent(part)
            self.add_limb(parent_id, part)

        #     if isinstance(self.structure[parent_id]["obj"], Head):
        #         self.add_torso()
        #     else:
        #         self.add_limb(parent_id, part)

    def add_torso(self) -> None:
        part = self.body_parts[0]
        part.matter.position = self.head.matter.position
        
        p1 = Vec2d(part.matter.position[0] + part.end_1[0],
                   part.matter.position[1] + part.end_1[1])

        p2 = Vec2d(part.matter.position[0] + part.end_2[0],
                   part.matter.position[1] + part.end_2[1])

        # we always want the endpoint at index 0 to be on lhs of y axis 
        if p1.x < 0:
            endpoints = [p1,p2]
        else:
            endpoints = [p2,p1]

        joints = [pymunk.constraints.PinJoint(part.matter, self.head.matter),
                  pymunk.constraints.RotaryLimitJoint(part.matter, self.head.matter, 0,0)]

        self.add_part_to_structure(part, joints, endpoints, None, self.head.id)

    def add_limb(self, parent_id, part):
        parent = self.structure[parent_id]

        if parent["parent"] == self.head.id:
            position = parent["endpoints"][part.side]
        else:
            position = parent["endpoints"][1]

        part.matter.position = Vec2d(position.x + part.v.x/2,
                                     position.y + part.v.y/2)

        p1 = position
        p2 = Vec2d(position.x + part.v.x, position.y + part.v.y)

        endpoints = [p1, p2]

        print(endpoints)

        joints = self.create_joints(parent, part, p1)

        self.add_part_to_structure(part, joints, endpoints, part.side, parent_id)
        
        parent["children"].append(part.id)

    def create_joints(self, parent, part, p) -> pymunk.Constraint:
        joints = []
        joints.append(
                pymunk.constraints.PivotJoint(part.matter, parent["obj"].matter, p)
        )

        if part.rotary_lim:
            joints.append(pymunk.constraints.DampedRotarySpring(
                part.matter, parent["obj"].matter, math.pi/4, 10000, 100)
            )

        if part.motor:
            motor = pymunk.constraints.SimpleMotor(part.matter, parent["obj"].matter, 30000000000000000)
            motor.max_force = 500000
            joints.append(
               motor
            )

        return joints

    def add_part_to_structure(self, part, joints, endpoints, side, parent_id) -> None:
        self.structure.update({
            part.id: {
                "obj": part,
                "joints": joints,
                "endpoints": endpoints,
                "side": side,
                "parent": parent_id,
                "children": []
            }
        })

    def select_parent(self, part) -> str:
        parent_id = random.choice(list(self.structure))

        # we want to make sure that the parts we are connection are
        # of the same side. since the torso is in the middle we ignore it
        if self.structure[parent_id]["side"] != None:
            if part.side != self.structure[parent_id]["side"]:
                parent_id = self.select_parent(part)  

        # torso can have up to 4 children
        if self.structure[parent_id]["side"] == None and len(self.structure[parent_id]["children"]) < 3:
            pass 
        elif len(self.structure[parent_id]["children"]) >= 2:
            parent_id = self.select_parent(part)
        
        return parent_id   