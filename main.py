import pygame
import pymunk
import random
from environment import Environment
from organism import Organism, Limb

if __name__ == "__main__":
    pygame.init()

    run = True

    env = Environment()
    env.create_outer_boundaries()
    
    genome = '%030x' % random.randrange(16**30)
    genome =  ' '.join(genome[i:i+3] for i in range(0, len(genome), 3))
    print(genome)
    # genome = "fff 8b5 53f fff 8b5 53f fff"
    adam = Organism(genome)


    for part in adam.body.structure.values():
        env.space.add(part["obj"].matter, 
                      part["obj"].shape)

        part["obj"].shape.filter = pymunk.ShapeFilter(categories=1, mask=2)

        if isinstance(part["obj"], Limb):
            env.space.add(part["joint"])
        
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ERROR_KEK

        env.draw()
        env.space.step(env.dt)
        env.clock.tick(env.fps)

