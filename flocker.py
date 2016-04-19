from scipy.spatial.distance import cdist

class Flocker(object):
	def __init__(self, space, flockSize = 10):
		self.flockSize = flockSize
		self.speed = np.array(space.size)

	def center(self, spaceMatrix):
		pass
		

	def avoid(self, space):
		pass

	def align(self, space):
		pass

	def flock(self, space):
		#We get the distance between each point and every other point (matrix)
		distances = cdist(space, space)
		localFlocks = distances < flockSize
		#Space is a vector of points, we get a matrix by repeating it along its depth
		spaceMatrix = np.repeat(space[None, :], space.shape[0], axis=0)
		#We get the baricenter of points that are close together
		spaceMatrix[localFlocks]

		