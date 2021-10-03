from ursina import *

vertices = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1),
            (0,0,0), (0,1,0), (0,0,0), (0,0,1), (1,0,0), (0,0,1), (0,1,1), (1,0,1),
            (0,1,0), (0,1,1), (1,1,0), (1,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]

triangles = [(0,1,2), (1,2,3), (8,9,4), (9,4,6), (10,11,12), (11,12,5), (13,14,15),
             (14,15,7), (16,17,18), (17,18,19), (20,21,22), (21,22,23)]

normals = [(-1,0,0), (-1,0,0), (-1,0,0), (-1,0,0), (0,0,-1), (0,-1,0), (0,0,-1),
           (0,0,1), (0,0,-1), (0,0,-1), (0,-1,0), (0,-1,0), (0,-1,0), (0,0,1),
           (0,0,1), (0,0,1), (0,1,0), (0,1,0), (0,1,0), (0,1,0), (1,0,0),
           (1,0,0), (1,0,0), (1,0,0)]

uvs = [(0.375, 0.75), (0.375, 1), (0.625, 0.75), (0.625, 1), (0.375, 0.5), (0.125, 0.5),
       (0.625, 0.25), (0.625, 0.25), (0.375, 0.75), (0.625, 0.75), (0.375, 0.75), (0.125, 0.75),
       (0.375, 0.5), (0.375, 0), (0.625, 0), (0.375, 0.25), (0.625, 0.75), (0.875, 0.75),
       (0.625, 0.5), (0.875, 0.5), (0.375, 0.5), (0.375, 0.25), (0.625, 0.5), (0.625, 0.25)]

class CubeMesh(Entity):
    def __init__(self, position = (0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = Mesh(vertices=vertices, triangles=triangles, normals=normals, uvs=uvs),
            texture = load_texture('assets/grass_block.png'),
            collider = 'mesh',
            collision = True,
            double_sided = True
        )
        for tri in self.model.triangles:
            print("Tri: ", tri)
            print("#1: ", self.model.vertices[tri[0]], self.model.uvs[tri[0]], self.model.normals[tri[0]])
            print("#2: ", self.model.vertices[tri[1]], self.model.uvs[tri[1]], self.model.normals[tri[1]])
            print("#3: ", self.model.vertices[tri[2]], self.model.uvs[tri[2]], self.model.normals[tri[2]])