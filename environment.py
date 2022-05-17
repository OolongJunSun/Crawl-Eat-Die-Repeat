import pygame
import pymunk
import pymunk.pygame_util

class Environment():
    def __init__(self) -> None:
        self.WIDTH, self.HEIGHT = 512, 512

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
        self.draw_options.collision_point_color = (255, 255,255, 100)
        self.space = pymunk.Space()
        self.space.gravity = (0,0)

        self.clock = pygame.time.Clock()
        self.fps = 30
        self.dt = 1/self.fps

        self.particle_density = 16
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
        for j in range(self.n_particles_y):
            for i in range(self.n_particles_x):
                if ((i > int(192/self.particle_density) and 
                    j > int(192/self.particle_density) and 
                    i < int(304/self.particle_density) and 
                    j < int(304/self.particle_density)) or
                    i == 0 or j == 0 or 
                    i == self.WIDTH/self.particle_density or 
                    j == self.WIDTH/self.particle_density):
                    continue
                else:
                    particle = pymunk.Body()
                    particle.position = (i*self.particle_density, j*self.particle_density)
                    shape = pymunk.Circle(particle, 8.1)
                    shape.density = 0.5
                    shape.elasticity = 0.99
                    shape.color = (200, 200,255, 100)
                    self.space.add(particle, shape)