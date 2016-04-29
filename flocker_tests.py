import numpy as np
from math import sqrt
from flocker import MatricialFlocker
from scipy.spatial.distance import cdist
def testAvoid():
	space = np.array([])

	pass

def testCenter():
	flockRadius = 10
	space = np.array([[1,2,3], # 1 flockmate
					  [4,5,6], # 2 flockmates
					  [7,8,9],
					  [70,45,89], #0 flockmates
					  [120,150,170],
					  [121,148,165]], dtype=np.float32)

	#Initialize correct array of steering speeds for test space
	correctSpeeds = np.zeros(space.shape)
	for i in range(space.shape[0]):
		point1 = space[i]

		#Get that boid's flock and leave speed at 0 if he doesn't have one		
		flock = getFlock(space, i, flockRadius)
		if flock.shape[0] == 0: continue

		#Sum all boid positions
		positionSum = np.zeros(3)
		for otherPoint in flock:
			positionSum += otherPoint

		#Calc barycenter
		barycenter = positionSum / flock.shape[0]
		#Calc steering
		speed = barycenter - point1
		correctSpeeds[i] = speed

	#Initialize flocker
	MF = MatricialFlocker(flockRadius) #motherfucking matricial flocker, rolls off the tongue
	distances = MF.calcDistances(space)
	actualSpeeds = MF.center(space, distances)

	assert (correctSpeeds == actualSpeeds).all()



def testAlign():
	pass


#helpers

def calcDistance(point1, point2):
	return sqrt(((point2 - point1) ** 2).sum())

def getFlock(space, index, flockRadius):
	flock = []
	point = space[index]
	for i in range(space.shape[0]):
		if i == index: continue
		otherPoint = space[i]

		distance = calcDistance(point, otherPoint)
		if distance <= flockRadius:
			flock.append(otherPoint)

	return np.array(flock)

space = np.array([[1,2,3], # 1 flockmate
				  [4,5,6], # 2 flockmates
				  [7,8,9],
				  [70,45,89], #0 flockmates
				  [120,150,170],
				  [121,148,165]])



testCenter()