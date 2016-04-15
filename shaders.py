from shader import Shader
import numpy as np

class Distortion(Shader):
	def __init__(self, distortion, strength):
		self.distortion = distortion
		self.strength = strength

	def apply(self, space):
		vector = space - self.distortion
		distance = np.linalg.norm(vector, axis=1)
		return (space - vector * self.strength / distance[:, None])
