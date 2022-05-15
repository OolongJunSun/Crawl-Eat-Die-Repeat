import pygame
from environment import Environment
from organism import Organism, Limb

if __name__ == "__main__":
    pygame.init()

    run = True

    env = Environment()
    env.create_outer_boundaries()
    
    genome = "fff a12 493 a69 b38 931 129 420"
    adam = Organism(genome)

    env.space.add(adam.body.head.matter, adam.body.head.shape)

    for part in adam.body.structure.values():
        env.space.add(part["obj"].matter, 
                      part["obj"].shape)

        env.space.add(part["joint"])
        
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ERROR_KEK

        env.draw()
        env.space.step(env.dt)
        env.clock.tick(env.fps)

