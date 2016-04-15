


class Engine(object):
	def __init__(self):
		pass

	def project(self, space):
		#Divive all coordinates by z axis then discard it
		return (space / space[:, 2, None])[:, :2]

	def translate(self, space, translation):
		return space + translation


