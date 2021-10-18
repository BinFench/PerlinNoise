from ursina import *
from utils import *

class Voxel():
    def __init__(self, position = (0,0,0), texture = 'assets/grass_block.png', chunk = None):
        self.chunk = chunk
        self.vertices = []
        self.vertIndices = []
        self.triangles = []
        self.triIndices = []
        self.uvs = []
        self.uvIndices = []
        self.normals = []
        self.normalIndices = []
        self.texture = texture
        self.position = position
        self.generated = False
        if (chunk is None):
            self.generateMesh()

    def generateMesh(self):
        self.vertices = [(0, 0, 0), (0, 0, 1),
                         (0, 1, 0), (0, 1, 1),
                         (1, 0, 0), (1, 0, 1),
                         (1, 1, 0), (1, 1, 1)]
        self.triangles = getTris(self.vertices, 0)
        self.uvs = [(0,0) for i in range(len(self.vertices))]
        self.normals = [(0,0,0) for i in range(len(self.vertices))]
        for tri in self.triangles:
                uv = getUV((self.vertices[tri[0]], self.vertices[tri[1]], self.vertices[tri[2]]), self.texture)
                self.uvs[tri[0]] = uv[0]
                self.uvs[tri[1]] = uv[1]
                self.uvs[tri[2]] = uv[2]
                normal = getNormal((self.vertices[tri[0]], self.vertices[tri[1]], self.vertices[tri[2]]))
                self.normals[tri[0]] = normal
                self.normals[tri[1]] = normal
                self.normals[tri[2]] = normal

    def generateSubMesh(self):
        self.vertices = [(0, 0, 0), (0, 0, 1),
                         (0, 1, 0), (0, 1, 1),
                         (1, 0, 0), (1, 0, 1),
                         (1, 1, 0), (1, 1, 1)]
        pos = self.position

        if (pos[0] != 0 and self.chunk.voxels[pos[0] - 1][pos[1]][pos[2]] is not None):
            if (pos[1] != 0 and self.chunk.voxels[pos[0]][pos[1] - 1][pos[2]] is not None):
                if (pos[2] != 0 and self.chunk.voxels[pos[0]][pos[1]][pos[2] - 1] is not None):
                    self.vertices.remove((0,0,0))
                if (pos[2] != 15 and self.chunk.voxels[pos[0]][pos[1]][pos[2] + 1] is not None):
                    self.vertices.remove((0,0,1))
            if (pos[1] != 15 and self.chunk.voxels[pos[0]][pos[1] + 1][pos[2]] is not None):
                if (pos[2] != 0 and self.chunk.voxels[pos[0]][pos[1]][pos[2] - 1] is not None):
                    self.vertices.remove((0,1,0))
                if (pos[2] != 15 and self.chunk.voxels[pos[0]][pos[1]][pos[2] + 1] is not None):
                    self.vertices.remove((0,1,1))
        if (pos[0] != 15 and self.chunk.voxels[pos[0] + 1][pos[1]][pos[2]] is not None):
            if (pos[1] != 0 and self.chunk.voxels[pos[0]][pos[1] - 1][pos[2]] is not None):
                if (pos[2] != 0 and self.chunk.voxels[pos[0]][pos[1]][pos[2] - 1] is not None):
                    self.vertices.remove((1,0,0))
                if (pos[2] != 15 and self.chunk.voxels[pos[0]][pos[1]][pos[2] + 1] is not None):
                    self.vertices.remove((1,0,1))
            if (pos[1] != 15 and self.chunk.voxels[pos[0]][pos[1] + 1][pos[2]] is not None):
                if (pos[2] != 0 and self.chunk.voxels[pos[0]][pos[1]][pos[2] - 1] is not None):
                    self.vertices.remove((1,1,0))
                if (pos[2] != 15 and self.chunk.voxels[pos[0]][pos[1]][pos[2] + 1] is not None):
                    self.vertices.remove((1,1,1))

        if (len(self.vertices) != 0):
            self.triangles = getTris(self.vertices, 0)
            self.uvs = [(0,0) for i in range(len(self.vertices))]
            self.normals = [(0,0,0) for i in range(len(self.vertices))]
            for tri in self.triangles:
                uv = getUV((self.vertices[tri[0]], self.vertices[tri[1]], self.vertices[tri[2]]), self.texture)
                self.uvs[tri[0]] = uv[0]
                self.uvs[tri[1]] = uv[1]
                self.uvs[tri[2]] = uv[2]
                normal = getNormal((self.vertices[tri[0]], self.vertices[tri[1]], self.vertices[tri[2]]))
                self.normals[tri[0]] = normal
                self.normals[tri[1]] = normal
                self.normals[tri[2]] = normal
            return True
        
        self.clearGeometry()
        return False

    def getMesh(self, vbase):
        if (self.chunk is not None and (self.generated or self.generateSubMesh())):
            pos = self.position
            for vert in self.vertices:
                self.chunk.vertices.append((vert[0] + pos[0], vert[1] + pos[1], vert[2] + pos[2]))
            for tri in self.triangles:
                self.chunk.triangles.append((tri[0] + vbase, tri[1] + vbase, tri[2] + vbase))
            self.chunk.uvs.extend(self.uvs)
            self.chunk.normals.extend(self.normals)
            return len(self.chunk.vertices)
        return vbase
                

    def clearGeometry(self):
        self.vertices = []
        self.vertIndices = []
        self.triangles = []
        self.triIndices = []
        self.uvs = []
        self.uvIndices = []
        self.normals = []
        self.normalIndices = []