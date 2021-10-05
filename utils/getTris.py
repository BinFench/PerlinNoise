def getTris(vertices, vbase):
    # For a set of vertices, generate every possible triangle on a cube
    tris = []
    usedVert = [[[False for i in range(2)] for j in range(2)] for k in range(2)]
    stop = len(vertices)
    count = 0
    for vertex in vertices:
        if (count == stop):
            break
        count += 1
        # Another state machine.  May refactor later
        if (vertex == (0,0,0)):
            if ((0,0,1) in vertices and (0,1,0) in vertices):
                usedVert[0][0][0] = True
                usedVert[0][0][1] = True
                usedVert[0][1][0] = True
                tris.append((
                            vbase + getIndex((0,0,0), vertices),
                            vbase + getIndex((0,0,1), vertices),
                            vbase + getIndex((0,1,0), vertices)))

                if ((0,1,1) in vertices):
                    usedVert[0][1][1] = True
                    tris.append((
                                vbase + getIndex((0,0,1), vertices),
                                vbase + getIndex((0,1,0), vertices),
                                vbase + getIndex((0,1,1), vertices)))

            if ((0,1,0) in vertices and (1,0,0) in vertices):
                if (usedVert[0][0][0]):
                    i = len(vertices)
                    vertices.append((0,0,0))
                else:
                    i = getIndex((0,0,0), vertices)
                if (usedVert[0][1][0]):
                    j = len(vertices)
                    vertices.append((0,1,0))
                else:
                    j = getIndex((0,1,0), vertices)
                
                usedVert[0][0][0] = True
                usedVert[0][1][0] = True
                usedVert[1][0][0] = True
                
                tris.append((
                            vbase + i,
                            vbase + j,
                            vbase + getIndex((1,0,0), vertices)))

                if ((1,1,0) in vertices):
                    usedVert[1][1][0] = True
                    tris.append((
                                vbase + j,
                                vbase + getIndex((1,0,0), vertices),
                                vbase + getIndex((1,1,0), vertices)))

            if ((0,0,1) in vertices and (1,0,0) in vertices):
                if (usedVert[0][0][0]):
                    i = len(vertices)
                    vertices.append((0,0,0))
                else:
                    i = getIndex((0,0,0), vertices)
                if (usedVert[0][0][1]):
                    j = len(vertices)
                    vertices.append((0,0,1))
                else:
                    j = getIndex((0,0,1), vertices)
                if (usedVert[1][0][0]):
                    k = len(vertices)
                    vertices.append((1,0,0))
                else:
                    k = getIndex((1,0,0), vertices)

                usedVert[0][0][0] = True
                usedVert[0][0][1] = True
                usedVert[1][0][0] = True

                tris.append((
                            vbase + i,
                            vbase + j,
                            vbase + k))

                if ((1,0,1) in vertices):
                    usedVert[1][0][1] = True
                    tris.append((
                                vbase + j,
                                vbase + k,
                                vbase + getIndex((1,0,1), vertices)))

        elif (vertex == (0,0,1)):
            if ((0,1,1) in vertices and (1,0,1) in vertices):
                if (usedVert[0][0][1]):
                    i = len(vertices)
                    vertices.append((0,0,1))
                else:
                    i = getIndex((0,0,1), vertices)
                if (usedVert[0][1][1]):
                    j = len(vertices)
                    vertices.append((0,1,1))
                else:
                    j = getIndex((0,1,1), vertices)
                if (usedVert[1][0][1]):
                    k = len(vertices)
                    vertices.append((1,0,1))
                else:
                    k = getIndex((1,0,1), vertices)

                usedVert[0][0][1] = True
                usedVert[0][1][1] = True
                usedVert[1][0][1] = True

                tris.append((
                            vbase + i,
                            vbase + j,
                            vbase + k))

                if ((1,1,1) in vertices):
                    usedVert[1][1][1] = True
                    tris.append((
                                vbase + j,
                                vbase + k,
                                vbase + getIndex((1,1,1), vertices)))

        elif (vertex == (0,1,0)):
            if ((0,1,1) in vertices and (1,1,0) in vertices):
                if (usedVert[0][1][0]):
                    i = len(vertices)
                    vertices.append((0,1,0))
                else:
                    i = getIndex((0,1,0), vertices)
                if (usedVert[0][1][1]):
                    j = len(vertices)
                    vertices.append((0,1,1))
                else:
                    j = getIndex((0,1,1), vertices)
                if (usedVert[1][1][0]):
                    k = len(vertices)
                    vertices.append((1,1,0))
                else:
                    k = getIndex((1,1,0), vertices)

                usedVert[0][1][0] = True
                usedVert[0][1][1] = True
                usedVert[1][1][0] = True

                tris.append((
                            vbase + i,
                            vbase + j,
                            vbase + k))

                if ((1,1,1) in vertices):
                    if (usedVert[1][1][1]):
                        i = len(vertices)
                        vertices.append((1,1,1))
                    else:
                        i = getIndex((1,1,1), vertices)
                    
                    usedVert[1][1][1] = True

                    tris.append((
                                vbase + j,
                                vbase + k,
                                vbase + i))

        elif (vertex == (1,0,0)):
            if ((1,0,1) in vertices and (1,1,0) in vertices):
                if (usedVert[1][0][0]):
                    i = len(vertices)
                    vertices.append((1,0,0))
                else:
                    i = getIndex((1,0,0), vertices)
                if (usedVert[1][0][1]):
                    j = len(vertices)
                    vertices.append((1,0,1))
                else:
                    j = getIndex((1,0,1), vertices)
                if (usedVert[1][1][0]):
                    k = len(vertices)
                    vertices.append((1,1,0))
                else:
                    k = getIndex((1,1,0), vertices)

                usedVert[1][0][0] = True
                usedVert[1][0][1] = True
                usedVert[1][1][0] = True

                tris.append((
                            vbase + i,
                            vbase + j,
                            vbase + k))

                if ((1,1,1) in vertices):
                    if (usedVert[1][1][1]):
                        i = len(vertices)
                        vertices.append((1,1,1))
                    else:
                        i = getIndex((1,1,1), vertices)
                    usedVert[1][1][1] = True

                    tris.append((
                                vbase + j,
                                vbase + k,
                                vbase + i))

    return tris
    
def getIndex(vertex, vertices):
    return vertices.index(vertex)