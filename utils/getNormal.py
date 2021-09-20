def getNormal(tri):
    v1 = tri[0]
    v2 = tri[1]
    v3 = tri[2]

    if (v1 == (0,0,0)):
        if (v2 == (0,0,1) and v3 == (0,1,0)):
            return (-1,0,0)
        elif (v2 == (0,1,0) and v3 == (1,0,0)):
            return (0,0,-1)
        elif (v2 == (0,0,1) and v3 == (1,0,0)):
            return (0,-1,0)
    elif (v1 == (0,0,1)):
        if (v2 == (0,1,0) and v3 == (0,1,1)):
            return (-1,0,0)
        elif (v2 == (0,1,1) and v3 == (1,0,1)):
            return (0,0,1)
        elif (v2 == (1,0,0) and v3 == (1,0,1)):
            return (0,-1,0)
    elif (v1 == (0,1,0)):
        if (v2 == (1,0,0) and v3 == (1,1,0)):
            return (0,0,-1)
        elif (v2 == (0,1,1) and v3 == (1,1,0)):
            return (0,1,0)
    elif (v1 == (0,1,1)):
        if (v2 == (1,0,1) and v3 == (1,1,1)):
            return (0,0,1)
        elif (v2 == (1,1,0) and v3 == (1,1,1)):
            return (0,1,0)
    elif (v1 == (1,0,0)):
        if (v2 == (1,0,1) and v3 == (1,1,0)):
            return (1,0,0)
    elif (v1 == (1,0,1)):
        if (v2 == (1,1,0) and v3 == (1,1,1)):
            return (1,0,0)