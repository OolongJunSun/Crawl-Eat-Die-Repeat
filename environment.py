import random
import pygame
import pygame.freetype
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

class Environment():
    def __init__(self, organism) -> None:
        self.WIDTH, self.HEIGHT = 512, 512

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game_font = pygame.freetype.Font("your_font.ttf", 24)
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
        self.populate_environment(organism)

    def draw(self):
        self.window.fill("white")
        self.space.debug_draw(self.draw_options)

        self.GAME_FONT.render_to(
            self.window, 
            (40, 350), 
            "Hello World!", 
            (0, 0, 0)
        )

        # pygame.display.flip()
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

                initial_impulse = Vec2d(random.uniform(-1000, 1000), random.uniform(-1000, 1000))
                pymunk.Body.update_velocity(particle, initial_impulse, 10, self.dt)

    def populate_environment(self, organism):
        self.space.add(organism.body.head.matter, organism.body.head.shape)
        organism.body.head.shape.filter = pymunk.ShapeFilter(group=2)
        
        for part in organism.body.structure.values():
            self.space.add(part["obj"].matter, part["obj"].shape)
            part["obj"].shape.filter = pymunk.ShapeFilter(group=2)

            for joint in part["joints"]:
                self.space.add(joint)