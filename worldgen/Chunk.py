from ursina import *
from utils import *
from worldgen.blocks import *

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
        self.vertices = []
        self.triangles = []
        self.uvs = []
        self.normals = []
        self.generated = False

    def generateMesh(self):
        self.vertices = []
        self.triangles = []
        self.uvs = []
        self.normals = []
        vbase = 0
        for x in range(16):
            for y in range(16):
                for z in range(16):
                    if (self.voxels[x][y][z] is None):
                        continue
                    vbase = self.voxels[x][y][z].getMesh(vbase)

        self.initMesh(self.vertices, self.triangles, self.normals, self.uvs)
        self.generated = True

    def initMesh(self, fvertices, triangles, normals, uvs):
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
        pos = voxel.position
        if (pos[0] < 0 or pos[0] > 15 or pos[1] < 0 or  pos[1] > 15 or pos[2] < 0 or pos[2] > 15):
            return False

        toRet = self.voxels[pos[0]][pos[1]][pos[2]] is None
        if (toRet):
            self.voxels[pos[0]][pos[1]][pos[2]] = voxel
            if (self.generated):
                voxel.generateSubMesh()
                if (pos[0] != 0 and self.voxels[pos[0] - 1][pos[1]][pos[2]] is not None):
                    self.voxels[pos[0] - 1][pos[1]][pos[2]].generateSubMesh()
                if (pos[0] != 15 and self.voxels[pos[0] + 1][pos[1]][pos[2]] is not None):
                    self.voxels[pos[0] + 1][pos[1]][pos[2]].generateSubMesh()
                if (pos[1] != 0 and self.voxels[pos[0]][pos[1] - 1][pos[2]] is not None):
                    self.voxels[pos[0]][pos[1] - 1][pos[2]].generateSubMesh()
                if (pos[1] != 15 and self.voxels[pos[0]][pos[1] + 1][pos[2]] is not None):
                    self.voxels[pos[0]][pos[1] + 1][pos[2]].generateSubMesh()
                if (pos[2] != 0 and self.voxels[pos[0]][pos[1]][pos[2] - 1] is not None):
                    self.voxels[pos[0]][pos[1]][pos[2] - 1].generateSubMesh()
                if (pos[2] != 15 and self.voxels[pos[0]][pos[1]][pos[2] + 1] is not None):
                    self.voxels[pos[0]][pos[1]][pos[2] + 1].generateSubMesh()
        return toRet

    def removeVoxel(self, pos):
        if (pos[0] < 0 or pos[0] > 15 or pos[1] < 0 or  pos[1] > 15 or pos[2] < 0 or pos[2] > 15):
            return False
        toRet = self.voxels[pos[0]][pos[1]][pos[2]] is not None
        self.voxels[pos[0]][pos[1]][pos[2]] = None
        if (toRet):
            if (self.generated):
                if (pos[0] != 0 and self.voxels[pos[0] - 1][pos[1]][pos[2]] is not None):
                    self.voxels[pos[0] - 1][pos[1]][pos[2]].generateSubMesh()
                if (pos[0] != 15 and self.voxels[pos[0] + 1][pos[1]][pos[2]] is not None):
                    self.voxels[pos[0] + 1][pos[1]][pos[2]].generateSubMesh()
                if (pos[1] != 0 and self.voxels[pos[0]][pos[1] - 1][pos[2]] is not None):
                    self.voxels[pos[0]][pos[1] - 1][pos[2]].generateSubMesh()
                if (pos[1] != 15 and self.voxels[pos[0]][pos[1] + 1][pos[2]] is not None):
                    self.voxels[pos[0]][pos[1] + 1][pos[2]].generateSubMesh()
                if (pos[2] != 0 and self.voxels[pos[0]][pos[1]][pos[2] - 1] is not None):
                    self.voxels[pos[0]][pos[1]][pos[2] - 1].generateSubMesh()
                if (pos[2] != 15 and self.voxels[pos[0]][pos[1]][pos[2] + 1] is not None):
                    self.voxels[pos[0]][pos[1]][pos[2] + 1].generateSubMesh()
        return toRet

    def input(self,key):
        global block_pick
        if self.hovered:
            pos = mouse.point
            pos = (int(pos[0]), int(pos[1]), int(pos[2]))
            if key == 'right mouse down':
                punch_sound.play()
                normal = mouse.normal
                while (not self.addVoxel(pickBlock(block_pick)(position=pos,chunk=self))):
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