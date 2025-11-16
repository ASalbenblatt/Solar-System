import numpy as np
import random as rand
import pygame
from functions import *

size_mult = 10
G = 1
acc_mult = 200
vel_mult = 0.01

show_acc = False
acc_vec_scale = 25

show_vel = False
vel_vec_scale = 0.3

def toggle_acc ():
    global show_acc
    show_acc = not show_acc

def toggle_vel ():
    global show_vel
    show_vel = not show_vel

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
        if show_acc and show_vel:
            draw_arrow(surface, pygame.math.Vector2(self.coords[0] - camera_pos[0], self.coords[1] - camera_pos[1]), pygame.math.Vector2(np.add(self.vel * vel_vec_scale, self.coords)[0] - camera_pos[0], np.add(self.vel * vel_vec_scale, self.coords)[1] - camera_pos[1]), (0, 200, 0))
            draw_arrow(surface, pygame.math.Vector2(self.coords[0] - camera_pos[0] + (self.vel * vel_vec_scale)[0], self.coords[1] - camera_pos[1] + (self.vel * vel_vec_scale)[1]), pygame.math.Vector2(np.add(self.acc * acc_vec_scale, self.coords)[0] - camera_pos[0] + (self.vel * vel_vec_scale)[0], np.add(self.acc * acc_vec_scale, self.coords)[1] - camera_pos[1] + (self.vel * vel_vec_scale)[1]), (200, 0, 0))
        elif show_vel:
            draw_arrow(surface, pygame.math.Vector2(self.coords[0] - camera_pos[0], self.coords[1] - camera_pos[1]), pygame.math.Vector2(np.add(self.vel * vel_vec_scale, self.coords)[0] - camera_pos[0], np.add(self.vel * vel_vec_scale, self.coords)[1] - camera_pos[1]), (0, 200, 0))
        elif show_acc:
            draw_arrow(surface, pygame.math.Vector2(self.coords[0] - camera_pos[0], self.coords[1] - camera_pos[1]), pygame.math.Vector2(np.add(self.acc * acc_vec_scale, self.coords)[0] - camera_pos[0], np.add(self.acc * acc_vec_scale, self.coords)[1] - camera_pos[1]), (200, 0, 0))

    def force(self, planets, to_delete):
        self.acc = np.array([0, 0])
        for i in planets:
            if i != self:
                force_dir = i.coords - self.coords
                r = np.linalg.norm(force_dir)
                self.acc = np.add(G * i.mass * force_dir / (r ** 3) * acc_mult, self.acc)
                if r < (self.diam + i.diam) /2 and len(to_delete) == 0:
                    to_delete.append(self)
                    to_delete.append(i)

    def up_and_move (self):
        self.vel = np.add(self.vel, self.acc)
        self.coords = np.add(self.coords, self.vel * vel_mult)