# Crawl-Eat-Die-Repeat
Physics-based evolutionary simulation for agents without a control system. 

## About
This is a hobby project that explores how agents can develop complex behaviours without having a central controller.
The agents are procedurally generated from hexadecimal string genomes which are subject to evolutionary mechasims over many iterations. 
They are analogues of proteins with parts that can rotate constantly, maintain an angle with their neighbouring parts or hang freely.

The agents inhabit a physics-based particle substrate. Agents are evaluated on their ability to move away from the center of the frame.
In the future other fitness functions will be added that also evaluate energy use, food collectio, damage avoidance, etc. 

## Features
- Basic genetic algorithm functions (selection, crossover, mutation)
- Physics environment with Pymunk
- Graphics with Pygame
- GUI with Dear PyGui
- Schemata analysis tool (in progress)

## To do
- [ ] Implement genetic algorithm operations
  - [ ] N-point crossover
  - [ ] Uniform crossover
  - [ ] Roulette selection
  - [ ] Tournament selection
  - [ ] Boltzmann selection
  - [ ] Mutation annealing
  
