from renderer import Renderer
from engine import Engine
import pygame
from pygame.locals import *
import numpy as np
from shaders import Distortion
from flocker import MatricialFlocker as Flocker

E = Engine()
R = Renderer()
F = Flocker()

#Gen 3D data (cube)
points = []
spacing = 20
for x in range(-8, 8, 4):
    for y in range(-8, 8, 4):
        for z in range(1):
            points.append(((x+1)*spacing, (y+1)*spacing+1, z))
points = np.array(points)



#Project it on 2D plane and move origin to center of screen
projected = E.project(points)
projected = E.translate(projected, 320)
R.points = points#projected

D = Distortion(np.array([[20,20,5]]), 30)

#Render and handle events
R.start()
F.start(points)

endRun = False
space = points
while not endRun:
    R.points = F.space#E.translate(E.project(F.space), 320)
    for event in pygame.event.get():
        if event.type == QUIT:
            R.stop()
            F.stop()
            endRun = True
        elif event.type == MOUSEMOTION:
            pass
            # x, y = event.pos
            # point = np.array([x-320, y-320, 3])
            # D.distortion = point
            # newSpace = D.apply(space)
            # R.points = E.translate(E.project(newSpace), 320)