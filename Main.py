''' controls:
q - quit
click and drag - new planet
'''

from math import *
from functions import *
from planet_class import *

import pygame

import random as rnd
import numpy as np

#Creates the window
pygame.display.init()
screen_size = pygame.display.get_desktop_sizes()[0]
screen_size = (screen_size[0], screen_size[1] - 60)
flags = pygame.RESIZABLE
screen = pygame.display.set_mode(screen_size, flags)

timer = pygame.time.Clock()

planets = []
dragging = False
pre_drag_pos = np.array([0,0])

mass_options = [1, 5, 10, 25, 50, 100, 250]
mass_selection = 3

camera = np.array([0, 0])

while(True):
    timer.tick(60)        #Sets the framerate to 60
    pygame.event.pump()   #keeps key inputs working

    keys = pygame.key.get_pressed()
    event = pygame.event.poll()

    screen.fill([0, 0, 5])

    for i in planets:
        i.draw(screen, camera)

    if event.type == pygame.KEYDOWN and event.key == pygame.K_PERIOD:
        mass_selection = (mass_selection + 1) % 7
    
    if event.type == pygame.KEYDOWN and event.key == pygame.K_COMMA:
        mass_selection = (mass_selection - 1) % 7

    if event.type == pygame.MOUSEBUTTONDOWN:
        dragging = True
        pre_drag_pos = np.array(pygame.mouse.get_pos())

    if event.type == pygame.MOUSEBUTTONUP and dragging == True:
        dragging = False
        planets.append(planet(mass_options[mass_selection], pre_drag_pos + camera, pre_drag_pos - np.array(pygame.mouse.get_pos())))

    if dragging:
        draw_arrow(screen, pygame.math.Vector2(pygame.mouse.get_pos()), pygame.math.Vector2(pre_drag_pos[0], pre_drag_pos[1]), pygame.Color(100, 100, 100), 5, 15, 15)

    pygame.display.flip()  #updates the screen

    #hitting 'q' will quit
    if keys[pygame.K_q] or event.type == pygame.QUIT:
        pygame.display.quit()
        break