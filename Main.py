''' controls:
q - quit
click and drag - new planet
a - toggle acc arrows
v - toggle vel arrows
r - reset
m - toggle center of mass
c - toggle the camera
space and drag - pan the camera
t - toggle trails
, - reduce mass
. - increace mass
u - toggle the UI
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
camera_on_COM = False
panning = False
pre_pan_diff = None

COM = np.array([0, 0])
COM_toggle = False
COM_size = 10
COM_width = 2

to_delete = []

show_trails = True

pygame.font.init()
UI_active = True
UI_font = 'Minecraftia-Regular.ttf'
mass_font = pygame.font.Font(UI_font, 40)
controls_font = pygame.font.Font(UI_font, 20)

while(True):
    timer.tick(60)        #Sets the framerate to 60

    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    screen.fill([0, 0, 5])

    for i in planets:
        i.force(planets, to_delete)

    for i in planets:
        i.up_and_move()

    if len(to_delete) == 2:
        new_mass = to_delete[0].mass + to_delete[1].mass
        new_color = ((to_delete[0].color[0] + to_delete[1].color[0])/2, (to_delete[0].color[1] + to_delete[1].color[1])/2, (to_delete[0].color[2] + to_delete[1].color[2])/2)
        new_coords = np.array([(to_delete[0].coords[0] * to_delete[0].mass + to_delete[1].mass * to_delete[1].coords[0])/new_mass, (to_delete[0].coords[1] * to_delete[0].mass + to_delete[1].mass * to_delete[1].coords[1])/new_mass])
        new_vel = np.array([(to_delete[0].vel[0] * to_delete[0].mass + to_delete[1].mass * to_delete[1].vel[0])/new_mass, (to_delete[0].vel[1] * to_delete[0].mass + to_delete[1].mass * to_delete[1].vel[1])/new_mass])
        planets.append(planet(new_mass, new_coords, new_vel, new_color))
        planets.remove(to_delete[0])
        planets.remove(to_delete[1])
        to_delete = []

    if show_trails:
        for i in planets:
            i.draw_trails(screen, camera)

    for i in planets:
        i.draw(screen, camera)

    if len(planets) != 0:
        COM  = np.array([0, 0])
        total_mass = 0
        for i in planets:
            COM = COM + (i.coords * i.mass)
            total_mass = total_mass + i.mass
        COM = COM/total_mass
    if COM_toggle:
        pygame.draw.line(screen, (60, 60, 225), (COM[0] - camera[0] - COM_size, COM[1] - camera[1]), (COM[0] - camera[0] + COM_size, COM[1] - camera[1]), COM_width)
        pygame.draw.line(screen, (60, 60, 225), (COM[0] - camera[0], COM[1] - camera[1] - COM_size), (COM[0] - camera[0], COM[1] - camera[1] + COM_size), COM_width)

    if camera_on_COM:
        camera = COM - np.array([pygame.Surface.get_width(screen)/2, pygame.Surface.get_height(screen)/2])

    if dragging:
        draw_arrow(screen, pygame.math.Vector2(pygame.mouse.get_pos()), pygame.math.Vector2(pre_drag_pos[0], pre_drag_pos[1]), pygame.Color(100, 100, 100), 5, 15, 15)

    screen.blit(mass_font.render('Mass: ' + str(mass_options[mass_selection]), False, (220, 220, 220)), (30, pygame.Surface.get_height(screen) - 70))

    if UI_active:
        screen.blit(controls_font.render('Controls:', False, (210, 210, 210)), (15, 15))
        screen.blit(controls_font.render('Click and Drag - Make a new planet', False, (210, 210, 210)), (15, 60))
        screen.blit(controls_font.render('Hold Space - Pan', False, (210, 210, 210)), (15, 90))
        screen.blit(controls_font.render(', - Less mass', False, (210, 210, 210)), (15, 120))
        screen.blit(controls_font.render('. - More mass', False, (210, 210, 210)), (15, 150))
        screen.blit(controls_font.render('C - Toggle the camera mode', False, (210, 210, 210)), (15, 180))
        screen.blit(controls_font.render('T - Toggle trails', False, (210, 210, 210)), (15, 210))
        screen.blit(controls_font.render('M - Toggle the center of mass marker', False, (210, 210, 210)), (15, 240))
        screen.blit(controls_font.render('A - Toggle acceleration arrows', False, (210, 210, 210)), (15, 270))
        screen.blit(controls_font.render('V - Toggle velocity arrows', False, (210, 210, 210)), (15, 300))
        screen.blit(controls_font.render('U - Toggle this UI', False, (210, 210, 210)), (15, 330))
        screen.blit(controls_font.render('Q - Quit', False, (210, 210, 210)), (15, 360))


    ''' controls:
    q - quit
    click and drag - new planet
    a - toggle acc arrows
    v - toggle vel arrows
    r - reset
    m - toggle center of mass
    c - toggle the camera
    space and drag - pan the camera
    t - toggle trails
    , - reduce mass
    . - increace mass
    u - toggle the UI
    '''

    if keys[pygame.K_SPACE] and not camera_on_COM:
            camera = pre_pan_diff - np.array(pygame.mouse.get_pos())

    pygame.display.flip()  #updates the screen

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pre_pan_diff = camera + np.array(pygame.mouse.get_pos())
    
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PERIOD:
            mass_selection = (mass_selection + 1) % len(mass_options)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_COMMA:
            mass_selection = (mass_selection - 1) % len(mass_options)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            toggle_acc()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
            toggle_vel()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            show_trails = not show_trails
            for i in planets:
                i.trail = []

        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            camera_on_COM = not camera_on_COM

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            planets = []

        if event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            pre_drag_pos = np.array([pygame.mouse.get_pos()[0] + rand.random() * 0.001, pygame.mouse.get_pos()[1]])

        if event.type == pygame.MOUSEBUTTONUP and dragging == True:
            dragging = False
            planets.append(planet(mass_options[mass_selection], pre_drag_pos + camera, pre_drag_pos - np.array(pygame.mouse.get_pos()), (rand.random()*200 + 25, rand.random()*200 + 25, rand.random()*200 + 25)))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            COM_toggle = not COM_toggle

        if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
            UI_active = not UI_active

        #hitting 'q' will quit
        if keys[pygame.K_q] or event.type == pygame.QUIT:
            pygame.display.quit()
            break