def unitTriangle(tri, vertices, pos):
    # For a given triangle and position, determine its shape as a unit triangle
    # e.g. all vertices contain only 1s and 0s
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