import pygame
import pymunk
import numpy as np
import pymunk.pygame_util
from pymunk.vec2d import Vec2d


class SimpleHabitat():
    def __init__(self, cfg, seed, individual=None, draw=False) -> None:
        self.WIDTH, self.HEIGHT = cfg["width"], cfg["height"]

        self.space = pymunk.Space()
        self.space.gravity = (cfg["gravity_x"], cfg["gravity_y"])
        self.fps = cfg["FPS"]
        self.dt = 1/self.fps

        self.substrate_density = cfg["substrate_density"]
        self.particle_density = cfg["particle_density"]
        self.particle_radius = cfg["particle_radius"]
        self.v_init = cfg["particle_velocity"]

        self.particles = []

        self.create_outer_boundaries()
        self.create_substrate(seed)
        if individual:
            self.populate_environment(individual)

        handler = self.space.add_collision_handler(1, 2)
        handler.pre_solve = self.wrap

        if draw:
            self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

            self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
            self.draw_options.collision_point_color = (255, 255, 255, 100)

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

    def create_substrate(self, seed):
        x = np.linspace(
            self.particle_radius,
            self.WIDTH-self.particle_radius,
            self.substrate_density
        )

        y = np.linspace(
            self.particle_radius,
            self.HEIGHT-self.particle_radius,
            self.substrate_density
        )

        rng = np.random.RandomState(seed)
        v = rng.random((2, np.size(x), np.size(y)))
        v = v - 0.5

        for n, i in enumerate(x):
            for m, j in enumerate(y):
                if (i > 314 and i < 454) and (j > 314 and j < 454):
                    continue

                particle = pymunk.Body()
                particle.position = (i, j)

                shape = pymunk.Circle(particle, self.particle_radius)   # 6 # 2.5
                shape.density = self.particle_density
                shape.elasticity = 1
                shape.friction = 0.01
                shape.color = (55, 210, 255, 100)
                shape.collision_type = 1
                self.space.add(particle, shape)

                self.particles.append(particle)

                initial_impulse = Vec2d(
                    v[0][n][m] * self.v_init,
                    v[1][n][m] * self.v_init
                )

                pymunk.Body.update_velocity(particle, initial_impulse, 10, self.dt)

    def populate_environment(self, individual):
        self.space.add(individual.body.head.matter, individual.body.head.shape)
        individual.body.head.shape.filter = pymunk.ShapeFilter(group=1)

        for i, part in enumerate(individual.body.structure.values()):
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
