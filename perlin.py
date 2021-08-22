"""
Created on Sat Jul 13 2019

@author: Ben Finch
https://adrianb.io/2014/08/09/perlinnoise.html
"""

import random
import numpy
import copy

class noiseGenerator:
    """
    A Perlin noise generator for n dimensions
    """
    
    def __init__(self, numDim, gridLength, gridSize = 10,
                 userSeed = random.randint(0,65535)):
        """Constructor"""
        self.isProcessed = False # To save on computation
        self.dimensions = numDim
        self.noiseMap = numpy.empty([gridLength[i]*gridSize for i in range(self.dimensions)]) # Gen. noise here
        self.blockMap = numpy.empty([gridLength[i] + 1 for i in range(self.dimensions)]) # grid on map
        self.seed = userSeed # Seed for random number generator
        self.gridLength = gridLength
        self.gridSize = gridSize
        random.seed(userSeed)
        self.initGrid()
        
    def setSeed(self, userSeed):
        """Change the seed for the random number generator"""
        self.seed = userSeed
        self.isProcessed = False
        random.seed(userSeed)
        self.initGrid()
        
    def initGrid(self):
        dimEdges = self.gridLength[0] + 1
        for i in range(dimEdges):
            self.setEdge([i])
                
    def f(self, coordinates):
        """Find the noise at the specified point"""
        assert(self.dimensions == len(coordinates)), """number of dimensions 
        and coordinates mismatch"""
        modCoordinates = [0] * len(coordinates) # Location in local gridspace
        gradCoordinates = [0] * len(coordinates) # Index of local grid edge
        smoothCoeff = [0] * len(coordinates) # Smooth coefficient for weighted ave
        for i in range(len(coordinates)):
            modCoordinates[i] = coordinates[i] % self.gridSize
            gradCoordinates[i] = coordinates[i] / self.gridSize
            # smoothCoeff = 3x^2 - 2x^3 (scalar smoothing function)
            smoothCoeff[i] = 3*(float(modCoordinates[i]/self.gridSize))**2 \
            - 2*(float(modCoordinates[i]/self.gridSize))**3
        # Now we perform dot product using the gradient index and 
        # the displacement vector
        dotProducts = [0] * (2 ** self.dimensions)
        adjacencies = [0] * self.dimensions
        dispVector = [0] * self.dimensions
        gradVector = [0] * self.dimensions
        gradScalar = 0
        
        for i in range(2 ** self.dimensions):
            if (i > 0):
                # Boolean counter from 0 to 2^(dims - 1)
                # Used to get the vectors for each 
                # edge of the n-dim hypercube
                for j in range(self.dimensions):
                    if (adjacencies[j] == 0):
                        adjacencies[j] = 1
                        break
                    else:
                        adjacencies[j] = 0
                        
            # Traverse the blockmap by each coordinate
            # Based on above counter, check adjacent coordinate
            for j in range(self.dimensions):
                if (j == 0):
                    gradScalar = self.blockMap[int(gradCoordinates[0] + adjacencies[0])]
                else:
                    gradScalar = gradScalar[int(gradCoordinates[j] + adjacencies[j])]

                if (adjacencies[j] == 1):
                    dispVector[j] = (self.gridSize - modCoordinates[j])/float(self.gridSize)
                else:
                    dispVector[j] = modCoordinates[j]/float(self.gridSize)
                    
            if (self.dimensions > 1):
                # Normalize vectors
                gradUnit = 0
                dispUnit = 0
                for j in range(len(gradVector)):
                    curVec = int(gradScalar / 1000 ** j)
                    nextVec = int(gradScalar / 1000 ** (j + 1)) * 1000.0
                    gradVector[j] = curVec - nextVec - 499.5
                    gradUnit += gradVector[j] ** 2
                    dispUnit += dispVector[j] ** 2
            
                gradUnit = gradUnit ** 0.5
                dispUnit = dispUnit ** 0.5
            
                for j in range(len(gradVector)):
                    gradVector[j] /= gradUnit
                    if (dispUnit != 0):
                        dispVector[j] /= dispUnit
                    
            else:
                gradVector[0] = (gradScalar - 499.5)/499.5
                
            dotProducts[i] = numpy.dot(dispVector, gradVector)
            
        subWeights = [[0 for i in range(2**(self.dimensions - 1))] for j in range(self.dimensions)]
        for i in range(self.dimensions):
            for j in range(2**(self.dimensions - i - 1)):
                if (i == 0):
                    subWeights[i][j] = smoothCoeff[0]*dotProducts[2*j + 1] + (1-smoothCoeff[0])*dotProducts[2*j]
                else:
                    subWeights[i][j] = smoothCoeff[i]*subWeights[i-1][2*j+1] + (1-smoothCoeff[i])*subWeights[i-1][2*j]
				
        noise = subWeights[self.dimensions - 1][0]
        if (noise > 0):
            return 6*noise**5 - 15*noise**4 + 10*noise**3
        else:
            return -(6*abs(noise)**5 - 15*abs(noise)**4 + 10*abs(noise)**3)

    def setMap(self, coords):
        """Recursively populate the noise map"""
        # The coords argument may be incomplete, and we 
        # use recursion to span the entire n-dim space
        if (len(coords) == self.dimensions):
            # Unpack the noisemap
            curMap = self.noiseMap
            for i in range(len(coords)):
                if (i != len(coords) - 1):
                    curMap = curMap[coords[i]]
                else:
                    curMap[coords[i]] = self.f(coords)
        
        else:
            # Build the coordinates
            dimCoords = self.gridLength[len(coords)]*self.gridSize
            for i in range(dimCoords):
                temp = copy.deepcopy(coords)
                temp.append(i)
                self.setMap(temp)

    def setEdge(self, coords):
        """Recursively populate the edge map"""
        # The coords argument may be incomplete, and we 
        # use recursion to span the entire n-dim space
        if (len(coords) == self.dimensions):
            # Unpack the noisemap
            curMap = self.blockMap
            for i in range(len(coords)):
                if (i != len(coords) - 1):
                    curMap = curMap[coords[i]]
                else:
                    curMap[coords[i]] = 0
                    for j in range(self.dimensions):
                        curMap[coords[i]] += random.randint(0, 999) * (1000 ** j)
        
        else:
            # Build the coordinates
            dimCoords = self.gridLength[len(coords)] + 1
            for i in range(dimCoords):
                temp = copy.deepcopy(coords)
                temp.append(i)
                self.setEdge(temp)
                
    def getMap(self):
        """Return the generated noise map"""
        if (not self.isProcessed):
            self.isProcessed = True
            dimCoords = self.gridLength[0]*self.gridSize
            for i in range(dimCoords):
                print("%d/%d" % (i + 1, dimCoords))
                self.setMap([i])
        return self.noiseMap


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    gen = noiseGenerator(2, [20, 20], 5)
    nmap = gen.getMap()
    for i in range(100):
        for j in range(100):
            if (not (i % 5 == 0 or j % 5  == 0)):
                continue
            avg = 0
            
            coords = [(i-1, j-1), (i, j-1), (i+1, j-1),
                      (i-1, j),             (i+1, j),
                      (i-1, j+1), (i, j+1), (i+1, j+1)]

            coords = list(filter((lambda coord : coord[0] >= 0 and coord[0] <= 99 and coord[1] >= 0 and coord[1] <= 99 and \
                                not(coord[0] % 5 == 0 or coord[1] % 5 == 0)), coords))

            for coord in coords:
                avg += nmap[coord[0]][coord[1]]/len(coords)

            nmap[i][j] = avg

    for i in range(100):
        for j in range(100):
            avg = 0
            
            coords = [(i-1, j-1), (i, j-1), (i+1, j-1),
                      (i-1, j),             (i+1, j),
                      (i-1, j+1), (i, j+1), (i+1, j+1)]

            coords = list(filter((lambda coord : coord[0] >= 0 and coord[0] <= 99 and coord[1] >= 0 and coord[1] <= 99), coords))

            for coord in coords:
                avg += nmap[coord[0]][coord[1]]/len(coords)

            nmap[i][j] = avg

    plt.imshow(nmap, cmap='hot', interpolation='nearest')
    plt.show()