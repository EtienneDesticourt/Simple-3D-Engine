from scipy.spatial.distance import cdist
import time, threading
import numpy as np
from math import sqrt


class Flocker(object):
	def __init__(self, time=time):
		self.time = time
		self.flockRadius = 100
		self.centerWeight = 1 / 100
		self.alignWeight  = 1 / 8
		self.avoidDist  = 10

	def flock(self, space):
		self.space = space
		self.speed = [0] * len(space)
		while self.keepFlocking:

			for i in range(len(self.space)):
				boid1 = self.space[i]
				speed1 = self.speed[i]

				flockSize = 0
				localPosSum = 0
				localSpeedSum = 0
				avoidSpeed = 0

				for j in range(len(self.space)):
					if i == j: continue
					boid2 = self.space[j]
					speed2 = self.speed[j]

					squaredDif = (boid2 - boid1) ** 2
					distance = sqrt(squaredDif.sum())

					if distance <= self.flockRadius:
						localPosSum += boid2
						localSpeedSum += speed2
						flockSize += 1

					if distance <= self.avoidDist:
						avoidSpeed -= (boid2 - boid1)

				barycenter = localPosSum / flockSize
				centerSpeed = (barycenter - boid1) * self.centerWeight

				meanLocalSpeed = localSpeedSum / flockSize
				alignSpeed = (meanLocalSpeed - speed1) * self.alignWeight

				self.speed[i] =  speed1 + centerSpeed + alignSpeed + avoidSpeed
				self.space[i] = boid1 + self.speed[i]

			self.time.sleep(0.1)

	def start(self, space):
		self.keepFlocking = True
		threading.Thread(target=self.flock, args=[space]).start()

	def stop(self):
		self.keepFlocking = False











class MatricialFlocker(object):
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
		