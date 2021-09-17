from ursina import *

class SurfaceChunk():
	def __init__(self, position = (0,0), neighbours = []):
		self.position = position
		self.gen = noiseGenerator(2, [2, 2], 5)
		self.nmap = self.gen.getMap()
		self.voxels = []
		self.neighbours = [[[False, None] for i in range(3)] for j in range(3)]
		self.corners = [[False for i in range(2)] for i in range(2)]
		self.neighbours[1][1] = [True, self]
		self.toDisable = True
		self.toEnable = True

		for neighbour in neighbours:
			self.neighbours[neighbour[0][0]][neighbour[0][1]] = [True, neighbour[1]]
			neighbour[1].neighbours[2-neighbour[0][0]][2-neighbour[0][1]] = [True, self]

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
					self.voxels.append(Voxel((i + 16*position[0] - 5, h, j + 16*position[1] - 5)))
					self.voxels[-1].chunk = self
				for h in range(13):
					self.voxels.append(Voxel((i + 16*position[0] - 5, -1 - h, j + 16*position[1] - 5), texture='assets/stone_block.png'))
					self.voxels[-1].chunk = self

		for i in range(2):
			for j in range(2):
				for k in range(3):
					for h in range(13):
						if (i == 0):
							for l in range(16):
								self.voxels.append(Voxel((k + 16*position[0] - 8 + 13*j, -1 - h, l + 16*position[1] - 8), texture=stone_texture))
								self.voxels[-1].chunk = self
						else:
							for l in range(10):
								self.voxels.append(Voxel((l + 16*position[0] - 5, -1 - h, k + 16*position[1] - 8 +  13*j), texture=stone_texture))
								self.voxels[-1].chunk = self

		for x in range(3):
			for y in range(3):
				if (x == 1 and y == 1):
					continue
				
				neighbour = self.neighbours[x][y]
				if (not neighbour[0]):
					continue

				npos = (x, y)
				# self.neighbours[npos[0]][npos[1]] = [True, neighbour[1]]
				nblocks = neighbour[1].gen.blockMap
				blocks= None
				bmap = self.gen.blockMap
				if (npos[0] == 1):
					#Either forward or backwards in z
					leftSquare = None
					rightSquare = None
					if (npos[1] == 0):
						#Backwards in z
						nblocks = [nblocks[0][2], nblocks[1][2], nblocks[2][2]]
						blocks = [bmap[0][0], bmap[1][0], bmap[2][0]]
						leftSquare = terrainSquare([[nblocks[0], blocks[0]], [nblocks[1], blocks[1]]], [5, 8])
						rightSquare = terrainSquare([[nblocks[1], blocks[1]], [nblocks[2], blocks[2]]], [5, 8])
					else:
						#Forwards in z
						nblocks = [nblocks[0][0], nblocks[1][0], nblocks[2][0]]
						blocks = [bmap[0][2], bmap[1][2], bmap[2][2]]
						leftSquare = terrainSquare([[blocks[0], nblocks[0]], [blocks[1], nblocks[1]]], [5, 8])
						rightSquare = terrainSquare([[blocks[1], nblocks[1]], [blocks[2], nblocks[2]]], [5, 8])
					
					# Place leftsquare heatmap
					for i in range(5):
						for j in range(8):
							if (j == 0 or j == 7):
								continue
							for h in range(int(leftSquare[i][j]*1.5)):
								if (j < 4 and npos[1] == 2):
									#Voxels on current chunk
									self.voxels.append(Voxel((i + 16*position[0] - 5, h, j + 16*position[1] + 5)))
									self.voxels[-1].chunk = self
								elif (j > 3 and npos[1] == 0):
									#Voxels on current chunk
									self.voxels.append(Voxel((i + 16*position[0] - 5, h, j + 16*position[1] - 8)))
									self.voxels[-1].chunk = self
								elif (j < 4 and npos[1] == 0):
									#Voxels on neighbour chunk
									neighbour[1].voxels.append(Voxel((i + 16*neighbour[1].position[0] - 5, h, j + 16*neighbour[1].position[1] - 8)))
									neighbour[1].voxels[-1].chunk = self
								else:
									#Voxels on neighbour chunk
									neighbour[1].voxels.append(Voxel((i + 16*neighbour[1].position[0] - 5, h, j + 16*neighbour[1].position[1] + 5)))
									neighbour[1].voxels[-1].chunk = self

					# Place rightsquare heatmap
					for i in range(5):
						for j in range(8):
							if (j == 0 or j == 7):
								continue
							for h in range(int(rightSquare[i][j]*1.5)):
								if (j < 4 and npos[1] == 2):
									#Voxels on current chunk
									self.voxels.append(Voxel((i + 16*position[0], h, j + 16*position[1] + 5)))
									self.voxels[-1].chunk = self
								elif (j > 3 and npos[1] == 0):
									#Voxels on current chunk
									self.voxels.append(Voxel((i + 16*position[0], h, j + 16*position[1] - 8)))
									self.voxels[-1].chunk = self
								elif (j < 4 and npos[1] == 0):
									#Voxels on neighbour chunk
									neighbour[1].voxels.append(Voxel((i + 16*neighbour[1].position[0], h, j + 16*neighbour[1].position[1] - 8)))
									neighbour[1].voxels[-1].chunk = self
								else:
									#Voxels on neighbour chunk
									neighbour[1].voxels.append(Voxel((i + 16*neighbour[1].position[0], h, j + 16*neighbour[1].position[1] + 5)))
									neighbour[1].voxels[-1].chunk = self

				elif (npos[1] == 1):
					#Either left or right in x
					downSquare = None
					upSquare = None
					if (npos[0] == 0):
						#Left in x
						nblocks = [nblocks[2][0], nblocks[2][1], nblocks[2][2]]
						blocks = [bmap[0][0], bmap[0][1], bmap[0][2]]
						downSquare = terrainSquare([[nblocks[0], nblocks[1]], [blocks[0], blocks[1]]], [8, 5])
						upSquare = terrainSquare([[nblocks[1], nblocks[2]], [blocks[1], blocks[2]]], [8, 5])

					else:
						#Right in x
						nblocks = [nblocks[0][0], nblocks[0][1], nblocks[0][2]]
						blocks = [bmap[2][0], bmap[2][1], bmap[2][2]]
						downSquare = terrainSquare([[blocks[0], blocks[1]], [nblocks[0], nblocks[1]]], [8,5])
						upSquare = terrainSquare([[blocks[1], blocks[2]], [nblocks[1], nblocks[2]]], [8,5])

					# Place downsquare heatmap
					for i in range(8):
						if (i == 0 or i == 7):
							continue
						for j in range(5):
							for h in range(int(downSquare[i][j]*1.5)):
								if (i < 4 and npos[0] == 2):
									#Voxels on current chunk
									self.voxels.append(Voxel((i + 16*position[0] + 5, h, j + 16*position[1] - 5)))
									self.voxels[-1].chunk = self
								elif (i > 3 and npos[0] == 0):
									#Voxels on current chunk
									self.voxels.append(Voxel((i + 16*position[0] - 8, h, j + 16*position[1] - 5)))
									self.voxels[-1].chunk = self
								elif (i < 4 and npos[0] == 0):
									#Voxels on neighbour chunk
									neighbour[1].voxels.append(Voxel(i + 16*neighbour[1].position[0] - 8, h, j + 16*neighbour[1].position[1] - 5))
									neighbour[1].voxels[-1].chunk = self
								else:
									#Voxels on neighbour chunk
									neighbour[1].voxels.append(Voxel((i + 16*neighbour[1].position[0] + 5, h, j + 16*neighbour[1].position[1] - 5)))
									neighbour[1].voxels[-1].chunk = self

					# Place upsquare heatmap
					for i in range(8):
						if (i == 0 or i == 7):
							continue
						for j in range(5):
							for h in range(int(upSquare[i][j]*1.5)):
								if (i < 4 and npos[0] == 2):
									#Voxels on current chunk
									self.voxels.append(Voxel((i + 16*position[0] + 5, h, j + 16*position[1])))
									self.voxels[-1].chunk = self
								elif (i > 3 and npos[0] == 0):
									#Voxels on current chunk
									self.voxels.append(Voxel((i + 16*position[0] - 8, h, j + 16*position[1])))
									self.voxels[-1].chunk = self
								elif (i < 4 and npos[0] == 0):
									#Voxels on neighbour chunk
									neighbour[1].voxels.append(Voxel((i + 16*neighbour[1].position[0] - 8, h, j + 16*neighbour[1].position[1])))
									neighbour[1].voxels[-1].chunk = self
								else:
									#Voxels on neighbour chunk
									neighbour[1].voxels.append(Voxel((i + 16*neighbour[1].position[0] + 5, h, j + 16*neighbour[1].position[1])))
									neighbour[1].voxels[-1].chunk = self

				else:
					#Corner neighbour
					block = bmap[npos[0]][npos[1]]
					square = None
					if (npos[0] == 0):
						if (npos[1] == 0):
							nblocks = [self.neighbours[0][1][1].gen.blockMap[2][0], neighbour[1].gen.blockMap[2][2], self.neighbours[1][0][1].gen.blockMap[0][2]]
							square = terrainSquare([[nblocks[1], nblocks[0]], [nblocks[2], block]], [8, 8])
						else:
							nblocks = [self.neighbours[0][1][1].gen.blockMap[2][2], neighbour[1].gen.blockMap[2][0], self.neighbours[1][2][1].gen.blockMap[0][0]]
							square = terrainSquare([[nblocks[0], nblocks[1]], [block, nblocks[2]]], [8, 8])
					else:
						if (npos[1] == 0):
							nblocks = [self.neighbours[1][0][1].gen.blockMap[2][2], neighbour[1].gen.blockMap[0][2], self.neighbours[2][1][1].gen.blockMap[0][0]]
							square = terrainSquare([[nblocks[0], block], [nblocks[1], nblocks[2]]], [8, 8])
						else:
							nblocks = [self.neighbours[1][2][1].gen.blockMap[2][0], neighbour[1].gen.blockMap[0][0], self.neighbours[2][1][1].gen.blockMap[0][2]]
							square = terrainSquare([[block, nblocks[0]], [nblocks[2], nblocks[1]]], [8, 8])

					for i in range(8):
						for j in range(8):
							if (i % 7 == 0 or j % 7 == 0):
								continue
							for h in range(int(square[i][j]*1.5)):
								if (i < 4 and npos[0] == 2):
									if (j < 4 and npos[1] == 2):
										self.voxels.append(Voxel((i + 16*position[0] + 5, h, j + 16*position[1] + 5)))
										self.voxels[-1].chunk = self
									elif (j > 3 and npos[1] == 0):
										self.voxels.append(Voxel((i + 16*position[0] + 5, h, j + 16*position[1] - 12)))
										self.voxels[-1].chunk = self
									elif (j < 4):
										self.neighbours[1][0][1].voxels.append(Voxel((i + 16*self.neighbours[1][0][1].position[0] + 5, h, j + 16*self.neighbours[1][0][1].position[1] + 5)))
										self.neighbours[1][0][1].voxels[-1].chunk = self
									else:
										self.neighbours[1][2][1].voxels.append(Voxel((i + 16*self.neighbours[1][2][1].position[0] + 5, h, j + 16*self.neighbours[1][2][1].position[1] - 12)))
										self.neighbours[1][2][1].voxels[-1].chunk = self

								elif (i > 3 and npos[0] == 0):
									if (j < 4 and npos[1] == 2):
										self.voxels.append(Voxel((i + 16*position[0] - 12, h, j + 16*position[1] + 5)))
										self.voxels[-1].chunk = self
									elif (j > 3 and npos[1] == 0):
										self.voxels.append(Voxel((i + 16*position[0] - 12, h, j + 16*position[1] - 12)))
										self.voxels[-1].chunk = self
									elif (j < 4):
										self.neighbours[1][0][1].voxels.append(Voxel((i + 16*self.neighbours[1][0][1].position[0] - 12, h, j + 16*self.neighbours[1][0][1].position[1] + 5)))
										self.neighbours[1][0][1].voxels[-1].chunk = self
									else:
										self.neighbours[1][2][1].voxels.append(Voxel((i + 16*self.neighbours[1][2][1].position[0] - 12, h, j + 16*self.neighbours[1][2][1].position[1] - 12)))
										self.neighbours[1][2][1].voxels[-1].chunk = self

								elif (i < 4):
									if (j < 4 and npos[1] == 2):
										self.neighbours[0][1][1].voxels.append(Voxel((i + 16*self.neighbours[0][1][1].position[0] + 5, h, j + 16*self.neighbours[0][1][1].position[1] + 5)))
										self.neighbours[0][1][1].voxels[-1].chunk = self
									elif (j > 3 and npos[1] == 0):
										self.neighbours[0][1][1].voxels.append(Voxel((i + 16*self.neighbours[0][1][1].position[0] + 5, h, j + 16*self.neighbours[0][1][1].position[1] - 12)))
										self.neighbours[0][1][1].voxels[-1].chunk = self
									elif (j < 4):
										self.neighbours[0][0][1].voxels.append(Voxel((i + 16*self.neighbours[0][0][1].position[0] + 5, h, j + 16*self.neighbours[0][0][1].position[1] + 5)))
										self.neighbours[0][0][1].voxels[-1].chunk = self
									else:
										self.neighbours[0][2][1].voxels.append(Voxel((i + 16*self.neighbours[0][2][1].position[0] + 5, h, j + 16*self.neighbours[0][2][1].position[1] - 12)))
										self.neighbours[0][2][1].voxels[-1].chunk = self

								else:
									if (j < 4 and npos[1] == 2):
										self.neighbours[2][1][1].voxels.append(Voxel((i + 16*self.neighbours[2][1][1].position[0] - 12, h, j + 16*self.neighbours[2][1][1].position[1] + 5)))
										self.neighbours[2][1][1].voxels[-1].chunk = self
									elif (j > 3 and npos[1] == 0):
										self.neighbours[2][1][1].voxels.append(Voxel((i + 16*self.neighbours[2][1][1].position[0] - 12, h, j + 16*self.neighbours[2][1][1].position[1] - 12)))
										self.neighbours[2][1][1].voxels[-1].chunk = self
									elif (j < 4):
										neighbour[1].voxels.append(Voxel((i + 16*neighbour[1].position[0] - 12, h, j + 16*neighbour[1].position[1] + 5)))
										neighbour[1].voxels[-1].chunk = self
									else:
										neighbour[1].voxels.append(Voxel((i + 16*neighbour[1].position[0] - 12, h, j + 16*neighbour[1].position[1] - 12)))
										neighbour[1].voxels[-1].chunk = self
		
	def enable(self):
		global player
		self.toDisable = True
		self.toEnable = False
		for voxel in self.voxels:
			voxel.enabled = True
		for x in range(3):
			for y in range(3):
				if (x == 1 and y == 1):
					continue

				neighbour = self.neighbours[x][y]
				if (neighbour[0]):
					continue

				if (x % 2 == 0 and y % 2 == 0):
					continue

				neighbour[0] = True
				neighbour[1] = SurfaceChunk((self.position[0] + x - 1, self.position[1] + y - 1), [[(2 - x, 2 - y), self]])

		for x in range(2):
			for y in range(2):
				neighbour = self.neighbours[x*2][y*2]
				if (neighbour[0]):
					continue

				neighbour[0] = True
				neighbour[1] = SurfaceChunk((self.position[0] + 2*x - 1, self.position[1] + 2*y - 1), [[(2 - 2*x, 2 - 2*y), self], [(2 - 2*x, 1), self.neighbours[1][y*2][1]], [(1, 2 - 2*y), self.neighbours[x*2][1][1]]])

	def disable(self):
		self.toDisable = False
		self.toEnable = True
		for voxel in self.voxels:
			voxel.enabled = False