import random
import pygame
import pymunk
import numpy as np
import pymunk.pygame_util
from pymunk.vec2d import Vec2d



class Environment():
    def __init__(self, organism=None, draw=None) -> None:
        self.WIDTH, self.HEIGHT = 200, 200


        self.space = pymunk.Space()
        self.space.gravity = (0,0)
        self.fps = 60
        self.dt = 1/self.fps

        self.env_density = 50
        self.v_init = 2000
        self.particle_density = 2.8
        self.particle_radius = 4

        self.particles = []


        self.create_outer_boundaries()
        self.create_substrate()
        if organism:
            self.populate_environment(organism)

        handler = self.space.add_collision_handler(1,2)
        handler.pre_solve = self.wrap


        self.i = 0
        print(len(self.particles))

        if draw:
            self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

            self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
            self.draw_options.collision_point_color = (255, 255,255, 100)

            self.clock = pygame.time.Clock()

    def wrap(self, arbiter, space, data):
        if arbiter.shapes[0].body.position.x < 0:
            arbiter.shapes[0].body.position = (self.WIDTH, arbiter.shapes[0].body.position.y)
        elif arbiter.shapes[0].body.position.x > self.WIDTH:
            arbiter.shapes[0].body.position = (0, arbiter.shapes[0].body.position.y)
        elif arbiter.shapes[0].body.position.y > self.HEIGHT:
            arbiter.shapes[0].body.position = (arbiter.shapes[0].body.position.x, 0)
        elif arbiter.shapes[0].body.position.y < 0:
            arbiter.shapes[0].body.position = (arbiter.shapes[0].body.position.x, self.HEIGHT)   

        return True

    def draw(self):
        self.window.fill("white")
        self.space.debug_draw(self.draw_options)

        pygame.display.update()

    def obj_wrap(self, organism=None):
        for particle in self.particles:
            print(particle.position)
            if particle.position.x < 0:
                particle.position = (self.WIDTH, particle.position.y)
            elif particle.position.x > self.WIDTH:
                particle.position = (0, particle.position.y)
            elif particle.position.y > self.HEIGHT:
                particle.position = (particle.position.x, 0)
            elif particle.position.y < 0:
                particle.position = (particle.position.x, self.HEIGHT)

        if organism:
            if organism.body.head.matter.position.x < 0:
                organism.body.head.matter.position = (self.WIDTH, organism.body.head.matter.position.y)
                for part in organism.body.structure.values():
                    part["obj"].matter.position = (self.WIDTH, part["obj"].matter.position.y)
            elif organism.body.head.matter.position.x > self.WIDTH:
                for part in organism.body.structure.values():
                    part["obj"].matter.position = (0, part["obj"].matter.position.y)
                organism.body.head.matter.position = (0, organism.body.head.matter.position.y)
            elif organism.body.head.matter.position.y > self.HEIGHT:
                for part in organism.body.structure.values():
                    part["obj"].matter.position = (part["obj"].matter.position.x, 0)
                organism.body.head.matter.position = (organism.body.head.matter.position.x, 0)
            elif organism.body.head.matter.position.y < 0:
                for part in organism.body.structure.values():
                    part["obj"].matter.position = (part["obj"].matter.position.x, self.HEIGHT)
                organism.body.head.matter.position = (organism.body.head.matter.position.x, self.HEIGHT)


    def create_outer_boundaries(self):
        rects = [
            [(self.WIDTH/2, self.HEIGHT+self.particle_radius), (self.WIDTH, 1)],
            [(self.WIDTH/2, -self.particle_radius), (self.WIDTH, 1)],
            [(-self.particle_radius, self.HEIGHT/2), (1, self.HEIGHT)],
            [(self.WIDTH+self.particle_radius, self.HEIGHT/2), (1, self.HEIGHT)]
        ]

        for pos, size in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.collision_type = 2 
            shape.sensor = True
            self.space.add(body, shape)   

            shape.filter = pymunk.ShapeFilter(group=1)

    def create_substrate(self):
        x = np.linspace(
            self.particle_radius, 
            self.WIDTH-self.particle_radius, 
            self.env_density
        )

        y = np.linspace(
            self.particle_radius, 
            self.HEIGHT-self.particle_radius, 
            self.env_density
        )

        for i in x:
            for j in y:
                particle = pymunk.Body()
                particle.position = (i, j)

                shape = pymunk.Circle(particle, self.particle_radius) # 6 # 2.5
                shape.density = self.particle_density
                shape.elasticity = 0.999
                shape.friction = 0.02
                shape.color = (55, 210,255, 100)
                shape.collision_type = 1
                self.space.add(particle, shape)

                self.particles.append(particle)

                initial_impulse = Vec2d(
                    random.uniform(-self.v_init, self.v_init), 
                    random.uniform(-self.v_init, self.v_init)
                )
                pymunk.Body.update_velocity(particle, initial_impulse, 10, self.dt)    
            


    def populate_environment(self, organism):
        self.space.add(organism.body.head.matter, organism.body.head.shape)
        organism.body.head.shape.filter = pymunk.ShapeFilter(group=1)

        for i, part in enumerate(organism.body.structure.values()):
            if i == 0:
                self.space.add(part["obj"].matter, part["obj"].shape)
                part["obj"].shape.filter = pymunk.ShapeFilter(group=1)

                for joint in part["joints"]:
                    self.space.add(joint)
            else:
                self.space.add(part["obj"].matter, part["obj"].shape)
                part["obj"].shape.filter = pymunk.ShapeFilter(group=2)

                for joint in part["joints"]:
                    self.space.add(joint)