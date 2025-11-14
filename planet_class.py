import numpy as np
import random as rand
import pygame

size_mult = 10
G = 1

class planet:
    def __init__(self, mass, coords, vel, color):
        self.mass = mass
        self.diam = size_mult * (mass**0.33333)
        self.coords = coords
        self.vel = vel
        self.acc = np.array([0, 0])
        self.color = color

    def draw(self, surface, camera_pos):
        pygame.draw.ellipse(surface, self.color, pygame.Rect(self.coords[0] - camera_pos[0] - (self.diam/2), self.coords[1] - camera_pos[1] - (self.diam/2), self.diam, self.diam))

    def force(self, planets, to_delete):
        for i in planets:
            if i != self:
                force_dir = i.coords - self.coords
                r = np.linalg.norm(force_dir)
                self.acc = np.add(G * i.mass * force_dir / (r ** 3), self.acc)
                if r < (self.diam + i.diam) /2 and len(to_delete) == 0:
                    to_delete.append(self)
                    to_delete.append(i)

    def up_and_move (self):
        pass