from renderer import Renderer
from engine import Engine
import pygame
from pygame.locals import *
import numpy as np
from shaders import Distortion
E = Engine()
R = Renderer()

#Gen 3D data (cube)
points = []
spacing = 20
for x in range(-10, 10, 2):
    for y in range(-10, 10, 2):
        for z in range(10):
            points.append(((x+1)*spacing, (y+1)*spacing+1, 1+z/35))
points = np.array(points)



#Project it on 2D plane and move origin to center of screen
projected = E.project(points)
projected = E.translate(projected, 320)
R.points = projected

D = Distortion(np.array([[20,20,5]]), 30)

#Render and handle events
R.start(projected)
endRun = False
space = points
while not endRun:
    for event in pygame.event.get():
        if event.type == QUIT:
            R.stop()
            endRun = True
        elif event.type == MOUSEMOTION:
            x, y = event.pos
            point = np.array([x-320, y-320, 3])
            D.distortion = point
            newSpace = D.apply(space)
            R.points = E.translate(E.project(newSpace), 320)