from ursina import *
from utils import *
from worldgen.Voxel import Voxel

chunkTexture = load_texture('assets/textureMap.png')
punch_sound = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 0

def set_block_pick(pick):
    global block_pick
    block_pick = pick

class Chunk(Entity):
    def __init__(self, position = (0,0,0)):
        self.pos = position
        self.voxels = [[[None for z in range(16)] for y in range(16)] for x in range(16)]

    def generateMesh(self):
        # First, we make a pass generating all the vertices and assigning them to voxels
        fvertices = []
        triangles = []
        uvs = []
        normals = []
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
                    vertBase = len(fvertices)
                    self.voxels[x][y][z].vertices = []
                    verts = [(x + vertex[0], y + vertex[1], z + vertex[2]) for vertex in vertices]
                    i = 0
                    for vertex in vertices:
                        fvertices.append(verts[i])
                        self.voxels[x][y][z].vertices.append(vertex)
                        self.voxels[x][y][z].vertIndices.append(vertBase + i)
                        i += 1
                        uvs.append((0,0))
                        normals.append((0,0,0))
                    # We now build the triangles and apply UVs and normals from the vertex indices
                    # They are also tracked in the voxel
                    triBase = len(triangles)
                    prevLen = len(vertices)
                    tris = getTris(vertices, vertBase)
                    diffLen = len(vertices) - prevLen
                    for i in range(diffLen):
                        fvertices.append((x + vertices[prevLen + i][0], y + vertices[prevLen + i][1], z + vertices[prevLen + i][2]))
                        uvs.append((0,0))
                        normals.append((0,0,0))
                    count = 0
                    for tri in tris:
                        index = vertBase + count
                        triangles.append(tri)
                        self.voxels[x][y][z].triangles.append(tri)
                        self.voxels[x][y][z].triIndices.append(triBase + count)
                        triangle = unitTriangle(tri, fvertices, (x,y,z))
                        uv = getUV(triangle, self.voxels[x][y][z].texture)
                        uvs[tri[0]] = uv[0]
                        uvs[tri[1]] = uv[1]
                        uvs[tri[2]] = uv[2]
                        self.voxels[x][y][z].uvs.append(uv)
                        self.voxels[x][y][z].uvIndices.append(triBase + count)
                        normal = getNormal(triangle)
                        normals[tri[0]] = normal
                        normals[tri[1]] = normal
                        normals[tri[2]] = normal
                        self.voxels[x][y][z].normals.append(normal)
                        self.voxels[x][y][z].normalIndices.append(triBase + count)
                        count += 1
        super().__init__(
            parent = scene,
            position = (16*self.pos[0] - 8, 16*self.pos[1] - 8, 16*self.pos[2] - 8),
            model = Mesh(vertices=fvertices, triangles=triangles, normals=normals, uvs=uvs),
            texture = chunkTexture,
            collider = 'mesh',
            collision = True,
            double_sided = True
        )

    def addVoxel(self, voxel):
        voxel.chunk = self
        pos = voxel.position
        if (pos[0] < 0 or pos[0] > 15 or pos[1] < 0 or  pos[1] > 15 or pos[2] < 0 or pos[2] > 15):
            return False

        toRet = self.voxels[pos[0]][pos[1]][pos[2]] is None
        if (toRet):
            self.voxels[pos[0]][pos[1]][pos[2]] = voxel
        return toRet

    def removeVoxel(self, pos):
        if (pos[0] < 0 or pos[0] > 15 or pos[1] < 0 or  pos[1] > 15 or pos[2] < 0 or pos[2] > 15):
            return False
        toRet = self.voxels[pos[0]][pos[1]][pos[2]] is not None
        self.voxels[pos[0]][pos[1]][pos[2]] = None
        return toRet

    def input(self,key):
        global block_pick
        if self.hovered:
            pos = mouse.point
            pos = (int(pos[0]), int(pos[1]), int(pos[2]))
            if key == 'right mouse down':
                punch_sound.play()
                normal = mouse.normal
                while (not self.addVoxel(Voxel(position = pos, texture = list(Texture)[block_pick].name))):
                    if (normal[0] > 0 or normal[1] > 0 or normal[2] > 0):
                        pos = (int(pos[0] - normal[0]), int(pos[1] - normal[1]), int(pos[2] - normal[2]))
                    else:
                        pos = (int(pos[0] + normal[0]), int(pos[1] + normal[1]), int(pos[2] + normal[2]))
                    if (pos[0] < 0 or  pos[0] > 15 or pos[1] < 0 or  pos[1] > 15 or pos[2] < 0 or  pos[2] > 15):
                        break
                self.generateMesh()

            if key == 'left mouse down':
                punch_sound.play()
                normal = mouse.normal
                while (not self.removeVoxel(pos)):
                    if (normal[0] > 0 or normal[1] > 0 or normal[2] > 0):
                        pos = (int(pos[0] - normal[0]), int(pos[1] - normal[1]), int(pos[2] - normal[2]))
                    else:
                        pos = (int(pos[0] + normal[0]), int(pos[1] + normal[1]), int(pos[2] + normal[2]))
                    if (pos[0] < 0 or  pos[0] > 15 or pos[1] < 0 or  pos[1] > 15 or pos[2] < 0 or  pos[2] > 15):
                        break
                self.generateMesh()