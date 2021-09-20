from ursina import *
from utils.checkNeighbourVoxels import checkNeighbourVoxels
from utils.getTri import getTris
from utils.textureMap import *
from utils.getNormal import getNormal

class Chunk(Button):
    def __init__(self, position = (0,0,0)):
        super().__init__(
            parent = scene,
            position = (16*position[0] - 8, 16*position[1] - 8, 16*position[2] - 8),
            model = Mesh(),
            texture = textureMap,
            collider = 'mesh'
        )
        self.voxels = [[[None for z in range(16)] for y in range(16)] for x in range(16)]
        print("Chunk at: ", self.position)

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
                    vertBase = len(self.model.vertices)
                    self.voxels[x][y][z].vertices = []
                    # verts = [(x + vertex[0], y + vertex[1], z + vertex[2]) for vertex in vertices]
                    # i = 0
                    # count = 0
                    # for vertex in vertices:
                    #     if (verts[count] not in self.model.vertices):
                    #         self.model.vertices.append(verts[count])
                    #         self.voxels[x][y][z].vertices.append(vertex)
                    #         self.voxels[x][y][z].vertIndices.append(vertBase + i)
                    #         i += 1
                    #     count += 1
                    # We now build the triangles and apply UVs and normals from the vertex indices
                    # They are also tracked in the voxel
                    triBase = len(self.model.triangles)
                    tris = getTris(vertices)
                    count = 0
                    for tri in tris:
                        index = vertBase + count
                        self.model.triangles.append(tri)
                        self.voxels[x][y][z].triangles.append(tri)
                        self.voxels[x][y][z].triIndices.append(triBase + count)
                        triangle = unitTriangle(tri, self.model.vertices, (x,y,z))
                        uv = getUV(triangle, self.voxels[x][y][z].texture)
                        self.model.uvs.append(uv[0])
                        self.model.uvs.append(uv[1])
                        self.model.uvs.append(uv[2])
                        self.voxels[x][y][z].uvs.append(uv)
                        self.voxels[x][y][z].uvIndices.append(triBase + count)
                        normal = getNormal(triangle)
                        self.model.normals.append(normal)
                        self.voxels[x][y][z].normals.append(normal)
                        self.voxels[x][y][z].normalIndices.append(triBase + count)
                        count += 1
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
            print(pos)
            if key == 'right mouse down':
                print(pos)
                punch_sound.play()
                if block_pick == 1: self.addVoxel(Voxel(position = pos, texture = 'assets/grass_block.png'))
                if block_pick == 2: self.addVoxel(Voxel(position = pos, texture = 'assets/stone_block.png'))
                if block_pick == 3: self.addVoxel(Voxel(position = pos, texture = 'assets/brick_block.png'))
                if block_pick == 4: self.addVoxel(Voxel(position = pos, texture = 'assets/dirt_block.png'))
                self.generateMesh()

            if key == 'left mouse down':
                punch_sound.play()
                normal = mouse.normal
                if (normal[0] > 0 or normal[1] > 0 or normal[2] > 0):
                    pos = (pos[0] - normal[0], pos[1] - normal[1], pos[2] - normal[2])
                self.removeVoxel(pos)
                print(pos)
                self.generateMesh()
                        
def unitTriangle(tri, vertices, pos):
    v1 = vertices[tri[0]]
    v2 = vertices[tri[1]]
    v3 = vertices[tri[2]]
    if (pos[0] == 1):
        v1 = (v1[0] - 1, v1[1], v1[2])
        v2 = (v2[0] - 1, v2[1], v2[2])
        v3 = (v3[0] - 1, v3[1], v3[2])
    if (pos[0] > 1):
        v1 = (v1[0] % pos[0], v1[1], v1[2])
        v2 = (v2[0] % pos[0], v2[1], v2[2])
        v3 = (v3[0] % pos[0], v3[1], v3[2])
    if (pos[1] == 1):
        v1 = (v1[0], v1[1] - 1, v1[2])
        v2 = (v2[0], v2[1] - 1, v2[2])
        v3 = (v3[0], v3[1] - 1, v3[2])
    if (pos[1] > 1):
        v1 = (v1[0], v1[1] % pos[1], v1[2])
        v2 = (v2[0], v2[1] % pos[1], v2[2])
        v3 = (v3[0], v3[1] % pos[1], v3[2])
    if (pos[2] == 1):
        v1 = (v1[0], v1[1], v1[2] - 1)
        v2 = (v2[0], v2[1], v2[2] - 1)
        v3 = (v3[0], v3[1], v3[2] - 1)
    if (pos[2] > 1):
        v1 = (v1[0], v1[1], v1[2] % pos[2])
        v2 = (v2[0], v2[1], v2[2] % pos[2])
        v3 = (v3[0], v3[1], v3[2] % pos[2])
    return (v1, v2, v3)