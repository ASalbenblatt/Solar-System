''' controls:
q - quit

'''

from math import *
from functions import *

import pygame

import random as rnd
import numpy as np

screen = pygame.display.set_mode()

timer = pygame.time.Clock()

while(True):
    timer.tick(60)        #Sets the framerate to 60
    pygame.event.pump()   #keeps key inputs working

    keys = pygame.key.get_pressed()

    screen.fill([0, 0, 5])



    pygame.display.flip()  #updates the screen

    #hitting 'q' will quit
    if keys[pygame.K_q]:
        pygame.display.quit()
        break