from ursina import *
from worldgen.Chunk import Chunk
from worldgen.blocks import *
from worldgen.Biome import Biome

class SurfaceChunk(Chunk):
	def __init__(self, biome, position = (0,0), neighbours = [], globchunks = []):
		super().__init__(position=(position[0], 0, position[1]))
		self.biome = biome
		self.nmap = biome.getChunk(position)
		self.neighbours = [[[False, None] for i in range(3)] for j in range(3)]
		self.corners = [[False for i in range(2)] for i in range(2)]
		self.neighbours[1][1] = [True, self]
		self.spos = position
		self.chunks = globchunks
		self.chunks.append(self)
		self.scanned = [[False for i in range(3)] for j in range(3)]

		for neighbour in neighbours:
			self.neighbours[neighbour[0][0]][neighbour[0][1]] = [True, neighbour[1]]
			neighbour[1].neighbours[2-neighbour[0][0]][2-neighbour[0][1]] = [True, self]

		for i in range(16):
			for j in range(16):
				for h in range(int(self.nmap[i][j]*1.5)):
					if (h == int(self.nmap[i][j]*1.5) - 1):
						self.addVoxel(GrassBlock(position=(i, h + 11, j), chunk=self))
					else:
						self.addVoxel(DirtBlock(position=(i, h + 11, j), chunk=self))
				for h in range(11):
					self.addVoxel(StoneBlock(position=(i, h, j), chunk=self))

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

				if (self.scanned[x][y]):
					continue

				self.scanned[x][y] = True

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
		self.enabled = True
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
				neighbour[1] = SurfaceChunk(self.biome, (self.spos[0] + x - 1, self.spos[1] + y - 1), [[(2 - x, 2 - y), self]], globchunks = self.chunks)
				self.chunks.append(neighbour[1])

		for x in range(2):
			for y in range(2):
				neighbour = self.neighbours[x*2][y*2]
				if (neighbour[0]):
					continue

				neighbour[0] = True
				neighbour[1] = SurfaceChunk(self.biome, (self.spos[0] + 2*x - 1, self.spos[1] + 2*y - 1), [[(2 - 2*x, 2 - 2*y), self], [(2 - 2*x, 1), self.neighbours[1][y*2][1]], [(1, 2 - 2*y), self.neighbours[x*2][1][1]]], globchunks = self.chunks)
				self.chunks.append(neighbour[1])

	def disable(self):
		self.enabled = False