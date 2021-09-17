from ursina import *
from ...utils import checkNeighbourVoxels, getTris
from ...utils.textureMap import *

class Chunk(Button):
    def __init__(self, position = (0,0,0)):
        super().__init__(
			parent = scene,
			position = (16*position[0] - 8, 16*position[1] - 8, 16*position[2] - 8),
            model = Mesh(),
            texture = textureMap
        )
        self.voxels = [[[None for z in range(16)] for y in range(16)] for x in range(16)]

    def generateMesh(self):
        # First, we make a pass generating all the vertices and assigning them to voxels
        self.model.vertices = []
        self.model.triangles = []
        self.model.uvs = []
        for x in range(16):
            for y in range(16):
                for z in range(16):
                    if (self.voxels[x][y][z] is None):
                        continue

                    self.voxels[x][y][z].clearGeometry()
                    vertices = checkNeighbourVoxels(x, y, z, self.voxels)
                        
                    # The vertices are filtered.  We can now shape and texture the mesh
                    # Begin by appending the vertices to the model,
                    # and keeping track of them in the voxel.
                    vertBase = self.model.vertices.lengths
                    self.voxels[x][y][z].vertices = []
                    verts = [x + vertex[0], y + vertex[1], z + vertex[2]) for vertex in vertices]
                    i = 0
                    for vertex, count in vertices:
                        if (verts[count] not in self.model.vertices):
                            self.model.vertices.append(verts[count])
                            self.voxels[x][y][z].vertices.append(vertex)
                            self.voxels[x][y][x].vertIndices.append(vertBase + i)
                            i += 1
                    # We now build the triangles and apply UVs from the vertex indices
                    # They are also tracked in the voxel
                    triBase = self.model.triangles.lengths
                    tris = getTris(vertices, verts, self.model)
                    for tri, count in tris:
                        index = vertBase + count
                        self.model.triangles.append(tri)
                        self.voxels[x][y][z].triangles.append(tri)
                        self.voxels[x][y][z].triIndices.append(triBase + count)
                        uv = getUV(unitTriangle(tri, self.model.vertices, (x,y,z)), self.voxels[x][y][z].texture)
                        self.model.uvs.append(uv)
                        self.voxels[x][y][z].uvs.append(uv)
                        self.voxels[x][y][z].uvIndices.append(triBase + count)
        self.model.generate()

    def addVoxel(self, voxel):
        voxel.chunk = self
        pos = voxel.position
        self.voxels[pos[0]][pos[1]][pos[2]] = voxel

    def removeVoxel(self, pos):
        self.voxels[pos[0]][pos[1]][pos[2]] = None

    def input(self,key):
		if self.hovered:
            pos = mouse.point
            pos = (int(pos[0]), int(pos[1]), int(pos[2]))
			if key == 'right mouse down':
				punch_sound.play()
				if block_pick == 1: self.addVoxel(Voxel(position = pos, texture = 'assets/grass_block.png'))
				if block_pick == 2: self.addVoxel(Voxel(position = pos, texture = 'assets/stone_block.png'))
				if block_pick == 3: self.addVoxel(Voxel(position = pos, texture = 'assets/brick_block.png'))
				if block_pick == 4: self.addVoxel(Voxel(position = pos, texture = 'assets/dirt_block.png'))

			if key == 'left mouse down':
				punch_sound.play()
				
                        
def unitTriangle(tri, vertices, pos):
    v1 = vertices[tri[0]]
    v2 = vertices[tri[1]]
    v3 = vertices[tri[2]]
    v = (v1, v2, v3)
    return ((ve[i] % pos[i] for i in range(3)) for ve in v)