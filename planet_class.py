import numpy as np
import random as rand
import pygame

size_mult = 10

class planet:
    def __init__(self, mass, coords, vel):
        self.mass = mass
        self.diam = size_mult * (mass**0.33333)
        self.coords = coords
        self.vel = vel
        self.force = np.array([0, 0])
        self.color = (rand.random()*200 + 25, rand.random()*200 + 25, rand.random()*200 + 25)

    def draw(self, surface, camera_pos):
        pygame.draw.ellipse(surface, self.color, pygame.Rect(self.coords[0] - camera_pos[0] - (self.diam/2), self.coords[1] - camera_pos[1] - (self.diam/2), self.diam, self.diam))