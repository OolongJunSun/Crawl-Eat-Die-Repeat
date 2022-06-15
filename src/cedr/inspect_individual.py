import time
import json
import uuid
import pygame

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment import SimpleHabitat
from individual import BasicProtein

if __name__ == "__main__":
    genome = "A87C654 0289A2B 8B4B8FC 16D8992 2FB668A 10C7BB0 6FF3F1E 6AB993E 45B929F"
    genome = "DD3D0CF 14A4BB5 CB57215 1CA7AEC 4F62BBC DC6E692 ECA9D5B E9A9969 DC21B5C"
    genome = "B9CF55E EE8D6B6 8D9D9B6 4CD4BCC A59BB2F 871F00F FF79F65 D480B61 BF47BFA"
    genome = "E13A6CE 0FD121E 4ED9224 EAF293F DBCD93E D72CBB2 EE6E9E2 4970BFC 4CA3AD5"
    # genome = "7717B4F 8E8E12C 4A4C9B8 3612797 6A2E9FE C11AF9F 0D1ABB2 F02CBFE D30D964"
    # genome = "30B0496 A2CC029 9A989B9 2DA2461 AF3E9F8 C81AEB7 E463B7E F48EB64 EBF5BFD"
    # genome = "1677C5E FE0B3B2 DCBE9F0 F489BE3 FD0FBE4 9EABBDE 3EDF9BE B87FB02 545F8F7"
    # genome = "ED0F2D9 E7B1650 8525C41 E8F69FF F6B2BFF C138B8A CFB399D 67FB0AC 0C67AD1"

    with open("config.json") as json_data_file:
        cfg = json.load(json_data_file)

    organism = BasicProtein(genome, uuid.uuid4())

    start = time.perf_counter()
    
    draw = True
    env = SimpleHabitat(cfg["environment"], seed=56, individual=organism, draw=draw)

    n_steps = 10000

    i = 0
    while i < n_steps:
        if draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ERROR_KEK
            organism.calculate_fitness()
            print(organism.fitness)
            
            env.draw()
            env.clock.tick(env.fps)

        env.space.step(env.dt)
        
        print(i)
        i += 1

    for shape in env.space.shapes:
        env.space.remove(shape)
        shape.body = None

    finish = time.perf_counter()
    elapsed=finish-start

    print(f"{elapsed=}")