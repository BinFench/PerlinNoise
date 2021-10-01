from ursina import *
from worldgen.chunk import Chunk
from worldgen.perlin import noiseGenerator
from worldgen.voxel import Voxel
from utils.terrainSquare import terrainSquare

class SurfaceChunk(Chunk):
	def __init__(self, position = (0,0), neighbours = [], globchunks = []):
		print("SurfaceChunk at: ", position)
		super().__init__(position=(position[0], 0, position[1]))
		self.gen = noiseGenerator(2, [2, 2], 5)
		self.nmap = self.gen.getMap()
		self.neighbours = [[[False, None] for i in range(3)] for j in range(3)]
		self.corners = [[False for i in range(2)] for i in range(2)]
		self.neighbours[1][1] = [True, self]
		self.pos = position
		self.chunks = globchunks

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
					self.addVoxel(Voxel((i + 3, h + 11, j + 3)))
				for h in range(11):
					self.addVoxel(Voxel((i + 3, h, j + 3), texture='assets/stone_block.png'))

		for i in range(2):
			for j in range(2):
				for k in range(3):
					for h in range(11):
						if (i == 0):
							for l in range(16):
								self.addVoxel(Voxel((k + 13*j, h, l), texture='assets/stone_block.png'))
						else:
							for l in range(10):
								self.addVoxel(Voxel((l + 3, h, k + 13*j), texture='assets/stone_block.png'))

		for x in range(3):
			for y in range(3):
				if (x == 1 and y == 1):
					continue
				
				neighbour = self.neighbours[x][y]
				if (not neighbour[0]):
					continue

				npos = (x, y)
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
									self.addVoxel(Voxel((i + 3, h + 11, j + 12)))
								elif (j > 3 and npos[1] == 0):
									#Voxels on current chunk
									self.addVoxel(Voxel((i + 3, h + 11, j - 4)))
								elif (j < 4 and npos[1] == 0):
									#Voxels on neighbour chunk
									neighbour[1].addVoxel(Voxel((i + 3, h + 11, j + 12)))
								else:
									#Voxels on neighbour chunk
									neighbour[1].addVoxel(Voxel((i + 3, h + 11, j - 4)))

					# Place rightsquare heatmap
					for i in range(5):
						for j in range(8):
							if (j == 0 or j == 7):
								continue
							for h in range(int(rightSquare[i][j]*1.5)):
								if (j < 4 and npos[1] == 2):
									#Voxels on current chunk
									self.addVoxel(Voxel((i + 8, h + 11, j + 12)))
								elif (j > 3 and npos[1] == 0):
									#Voxels on current chunk
									self.addVoxel(Voxel((i + 8, h + 11, j - 4)))
								elif (j < 4 and npos[1] == 0):
									#Voxels on neighbour chunk
									neighbour[1].addVoxel(Voxel((i + 8, h + 11, j + 12)))
								else:
									#Voxels on neighbour chunk
									neighbour[1].addVoxel(Voxel((i + 8, h + 11, j - 4)))

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
									self.addVoxel(Voxel((i + 12, h + 11, j + 3)))
								elif (i > 3 and npos[0] == 0):
									#Voxels on current chunk
									self.addVoxel(Voxel((i - 4, h + 11, j + 3)))
								elif (i < 4 and npos[0] == 0):
									#Voxels on neighbour chunk
									neighbour[1].addVoxel(Voxel((i + 12, h + 11, j + 3)))
								else:
									#Voxels on neighbour chunk
									neighbour[1].addVoxel(Voxel((i - 4, h + 11, j + 3)))

					# Place upsquare heatmap
					for i in range(8):
						if (i == 0 or i == 7):
							continue
						for j in range(5):
							for h in range(int(upSquare[i][j]*1.5)):
								if (i < 4 and npos[0] == 2):
									#Voxels on current chunk
									self.addVoxel(Voxel((i + 12, h + 11, j + 8)))
								elif (i > 3 and npos[0] == 0):
									#Voxels on current chunk
									self.addVoxel(Voxel((i - 4, h + 11, j + 8)))
								elif (i < 4 and npos[0] == 0):
									#Voxels on neighbour chunk
									neighbour[1].addVoxel(Voxel((i + 12, h + 11, j + 8)))
								else:
									#Voxels on neighbour chunk
									neighbour[1].addVoxel(Voxel((i - 4, h + 11, j + 8)))

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
										self.addVoxel(Voxel((i + 12, h + 11, j + 12)))
									elif (j > 3 and npos[1] == 0):
										self.addVoxel(Voxel((i + 12, h + 11, j - 4)))
									elif (j < 4):
										self.neighbours[1][0][1].addVoxel(Voxel((i, h + 11, j + 12)))
									else:
										self.neighbours[1][2][1].addVoxel(Voxel((i, h + 11, j - 4)))

								elif (i > 3 and npos[0] == 0):
									if (j < 4 and npos[1] == 2):
										self.addVoxel(Voxel((i - 4, h + 11, j + 12)))
									elif (j > 3 and npos[1] == 0):
										self.addVoxel(Voxel((i - 4, h + 11, j - 4)))
									elif (j < 4):
										self.neighbours[1][0][1].addVoxel(Voxel((i + 9, h + 11, j + 12)))
									else:
										self.neighbours[1][2][1].addVoxel(Voxel((i + 9, h + 11, j - 4)))

								elif (i < 4):
									if (j < 4 and npos[1] == 2):
										self.neighbours[0][1][1].addVoxel(Voxel((i + 12, h + 11, j + 12)))
									elif (j > 3 and npos[1] == 0):
										self.neighbours[0][1][1].addVoxel(Voxel((i + 12, h + 11, j - 4)))
									elif (j < 4):
										self.neighbours[0][0][1].addVoxel(Voxel((i + 12, h + 11, j + 12)))
									else:
										self.neighbours[0][2][1].addVoxel(Voxel((i + 12, h + 11, j - 4)))

								else:
									if (j < 4 and npos[1] == 2):
										self.neighbours[2][1][1].addVoxel(Voxel((i - 4, h + 11, j + 12)))
									elif (j > 3 and npos[1] == 0):
										self.neighbours[2][1][1].addVoxel(Voxel((i - 4, h + 11, j - 4)))
									elif (j < 4):
										neighbour[1].addVoxel(Voxel((i - 4, h + 11, j + 12)))
									else:
										neighbour[1].addVoxel(Voxel((i - 4, h + 11, j - 4)))
				neighbour[1].generateMesh()
		self.generateMesh()
		self.propogateNeighbours()

	def propogateNeighbours(self):
		# Scan neighbours and share any non matching adjacent neighbours
		rescan = False
		for x in range(3):
			for y in range(3):
				if (x == 1 and y == 1):
					continue
				
				neighbour = self.neighbours[x][y]
				if (not neighbour[0]):
					continue

				npos = (x, y)
				neighbour = neighbour[1]

				if (npos[0] == 0):
					if (npos[1] == 0):
						# (0,0)'s relative neighbours are (1,2) and (2,1)
						# Which is (0,1) and (1,0) relative to self
						rescan |= self.matchNeighbours(neighbour, (1,2), (0,1))
						rescan |= self.matchNeighbours(neighbour, (2,1), (1,0))

					elif (npos[1] == 1):
						# (0,1)'s relative neighbours are (1,0), (1,2), (2,0), and (2,2)
						# Which is (0,0), (0,2), (1,0), and (1,2) relative to self
						rescan |= self.matchNeighbours(neighbour, (1,0), (0,0))
						rescan |= self.matchNeighbours(neighbour, (1,2), (0,2))
						rescan |= self.matchNeighbours(neighbour, (2,0), (1,0))
						rescan |= self.matchNeighbours(neighbour, (2,2), (1,2))

					else:
						# (0,2)'s relative neighbours are (1,0), and (2,1) 
						# Which is (0,1), and (1,2) relative to self
						rescan |= self.matchNeighbours(neighbour, (1,0), (0,1))
						rescan |= self.matchNeighbours(neighbour, (2,1), (1,2))

				elif (npos[0] == 1):
					if (npos[1] == 0):
						# (1,0)'s relative neighbours are (0,1), (0,2), (2,1), (2,2)
						# Which is (0,0), (0,1), (2,0), (2,1) relative to self
						rescan |= self.matchNeighbours(neighbour, (0,1), (0,0))
						rescan |= self.matchNeighbours(neighbour, (0,2), (0,1))
						rescan |= self.matchNeighbours(neighbour, (2,1), (2,0))
						rescan |= self.matchNeighbours(neighbour, (2,2), (2,1))

					else:
						# (1,2)'s relative neighbours are (0,1), (0,0), (2,1), (2,0)
						# Which is (0,2), (0,1), (2,2), (2,1) relative to self
						rescan |= self.matchNeighbours(neighbour, (0,1), (0,2))
						rescan |= self.matchNeighbours(neighbour, (0,0), (0,1))
						rescan |= self.matchNeighbours(neighbour, (2,1), (2,2))
						rescan |= self.matchNeighbours(neighbour, (2,0), (2,1))

				else:
					if (npos[1] == 0):
						# (2,0)'s relative neighbours are (1,2) and (0,1)
						# Which is (2,1) and (1,0) relative to self
						rescan |= self.matchNeighbours(neighbour, (1,2), (2,1))
						rescan |= self.matchNeighbours(neighbour, (0,1), (1,0))

					elif (npos[1] == 1):
						# (2,1)'s relative neighbours are (0,0), (0,2), (1,0), and (1,2)
						# Which is (1,0), (1,2), (2,0), and (2,2) relative to self
						rescan |= self.matchNeighbours(neighbour, (0,0), (1,0))
						rescan |= self.matchNeighbours(neighbour, (0,2), (1,2))
						rescan |= self.matchNeighbours(neighbour, (1,0), (2,0))
						rescan |= self.matchNeighbours(neighbour, (1,2), (2,2))

					else:
						# (2,2)'s relative neighbours are (0,1) and (1,0)
						# Which is (1,2) and (2,1) relative to self
						rescan |= self.matchNeighbours(neighbour, (0,1), (1,2))
						rescan |= self.matchNeighbours(neighbour, (1,0), (2,1))
				
		if (rescan):
			self.propogateNeighbours()

	def matchNeighbours(self, neighbour, c1, c2):
		rescan = False
		if (neighbour.neighbours[c1[0]][c1[1]][0] and not self.neighbours[c2[0]][c2[1]][0]):
			self.neighbours[c2[0]][c2[1]][0] = True
			self.neighbours[c2[0]][c2[1]][1] = neighbour.neighbours[c1[0]][c1[1]][1]
			rescan = True
		if (self.neighbours[c2[0]][c2[1]][0] and not neighbour.neighbours[c1[0]][c1[1]][0]):
			neighbour.neighbours[c1[0]][c1[1]][0] = True
			neighbour.neighbours[c1[0]][c1[1]][1] = self.neighbours[c2[0]][c2[1]][1]
			rescan = True
		return rescan
		
	def enable(self):
		global player, chunks
		print("Enabled: ", self.pos)
		self.toDisable = True
		self.toEnable = False
		self.enabled = True
		# for x in range(3):
		# 	for y in range(3):
		# 		if (x == 1 and y == 1):
		# 			continue

		# 		neighbour = self.neighbours[x][y]
		# 		if (neighbour[0]):
		# 			continue

		# 		if (x % 2 == 0 and y % 2 == 0):
		# 			continue

		# 		neighbour[0] = True
		# 		neighbour[1] = SurfaceChunk((self.pos[0] + x - 1, self.pos[1] + y - 1), [[(2 - x, 2 - y), self]], globchunks = self.chunks)
		# 		self.chunks.append(neighbour[1])

		# for x in range(2):
		# 	for y in range(2):
		# 		neighbour = self.neighbours[x*2][y*2]
		# 		if (neighbour[0]):
		# 			continue

		# 		neighbour[0] = True
		# 		neighbour[1] = SurfaceChunk((self.pos[0] + 2*x - 1, self.pos[1] + 2*y - 1), [[(2 - 2*x, 2 - 2*y), self], [(2 - 2*x, 1), self.neighbours[1][y*2][1]], [(1, 2 - 2*y), self.neighbours[x*2][1][1]]], globchunks = self.chunks)
		# 		self.chunks.append(neighbour[1])

	def disable(self):
		print("Disabled: ", self.pos)
		self.toDisable = False
		self.toEnable = True
		self.enabled = False