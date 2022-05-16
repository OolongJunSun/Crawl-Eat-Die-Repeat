import pygame
import pymunk
from environment import Environment
from organism import Organism, Limb

if __name__ == "__main__":
    pygame.init()

    run = True

    env = Environment()
    env.create_outer_boundaries()
    
    genome = "fff 8b5 53f fff 8b5 53f fff 8b5 53f fff 8b5 53f fff"
    adam = Organism(genome)

    # env.load_objects(adam.body.structure)

    # env.space.add(adam.body.head.matter, adam.body.head.shape)

    for part in adam.body.structure.values():
        env.space.add(part["obj"].matter, 
                      part["obj"].shape)

        part["obj"].shape.filter = pymunk.ShapeFilter(group=1)

        if isinstance(part["obj"], Limb):
            env.space.add(part["joint"])
        
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ERROR_KEK

        env.draw()
        env.space.step(env.dt)
        env.clock.tick(env.fps)

