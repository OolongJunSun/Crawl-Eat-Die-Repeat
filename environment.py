import random
import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

class Environment():
    def __init__(self) -> None:
        self.WIDTH, self.HEIGHT = 512, 512

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
        self.draw_options.collision_point_color = (255, 255,255, 100)
        self.space = pymunk.Space()
        self.space.gravity = (0,0)

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 1/self.fps

        self.particle_density = 15
        self.n_particles_x = int(self.WIDTH/self.particle_density) 
        self.n_particles_y = int(self.HEIGHT/self.particle_density)

        self.create_outer_boundaries()
        self.create_substrate()

    def draw(self):
        self.window.fill("white")
        self.space.debug_draw(self.draw_options)
        pygame.display.update()

    def create_outer_boundaries(self):
        rects = [
            [(self.WIDTH/2, self.HEIGHT-1), (self.WIDTH, 2)],
            [(self.WIDTH/2, 1), (self.WIDTH, 2)],
            [(1, self.HEIGHT/2), (2, self.HEIGHT)],
            [(self.WIDTH-1, self.HEIGHT/2), (2, self.HEIGHT)]
        ]

        for pos, size in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            self.space.add(body, shape)   

            shape.filter = pymunk.ShapeFilter(group=1)

    def create_substrate(self):
        for j in range(1,self.n_particles_y):
            for i in range(1,self.n_particles_x):
                particle = pymunk.Body()
                particle.position = (i*self.particle_density, j*self.particle_density)
                
                shape = pymunk.Circle(particle, 6)
                shape.density = 1
                shape.elasticity = 1
                shape.friction = 0.02
                shape.color = (55, 210,255, 100)
                self.space.add(particle, shape)

                pymunk.Body.update_velocity(particle, Vec2d(random.uniform(-1000, 1000), random.uniform(-2000, 2000)), 10, self.dt)