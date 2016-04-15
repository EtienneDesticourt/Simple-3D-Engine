import pygame, threading, time

class Renderer(object):
    def __init__(self, displaySize=(800,600), renderDelay=0.01):
        self.display = self.createDisplay(displaySize)
        self.renderDelay = renderDelay
        
        #Image resources
        self.pointRes = pygame.Surface((1,1))
        self.pointRes.fill((255,255,255))
        self.backgroundRes = pygame.Surface(displaySize)
        self.backgroundRes.fill((0,0,0))

    def createDisplay(self, displaySize):
        display = pygame.display.set_mode(displaySize)
        return display

    def render(self, points):
        for point in points:
            self.display.blit(self.pointRes, point)
            

    def run(self, points):
        while not self.endRun:
            self.display.blit(self.backgroundRes, (0,0))
            self.render(points)
            pygame.display.flip()
            time.sleep(self.renderDelay)

    def start(self, points):
        self.endRun = False
        t = threading.Thread(target=self.run, args=[points])
        t.start()

    def stop(self):
        self.endRun = True