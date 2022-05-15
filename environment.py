import pygame
import pymunk
import pymunk.pygame_util

class Environment():
    def __init__(self) -> None:
        self.WIDTH, self.HEIGHT = 512, 512
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)

        self.space = pymunk.Space()
        self.space.gravity = (0,10)

        self.clock = pygame.time.Clock()
        self.fps = 30
        self.dt = 1/self.fps

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
