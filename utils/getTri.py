def getTris(vertices):
    tris = []
    for vertex in vertices:
        # Another state machine.  May refactor later
        if (vertex == (0,0,0)):
            if ((0,0,1) in vertices and (0,1,0) in vertices):
                tris.append((
                            getIndex((0,0,0), vertices),
                            getIndex((0,0,1), vertices),
                            getIndex((0,1,0), vertices)))

            if ((0,1,0) in vertices and (1,0,0) in vertices):
                tris.append((
                            getIndex((0,0,0), vertices),
                            getIndex((0,1,0), vertices),
                            getIndex((1,0,0), vertices)))

            if ((0,0,1) in vertices and (1,0,0) in vertices):
                tris.append((
                            getIndex((0,0,0), vertices),
                            getIndex((0,0,1), vertices),
                            getIndex((1,0,0), vertices)))

        elif (vertex == (0,0,1)):
            if ((0,1,0) in vertices and (0,1,1) in vertices):
                tris.append((
                            getIndex((0,0,1), vertices),
                            getIndex((0,1,0), vertices),
                            getIndex((0,1,1), vertices)))

            if ((0,1,1) in vertices and (1,0,1) in vertices):
                tris.append((
                            getIndex((0,0,1), vertices),
                            getIndex((0,1,1), vertices),
                            getIndex((1,0,1), vertices)))

            if ((1,0,0) in vertices and (1,0,1) in vertices):
                tris.append((
                            getIndex((0,0,1), vertices),
                            getIndex((1,0,0), vertices),
                            getIndex((1,0,1), vertices)))

        elif (vertex == (0,1,0)):
            if ((1,0,0) in vertices and (1,1,0) in vertices):
                tris.append((
                            getIndex((0,1,0), vertices),
                            getIndex((1,0,0), vertices),
                            getIndex((1,1,0), vertices)))

            if ((0,1,1) in vertices and (1,1,0) in vertices):
                tris.append((
                            getIndex((0,1,0), vertices),
                            getIndex((0,1,1), vertices),
                            getIndex((1,1,0), vertices)))

        elif (vertex == (0,1,1)):
            if ((1,0,1) in vertices and (1,1,1) in vertices):
                tris.append((
                            getIndex((0,1,1), vertices),
                            getIndex((1,0,1), vertices),
                            getIndex((1,1,1), vertices)))

            if ((1,1,0) in vertices and (1,1,1) in vertices):
                tris.append((
                            getIndex((0,1,1), vertices),
                            getIndex((1,1,0), vertices),
                            getIndex((1,1,1), vertices)))

        elif (vertex == (1,0,0)):
            if ((1,0,1) in vertices and (1,1,0) in vertices):
                tris.append((
                            getIndex((1,0,0), vertices),
                            getIndex((1,0,1), vertices),
                            getIndex((1,1,0), vertices)))

        elif (vertex == (1,0,1)):
            if ((1,1,0) in vertices and (1,1,1) in vertices):
                tris.append((
                            getIndex((1,0,1), vertices),
                            getIndex((1,1,0), vertices),
                            getIndex((1,1,1), vertices)))

    return tris
    
def getIndex(vertex, vertices):
    return vertices.index(vertex)