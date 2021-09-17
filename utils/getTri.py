def getTris(vertices, verts, model):
    tris = []
    for vertex in vertices:
        # Another state machine.  May refactor later
        if (vertex == (0,0,0)):
            if ((0,0,1) in vertices and (0,1,0) in vertices):
                tris.append((
                            getIndex((0,0,0), vertices, verts, model),
                            getIndex((0,0,1), vertices, verts, model),
                            getIndex((0,1,0), vertices, verts, model)))

            if ((0,1,0) in vertices and (1,0,0) in vertices):
                tris.append((
                            getIndex((0,0,0), vertices, verts, model),
                            getIndex((0,1,0), vertices, verts, model),
                            getIndex((1,0,0), vertices, verts, model)))

            if ((0,0,1) in vertices and (1,0,0) in vertices):
                tris.append((
                            getIndex((0,0,0), vertices, verts, model),
                            getIndex((0,0,1), vertices, verts, model),
                            getIndex((1,0,0), vertices, verts, model)))

        elif (vertex == (0,0,1)):
            if ((0,1,0) in vertices and (0,1,1) in vertices):
                tris.append((
                            getIndex((0,0,1), vertices, verts, model),
                            getIndex((0,1,0), vertices, verts, model),
                            getIndex((0,1,1), vertices, verts, model)))

            if ((0,1,1) in vertices and (1,0,1) in vertices):
                tris.append((
                            getIndex((0,0,1), vertices, verts, model),
                            getIndex((0,1,1), vertices, verts, model),
                            getIndex((1,0,1), vertices, verts, model)))

            if ((1,0,0) in vertices and (1,0,1) in vertices):
                tris.append((
                            getIndex((0,0,1), vertices, verts, model),
                            getIndex((1,0,0), vertices, verts, model),
                            getIndex((1,0,1), vertices, verts, model)))

        elif (vertex == (0,1,0)):
            if ((1,0,0) in vertices and (1,1,0) in vertices):
                tris.append((
                            getIndex((0,1,0), vertices, verts, model),
                            getIndex((1,0,0), vertices, verts, model),
                            getIndex((1,1,0), vertices, verts, model)))

            if ((0,1,1) in vertices and (1,1,0) in vertices):
                tris.append((
                            getIndex((0,1,0), vertices, verts, model),
                            getIndex((0,1,1), vertices, verts, model),
                            getIndex((1,1,0), vertices, verts, model)))

        elif (vertex == (0,1,1)):
            if ((1,0,1) in vertices and (1,1,1) in vertices):
                tris.append((
                            getIndex((0,1,1), vertices, verts, model),
                            getIndex((1,0,1), vertices, verts, model),
                            getIndex((1,1,1), vertices, verts, model)))

            if ((1,1,0) in vertices and (1,1,1) in vertices):
                tris.append((
                            getIndex((0,1,1), vertices, verts, model),
                            getIndex((1,1,0), vertices, verts, model),
                            getIndex((1,1,1), vertices, verts, model)))

        elif (vertex == (1,0,0)):
            if ((1,0,1) in vertices and (1,1,0) in vertices):
                tris.append((
                            getIndex((1,0,0), vertices, verts, model),
                            getIndex((1,0,1), vertices, verts, model),
                            getIndex((1,1,0), vertices, verts, model)))

        elif (vertex == (1,0,1)):
            if ((1,1,0) in vertices and (1,1,1) in vertices):
                tris.append((
                            getIndex((1,0,1), vertices, verts, model),
                            getIndex((1,1,0), vertices, verts, model),
                            getIndex((1,1,1), vertices, verts, model)))

    return tris
    
def getIndex(vertex, vertices, verts, model):
    return model.vertices.index(verts[vertices.index(vertex)])