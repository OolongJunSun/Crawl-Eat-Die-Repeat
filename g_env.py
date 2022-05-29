import random
import pygame
# import pygame.freetype
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

class Environment():
    def __init__(self, organism) -> None:
        self.WIDTH, self.HEIGHT = 768, 768

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
        self.draw_options.collision_point_color = (255, 255,255, 100)
        
        self.particles = []

        self.space = pymunk.Space()
        self.space.gravity = (0,0)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 1/self.fps
 

        self.particle_density = 25 # 15
        self.n_particles_x = int(self.WIDTH/self.particle_density) 
        self.n_particles_y = int(self.HEIGHT/self.particle_density)

        # self.create_outer_boundaries()
        self.create_substrate()
        self.populate_environment(organism)

    # def display_fps(self):
    #     "Data that will be rendered and blitted in _display"
    #     self.render(
    #         self.fonts[0],
    #         what=str(int(self.clock.get_fps())),
    #         color="red",
    #         where=(10, 10))


    # def create_fonts(self, font_sizes_list):
    #     "Creates different fonts with one list"
    #     self.fonts = []
    #     for size in font_sizes_list:
    #         self.fonts.append(
    #             pygame.font.SysFont("Arial", size))
    #     return self.fonts


    # def render(self,fnt, what, color, where):
    #     "Renders the fonts as passed from display_fps"
    #     text_to_show = fnt.render(what, 0, pygame.Color(color))
    #     self.window.blit(text_to_show, where)

    def obj_wrap(self, organism):
        for particle in self.particles:
            if particle.position.x < 0:
                particle.position = (self.WIDTH, particle.position.y)
            elif particle.position.x > self.WIDTH:
                particle.position = (0, particle.position.y)
            elif particle.position.y > self.HEIGHT:
                particle.position = (particle.position.x, 0)
            elif particle.position.y < 0:
                particle.position = (particle.position.x, self.HEIGHT)

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



    def draw(self):
        self.window.fill("white")
        self.space.debug_draw(self.draw_options)
        # self.display_fps()
        
        # rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        # sub = self.window.subsurface(rect)
        # pygame.image.save(sub, "screenshot.jpg")
        

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
        for j in range(2,self.n_particles_y-1):
            for i in range(2,self.n_particles_x-1):
                if ((i > int(340/self.particle_density) and 
                    j > int(340/self.particle_density) and 
                    i < int(430/self.particle_density) and 
                    j < int(430/self.particle_density)) or
                    i == 0 or j == 0 or 
                    i == self.WIDTH/self.particle_density or 
                    j == self.WIDTH/self.particle_density):
                    continue
                else:
                    particle = pymunk.Body()
                    particle.position = (i*self.particle_density, j*self.particle_density)
                    
                    shape = pymunk.Circle(particle, 6) # 6 # 2.5
                    shape.density = 2.8
                    shape.elasticity = 0.99
                    shape.friction = 0.02
                    shape.color = (55, 210,255, 100)
                    self.space.add(particle, shape)

                    self.particles.append(particle)

                    initial_impulse = Vec2d(random.uniform(-800, 800), random.uniform(-800, 800))
                    pymunk.Body.update_velocity(particle, initial_impulse, 10, self.dt)


    def populate_environment(self, organism):
        # self.space.add(organism.body.head.matter, organism.body.head.shape)
        # organism.body.head.shape.filter = pymunk.ShapeFilter(group=2)
        
        # for part in organism.body.structure.values():
        #     self.space.add(part["obj"].matter, part["obj"].shape)
        #     part["obj"].shape.filter = pymunk.ShapeFilter(group=2)

        #     for joint in part["joints"]:
        #         self.space.add(joint)

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
