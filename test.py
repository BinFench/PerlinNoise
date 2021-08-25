from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin import noiseGenerator

app = Ursina()
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')
punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 1
chunks = []
player = FirstPersonController()

# window.fps_counter.enabled = False
window.exit_button.visible = False

def update():
	global block_pick, chunks

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4
	chunks[0].checkEnable()

class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_texture, chunk = None):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5)
		self.chunk = chunk

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

class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 10000,
			double_sided = True)

class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.4,-0.6))

	def active(self):
		self.position = Vec2(0.3,-0.5)

	def passive(self):
		self.position = Vec2(0.4,-0.6)

class SurfaceChunk():
	def __init__(self):
		self.gen = noiseGenerator(2, [2, 2], 5)
		self.nmap = self.gen.getMap()
		self.voxels = []
		for i in range(10):
			for j in range(10):
				if (not (i % 5 == 0 or j % 5  == 0)):
					continue
				avg = 0
				
				coords = [(i-1, j-1), (i, j-1), (i+1, j-1),
						(i-1, j),			 (i+1, j),
						(i-1, j+1), (i, j+1), (i+1, j+1)]

				coords = list(filter((lambda coord : coord[0] >= 0 and coord[0] <= 9 and coord[1] >= 0 and coord[1] <= 9 and \
									not(coord[0] % 5 == 0 or coord[1] % 5 == 0)), coords))

				for coord in coords:
					avg += self.nmap[coord[0]][coord[1]]/len(coords)

				self.nmap[i][j] = avg

		for i in range(10):
			for j in range(10):
				avg = 0
				
				coords = [(i-1, j-1), (i, j-1), (i+1, j-1),
						(i-1, j),			 (i+1, j),
						(i-1, j+1), (i, j+1), (i+1, j+1)]

				coords = list(filter((lambda coord : coord[0] >= 0 and coord[0] <= 9 and coord[1] >= 0 and coord[1] <= 9), coords))

				for coord in coords:
					avg += self.nmap[coord[0]][coord[1]]/len(coords)

				self.nmap[i][j] = avg + 1

		for i in range(10):
			for j in range(10):
				for h in range(int(self.nmap[i][j]*1.5)):
					self.voxels.append(Voxel((i, h, j)))
					self.voxels[-1].chunk = self
				for h in range(6):
					self.voxels.append(Voxel((i, -1 - h, j), texture=stone_texture))
					self.voxels[-1].chunk = self
		
	def checkEnable(self):
		global player
		for voxel in self.voxels:
			inRange = distance(voxel.world_position, player.world_position) <= 5
			voxel.collision = inRange
			voxel.ignore = not inRange

chunks.append(SurfaceChunk())
player.y = 7
sky = Sky()
hand = Hand()
app.run()