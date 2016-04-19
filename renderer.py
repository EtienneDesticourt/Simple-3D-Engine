import pygame, threading, time

class Renderer(object):
    def __init__(self,points=None, displaySize=(800,600), renderDelay=0.01):
        self.display = self.createDisplay(displaySize)
        self.renderDelay = renderDelay
        self.points = points
        #Image resources
        self.pointRes = pygame.Surface((1,1))
        self.pointRes.fill((255,255,255))
        self.backgroundRes = pygame.Surface(displaySize)
        self.backgroundRes.fill((0,0,0))

    def createDisplay(self, displaySize):
        display = pygame.display.set_mode(displaySize)
        return display

    def render(self):
        for point in self.points:
            x, y, z = point
            x = x/z + 320
            y = y/z + 320
            self.pointRes.fill((max(min(255//z, 255), 0), 0, 255))
            self.display.blit(self.pointRes, (x,y))
            

    def run(self):
        while not self.endRun:
            self.display.blit(self.backgroundRes, (0,0))
            self.render()
            pygame.display.flip()
            time.sleep(self.renderDelay)

    def start(self):
        self.endRun = False
        t = threading.Thread(target=self.run)
        t.start()

    def stop(self):
        self.endRun = True