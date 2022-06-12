import uuid
import pymunk
from typing import Any, List, Dict, Union
from pymunk.vec2d import Vec2d
from dataclasses import dataclass
from pymunk.constraints import PinJoint, PivotJoint, RotaryLimitJoint, DampedRotarySpring, SimpleMotor

from phenotype import Head, Limb


@dataclass(unsafe_hash=True)
class BasicProtein():
    genome: str
    id: str

    def __post_init__(self) -> None:
        self.body = Body(self.genome)
        self.origin = Vec2d(392, 392)
        self.prev_position = self.origin
        self.fitness = 0

    def __repr__(self) -> str:
        return f'Individual(id={self.id})'

    def __str__(self) -> str:
        return f'Individual(id={self.id})'

    def calculate_fitness(self):
        # distance = abs(self.prev_position-self.body.head.matter.position)
        # direction = math.atan((p2[0]-p1[0])/(p2[1]-p1[1]))
        abs_distance = abs(self.prev_position-self.body.head.matter.position)
        distance_from_origin = abs(self.body.head.matter.position-self.origin)
        self.fitness += abs_distance * distance_from_origin

        self.prev_position = self.body.head.matter.position

    def update_energy(self):
        pass


class Body():
    def __init__(self, genome) -> None:
        self.head = Head(str(uuid.uuid4()))
        self.structure: Dict[str, Any] = {}
        self.body_parts: List[Limb] = []
        self.genes = genome.split(" ")

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

    def add_torso(self) -> None:
        depth = 0
        part = self.body_parts[0]

        self.torso_id = part.id

        p1 = Vec2d(-5,
                   0)

        p2 = Vec2d(5,
                   0)

        part.matter = None
        part.shape = None
        part.matter = pymunk.Body()
        part.shape = pymunk.Segment(
            part.matter,
            p1,
            p2,
            7
        )

        part.shape.density = 0.6
        part.shape.friction = 0.5
        part.shape.elasticity = 0.5
        part.shape.color = (0, 0, 0, 100)

        part.matter.position = self.head.matter.position

        p1 = Vec2d(392 - 16, 392)
        p2 = Vec2d(392 + 16, 392)

        endpoints = [p1, p2]

        joints = [PinJoint(part.matter, self.head.matter),
                  RotaryLimitJoint(part.matter, self.head.matter, 0, 0)]

        self.add_part_to_structure(part, joints, endpoints, None, self.head.id, depth)

    def add_limb(self, parent_id, part):
        parent = self.structure[parent_id]
        depth = parent["depth"] + 1

        if parent["parent"] == self.head.id:
            position = parent["endpoints"][part.side]
        else:
            position = parent["endpoints"][1]

        part.matter.position = Vec2d(position.x + part.v.x/2,
                                     position.y + part.v.y/2)

        p1 = position
        p2 = Vec2d(position.x + part.v.x, position.y + part.v.y)

        endpoints = [p1, p2]

        joints = self.create_joints(parent, part, p1)

        self.add_part_to_structure(part, joints, endpoints, part.side, parent_id, depth)

        parent["children"].append(part.id)

    def create_joints(
        self,
        parent,
        part,
        pos
    ) -> List[Union[PivotJoint, DampedRotarySpring, SimpleMotor]]:
        joints: List[Union[PivotJoint, DampedRotarySpring, SimpleMotor]] = []

        joints.append(
            PivotJoint(
                part.matter,
                parent["obj"].matter,
                pos
            )
        )

        if parent["parent"] == self.head.id:
            pass
        else:
            if part.spring:
                joints.append(
                    DampedRotarySpring(
                        part.matter,
                        parent["obj"].matter,
                        0,
                        part.spring_stiffness,
                        part.spring_damping
                    )
                )

            if part.motor:
                if part.motor_direction:
                    motor = SimpleMotor(
                        part.matter,
                        parent["obj"].matter,
                        -part.motor_speed
                    )
                else:
                    motor = SimpleMotor(
                        part.matter,
                        parent["obj"].matter,
                        part.motor_speed
                    )
                motor.max_force = part.motor_force
                joints.append(motor)

        return joints

    def add_part_to_structure(self, part, joints, endpoints, side, parent_id, depth) -> None:
        self.structure.update({
            part.id: {
                "obj": part,
                "joints": joints,
                "endpoints": endpoints,
                "side": side,
                "parent": parent_id,
                "children": [],
                "depth": depth
            }
        })

    def select_parent(self, part) -> str:
        side_filtered_dict = {k: v for k, v in self.structure.items() if v["side"] == part.side}

        if len(side_filtered_dict) > 0:
            parent_id = max(side_filtered_dict.items(), key=lambda x: x[1]['depth'])[0]
            max_depth = side_filtered_dict[parent_id]["depth"]
            depth_filtered_dict = {k: v for k, v in side_filtered_dict.items() if v["depth"] == min(max_depth, part.tree_index+1)}

            parent_id = min(depth_filtered_dict.items(), key=lambda x: (len(x[1]['children'])))[0]
        else:
            parent_id = self.torso_id

        return parent_id
