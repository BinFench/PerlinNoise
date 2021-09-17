def checkNeighbourVoxels(x, y, z, voxels):
    # We filter out vertices that are not seen
    vertices = [(0, 0, 0), (0, 0, 1),
                (0, 1, 0), (0, 1, 1),
                (1, 0, 0), (1, 0, 1),
                (1, 1, 0), (1, 1, 1)]

    # Determine if on chunk boundaries
    # I'm aware this is bad code, but it should be fast
    # TODO: Refactor if game performance allows
    if (x == 0):
        if (y == 0):
            if (z == 0):
                # x, y, z bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(7)

            elif (z == 15):
                # x, y, z bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(6)

            else:
                # x, y bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(7)

                vcheck = True
                # If there is any surrounding opening, (1, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(6)

        elif (y == 15):
            if (z == 0):
                # x, y, z bound
                vcheck = True
                # If there is any surrounding opening, (1, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][15 - j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(5)

            elif (z == 15):
                # x, y, z bound
                vcheck = True
                # If there is any surrounding opening, (1, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][15 - j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(4)

            else:
                # x, y bound
                vcheck = True
                # If there is any surrounding opening, (1, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][15 - j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(5)

                vcheck = True
                # If there is any surrounding opening, (1, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][15 - j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(4)

        else:
            if (z == 0):
                # x, z bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][y + j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(7)

                vcheck = True
                # If there is any surrounding opening, (1, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][y - j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(5)

            elif (z == 15):
                # x, z bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][y + j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(6)

                vcheck = True
                # If there is any surrounding opening, (1, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][y - j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(4)

            else:
                # x bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][y + j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(7)

                vcheck = True
                # If there is any surrounding opening, (1, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][y + j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(6)

                vcheck = True
                # If there is any surrounding opening, (1, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][y - j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(5)

                vcheck = True
                # If there is any surrounding opening, (1, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[i][y - j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(4)

    elif (x == 15):
        if (y == 0):
            if (z == 0):
                # x, y, z bound
                vcheck = True
                # If there is any surrounding opening, (0, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(3)

            elif (z == 15):
                # x, y, z bound
                vcheck = True
                # If there is any surrounding opening, (0, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(2)

            else:
                # x, y bound
                vcheck = True
                # If there is any surrounding opening, (0, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(3)

                vcheck = True
                # If there is any surrounding opening, (0, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(2)

        elif (y == 15):
            if (z == 0):
                # x, y, z bound
                vcheck = True
                # If there is any surrounding opening, (0, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][15 - j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(1)

            elif (z == 15):
                # x, y, z bound
                vcheck = True
                # If there is any surrounding opening, (0, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][15 - j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(0)

            else:
                # x, y bound
                vcheck = True
                # If there is any surrounding opening, (0, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][15 - j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(1)

                vcheck = True
                # If there is any surrounding opening, (0, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][15 - j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(0)

        else:
            if (z == 0):
                # x, z bound
                vcheck = True
                # If there is any surrounding opening, (0, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][y + j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(3)

                vcheck = True
                # If there is any surrounding opening, (0, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][y - j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(1)

            elif (z == 15):
                # x, z bound
                vcheck = True
                # If there is any surrounding opening, (0, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][y + j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(2)

                vcheck = True
                # If there is any surrounding opening, (0, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][y - j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(0)

            else:
                # x bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][y + j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(3)

                vcheck = True
                # If there is any surrounding opening, (0, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][y + j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(2)

                vcheck = True
                # If there is any surrounding opening, (0, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][y - j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(1)

                vcheck = True
                # If there is any surrounding opening, (0, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[15 - i][y - j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(0)

    else:
        if (y == 0):
            if (z == 0):
                # y, z bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(7)

                vcheck = True
                # If there is any surrounding opening, (0, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(3)

            elif (z == 15):
                # y, z bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(6)
                    
                vcheck = True
                # If there is any surrounding opening, (0, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(2)

            else:
                # y bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(7)

                vcheck = True
                # If there is any surrounding opening, (1, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(6)

                vcheck = True
                # If there is any surrounding opening, (0, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(3)

                vcheck = True
                # If there is any surrounding opening, (0, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(2)

        elif (y == 15):
            if (z == 0):
                # y, z bound
                vcheck = True
                # If there is any surrounding opening, (1, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][15 - j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(5)

                vcheck = True
                # If there is any surrounding opening, (0, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][15 - j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(1)

            elif (z == 15):
                # y, z bound
                vcheck = True
                # If there is any surrounding opening, (1, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][15 - j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(4)

                vcheck = True
                # If there is any surrounding opening, (0, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][15 - j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(0)

            else:
                # y bound
                vcheck = True
                # If there is any surrounding opening, (1, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][15 - j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(5)

                vcheck = True
                # If there is any surrounding opening, (1, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][15 - j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(4)
                
                vcheck = True
                # If there is any surrounding opening, (0, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][15 - j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(1)

                vcheck = True
                # If there is any surrounding opening, (0, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][15 - j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(0)

        else:
            if (z == 0):
                # z bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][y + j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(7)

                vcheck = True
                # If there is any surrounding opening, (1, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][y - j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(5)
                
                vcheck = True
                # If there is any surrounding opening, (0, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][y + j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(3)

                vcheck = True
                # If there is any surrounding opening, (0, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][y - j][k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(1)

            elif (z == 15):
                # z bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][y + j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(6)

                vcheck = True
                # If there is any surrounding opening, (1, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][y - j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(4)

                vcheck = True
                # If there is any surrounding opening, (0, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][y + j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(2)
                
                vcheck = True
                # If there is any surrounding opening, (0, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][y - j][15 - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(0)

            else:
                # no bound
                vcheck = True
                # If there is any surrounding opening, (1, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][y + j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(7)

                vcheck = True
                # If there is any surrounding opening, (1, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][y + j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(6)
                
                vcheck = True
                # If there is any surrounding opening, (1, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][y - j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(5)
                
                vcheck = True
                # If there is any surrounding opening, (1, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x + i][y - j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(4)
                
                vcheck = True
                # If there is any surrounding opening, (0, 1, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][y + j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(3)
                
                vcheck = True
                # If there is any surrounding opening, (0, 1, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][y + j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(2)
                
                vcheck = True
                # If there is any surrounding opening, (0, 0, 1) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][y - j][z + k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(1)
                
                vcheck = True
                # If there is any surrounding opening, (0, 0, 0) is needed
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            if (voxels[x - i][y - j][z - k] is None):
                                vcheck = False
                                break
                if (vcheck):
                    vertices.pop(0)
    return vertices