from ursina import *

class SingleVoxel(Button):
	def __init__(self, position = (0,0,0), texture = load_texture('assets/grass_block.png'), chunk = None):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5)
		self.chunk = chunk
		# print(len(self.model.vertices), len(self.model.uvs), len(self.model.triangles), len(self.model.normals))
		# for i in range(36):
		# 	print("#1: ", self.model.vertices[i], self.model.uvs[i], self.model.normals[i])