import math
import uuid
import pymunk
from pymunk.vec2d import Vec2d
from dataclasses import dataclass
from appendages import Head, Limb


@dataclass(unsafe_hash=True)
class Organism():
    genes: str
    id: str

    def __post_init__(self) -> None:
        self.body = Body(self.genes, self.id)
        self.origin = Vec2d(0,0)
        self.prev_position = self.origin
        self.fitness = 0

    def __repr__(self) -> str:
        return f'Organism(id={self.id})'

    def __str__(self) -> str:
        return f'Organism(id={self.id})'
        
    def calculate_fitness(self):
        # distance = abs(self.prev_position-self.body.head.matter.position)
        # direction = math.atan((p2[0]-p1[0])/(p2[1]-p1[1]))
        abs_distance = abs(self.prev_position-self.body.head.matter.position)
        # distance_from_origin = abs(self.body.head.matter.position-self.origin)
        self.fitness += abs_distance
        # self.fitness += (abs_distance * distance_from_origin**2) / 10000
        
        self.prev_position = self.body.head.matter.position

    def update_energy(self):
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

    def add_torso(self) -> None:
        depth = 0
        part = self.body_parts[0]


        self.torso_id = part.id


        part.matter = None
        part.shape = None

        p1 = Vec2d(-5,
                   0)

        p2 = Vec2d(5,
                   0)

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
        part.shape.color = (0,0,0,100)

        part.matter.position = self.head.matter.position

        p1 = Vec2d(384-16,
                   384)

        p2 = Vec2d(384+16,
                   384)

        endpoints = [p1,p2]
        # # we always want the endpoint at index 0 to be on lhs of y axis 
        # if p1.x < 0:
        #     endpoints = [p1,p2]
        # else:
        #     endpoints = [p2,p1]

        joints = [pymunk.constraints.PinJoint(part.matter, self.head.matter),
                  pymunk.constraints.RotaryLimitJoint(part.matter, self.head.matter, 0,0)]

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

    def create_joints(self, parent, part, pos) -> pymunk.Constraint:
        joints = []
        joints.append(
            pymunk.constraints.PivotJoint(
                part.matter,
                parent["obj"].matter, 
                pos
            )
        )

        if parent["parent"] == self.head.id:
            pass
        else: 
            if part.joint_mechanics >= 2:
                joints.append(
                    pymunk.constraints.DampedRotarySpring(
                        part.matter, 
                        parent["obj"].matter, 
                        0, 
                        part.spring_stiffness, 
                        part.spring_damping
                    )
                )

            if part.joint_mechanics == 1 or part.joint_mechanics == 3:    
                if part.motor_direction == 0:
                    motor = pymunk.constraints.SimpleMotor(
                        part.matter, 
                        parent["obj"].matter, 
                        -part.motor_speed
                    )
                else:
                    motor = pymunk.constraints.SimpleMotor(
                        part.matter, 
                        parent["obj"].matter, 
                        part.motor_speed
                    )
                motor.max_force = part.motor_force
                joints.append(motor)

        return joints

    def add_part_to_structure(self, part, joints, endpoints, side, parent_id, depth) -> None:
        #add depth
        self.structure.update({
            part.id: {
                "obj": part,
                "joints": joints,
                "endpoints": endpoints,
                "side": side,
                "parent": parent_id,
                "children": [],
                "depth" : depth
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