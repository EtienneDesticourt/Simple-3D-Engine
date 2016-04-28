from scipy.spatial.distance import cdist
import time, threading
import numpy as np
from math import sqrt


class Flocker(object):
	def __init__(self, time=time):
		self.time = time
		self.flockRadius = 50
		self.centerWeight = 1 / 100
		self.alignWeight  = 1 / 8
		self.avoidDist  = 3

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

				if flockSize != 0:
					barycenter = localPosSum / flockSize
					centerSpeed = (barycenter - boid1) * self.centerWeight

					meanLocalSpeed = localSpeedSum / flockSize
					alignSpeed = (meanLocalSpeed - speed1) * self.alignWeight
				else:
					centerSpeed = 0
					alignSpeed = 0

				boundingSpeedRate = 1
				boundingSpeed =  np.array([0,0,0])
				x, y, z = self.space[i]
				if z != -35:
					x = x / (1 + z / 35) + 320
					y = y / (1 + z / 35) + 320
				else:
					x = 1000
					y = 1000

				if z >= 5: boundingSpeed[-1] = -boundingSpeedRate
				elif z < 0.5: boundingSpeed[-1] = boundingSpeedRate
				if  x >= 750: boundingSpeed[0] = -boundingSpeedRate
				elif x <= 50: boundingSpeed[0] = boundingSpeedRate
				if y >= 550: boundingSpeed[1] = -boundingSpeedRate
				elif y <= 50: boundingSpeed[1] = boundingSpeedRate



				newSpeed = speed1 + centerSpeed + alignSpeed + avoidSpeed + boundingSpeed
				if newSpeed.sum() > 10:
					newSpeed /= newSpeed.max()
					newSpeed *= 10

				self.speed[i] = newSpeed
				self.space[i] = boid1 + self.speed[i]

			self.time.sleep(0.1)

	def start(self, space):
		self.keepFlocking = True
		threading.Thread(target=self.flock, args=[space]).start()

	def stop(self):
		self.keepFlocking = False







#This is more of an exercise on numpy indexing and mental visualisation of
#matricial operations rather than a practical way to implement flocking IMO, 
#for anything above 100 boids I would just implement it in C and import it,
#I actually did that a while back but I don't know what I did with that module
# ... ¯\_(ツ)_/¯



class MatricialFlocker(object):
	def __init__(self, time=time):
		self.time = time
		self.flockRadius = 10000
		self.centerWeight = 1 / 100
		self.alignWeight  = 1 / 2
		self.avoidWeight = 1
		self.avoidDist  = 200
		self.bounds = [[50, 750], [50, 550], [0.5, 1.5]]
		self.defaultBoundingSpeed = 3

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
		vectorsMatrix = space[:, None] - space[:, None].swapaxes(0,1)
		distances[distances == 0] = 1
		vectorsMatrix = vectorsMatrix / distances[:, :, None]
		vectorsMatrix[distances > self.avoidDist] = 0
		localSum = vectorsMatrix.sum(axis=1) / localCount[:, None]
		#Calc speed to reach baricenters
		speed = - localSum  * self.avoidWeight
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

	def bind(self, space):
		renderedPos = space.copy()
		renderedPos[:, 2][renderedPos[:, 2] == -35] = -35.1
		renderedPos[:, :2] /= renderedPos[:, 2][:, None] / 35 + 1 
		renderedPos[:, :2] += 320

		x, y, z = self.bounds
		boundingSpeed = np.zeros(space.shape)
		#bind x
		boundingSpeed[:, 0][renderedPos[:, 0] > x[1]] = -self.defaultBoundingSpeed
		boundingSpeed[:, 0][renderedPos[:, 0] < x[0]] = self.defaultBoundingSpeed
		#bind y
		boundingSpeed[:, 1][renderedPos[:, 1] > y[1]] = -self.defaultBoundingSpeed
		boundingSpeed[:, 1][renderedPos[:, 1] < y[0]] = self.defaultBoundingSpeed
		#bind z
		boundingSpeed[:, 2][renderedPos[:, 2] > z[1]] = -self.defaultBoundingSpeed
		boundingSpeed[:, 2][renderedPos[:, 2] < z[0]] = self.defaultBoundingSpeed

		return boundingSpeed


	def flock(self, space):
		self.space = space
		self.speed = np.zeros(space.shape)
		while self.keepFlocking:
			#We get the distance between each point and every other point (matrix)
			distances = cdist(space, space)
			centerSpeed = self.center(space, distances)
			avoidSpeed = self.avoid(space, distances)
			alignSpeed = self.align(space, distances)
			boundingSpeed = self.bind(space)
			
			newSpeed = self.speed + centerSpeed  + alignSpeed + avoidSpeed + boundingSpeed
			newSpeed /= abs(newSpeed).max(axis=1)[:, None]
			newSpeed *= 5
			

			self.speed = newSpeed 
			self.space += self.speed







			#print(self.speed)
			self.time.sleep(0.01)

	def start(self, space):
		self.keepFlocking = True
		threading.Thread(target=self.flock, args=[space]).start()

	def stop(self):
		self.keepFlocking = False
		