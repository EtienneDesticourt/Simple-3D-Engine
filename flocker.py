from scipy.spatial.distance import cdist
import time, threading
import numpy as np

class Flocker(object):
	def __init__(self, time=time):
		self.time = time
		self.flockRadius = 100
		self.centerWeight = 1 / 100
		self.alignWeight  = 1 / 8
		self.avoidDist  = 10

	def center(self, space, distances):
		#Space is a vector of points, we get a matrix by repeating it along its depth
		spaceMatrix = np.repeat(space[None, :], space.shape[0], axis=0)
		#Set position of non local points to 0 so they don't get counted
		spaceMatrix[distances > self.flockRadius] = 0
		baricenters = spaceMatrix.sum(axis=1) / space.shape[0]
		#Calc speed to reach baricenters
		speed = (baricenters - space) * self.centerWeight
		return speed

	def avoid(self, space, distances):
		#Space is a vector of points, we get a matrix by repeating it along its depth
		spaceMatrix = np.repeat(space[None, :], space.shape[0], axis=0)
		#Set position of non local points to 0 so they don't get counted
		spaceMatrix[distances > self.avoidDist] = 0
		localCount = (distances <= self.avoidDist).sum(axis=1)
		localSum = spaceMatrix.sum(axis=1)
		#Calc speed to reach baricenters
		speed = - (localSum - space * localCount[:, None])
		return speed

	def align(self, space, distances):
		#Speed is a vector of speeds, we get a matrix by repeating it along its depth
		speedMatrix = np.repeat(self.speed[None, :], self.speed.shape[0], axis=0)
		#Set speed of non local points to 0 so they don't get counted
		speedMatrix[distances > self.flockRadius] = 0
		meanLocalSpeed = speedMatrix.sum(axis=1) / space.shape[0]
		#Calc speed to reach baricenters
		speed = (meanLocalSpeed - self.speed) * self.alignWeight
		return speed

	def flock(self, space):
		self.space = space
		self.speed = np.zeros(space.shape)
		while self.keepFlocking:
			#We get the distance between each point and every other point (matrix)
			distances = cdist(space, space)
			centerSpeed = self.center(space, distances)
			avoidSpeed = self.avoid(space, distances)
			alignSpeed = self.align(space, distances)

			self.speed += centerSpeed  + alignSpeed + avoidSpeed
			self.space += self.speed
			#print(self.speed)
			self.time.sleep(0.01)

	def start(self, space):
		self.keepFlocking = True
		threading.Thread(target=self.flock, args=[space]).start()

	def stop(self):
		self.keepFlocking = False
		