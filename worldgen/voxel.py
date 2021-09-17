from ursina import *

punch_sound = Audio('assets/punch_sound',loop = False, autoplay = False)

class Voxel():
	def __init__(self, position = (0,0,0), texture = 'assets/grass_block.png', chunk = None):
		self.chunk = chunk
        self.vertices = []
        self.vertIndices = []
        self.triangles = []
        self.triIndices = []
		self.uvs = []
		self.uvIndices = []
        self.texture = texture
        self.position = position

	def input(self,key):
		if self.hovered:
			if key == 'right mouse down':
				punch_sound.play()
				if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
				if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
				if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
				if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)

			if key == 'left mouse down':
				punch_sound.play()
				if (self.chunk is not None):
					self.chunk.voxels.remove(self)
				destroy(self)

	def clearGeometry():
		self.vertices = []
        self.vertIndices = []
        self.triangles = []
        self.triIndices = []
		self.uvs = []
		self.uvIndices = []