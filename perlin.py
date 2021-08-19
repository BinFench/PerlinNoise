# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 11:28:49 2019

@author: Ben Finch
https://adrianb.io/2014/08/09/perlinnoise.html
"""

from collections import namedtuple
import math
import random
import numpy

class noiseGenerator:
    """
    A Perlin noise generator for n dimensions
    """
    
    def __init__(self, numDim, gridLength, gridSize = 10,
                 userSeed = random.randint(0,65535)):
        """Constructor"""
        self.isProcessed = False #To save on computation
        self.dimensions = numDim
        self.noiseMap = numpy.empty([gridLength*gridSize] * numDim) #Gen. noise here
        self.blockMap = numpy.empty([gridSize + 1] * numDim) #grid on map
        self.seed = userSeed #Seed for random number generator
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
        """Initialize the vectors on each grid edge"""
        blockTrav = self.blockMap
        #Begin by iterating through each grid edge
        for i in range((self.gridSize + 1) ** self.numDim):
            #iterate through each dimension of given edge
            for j in range(self.numDim):
                #Determine the index of the edge for given dimension
                coordinate = (i / ((self.gridSize + 1) ** j)) % (self.gridSize + 1)
                #If all dimensions haven't been indexed, traverse to next dim
                if (j != self.numDim - 1):
                    blockTrav = blockTrav[coordinate]
                #If all dimensions are indexed, encode unit vector on edge
                else:
                    blockTrav[coordinate] = 0
                    #n dimension unit vector is encoded as scalar
                    for k in range(self.numDim):
                        blockTrav[coordinate] += random.randint(0, 999) * (1000 ** k)
                
    def f(self, coordinates):
        """Find the noise at the specified point"""
        assert(self.dimensions == len(coordinates)), """number of dimensions 
        and coordinates mismatch"""
        modCoordinates = [0] * len(coordinates) #Location in local gridspace
        gradCoordinates = [0] * len(coordinates) #Index of local grid edge
        smoothCoeff = [0] * len(coordinates) #Smooth coefficient for weighted ave
        for i in range(len(coordinates)):
            modCoordinates[i] = coordinates[i] % self.gridSize
            gradCoordinates[i] = coordinates[i] / self.gridSize
            smoothCoeff[i] = 3*(float(modCoordinates[i]/self.gridSize))**2 
            - 2*(float(modCoordinates[i]/self.gridSize))**3
        #Now we perform dot product using the gradient index and 
        #the displacement vector
        dotProducts = [0] * (2 ** self.numDim)
        adjacencies = [0] * (2 ** (self.numDim - 1))
        dispVector = [0] * len(coordinates)
        gradVector = [0] * len(coordinates)
        gradScalar = 0
        
        for i in range(2 ** self.numDim):
            if (i > 0):
                for j in range(2 ** (self.numDim - 1) - 1):
                    if (adjacencies[j] == 0):
                        adjacencies[j] = 1
                        break
                    else:
                        adjacencies[j] = 0
                        
            for j in range(len(adjacencies)):
                if (j == 0):
                    gradScalar = self.blockMap[gradCoordinates[0] + adjacencies[0]]
                else:
                    gradScalar = gradScalar[gradCoordinates[j] + adjacencies[j]]
                if (adjacencies[j] == 1):
                    dispVector[j] = (self.gridSize - modCoordinates[j])/float(self.gridSize)
                else:
                    dispVector[j] = modCoordinates[j]/float(self.gridSize)
                    
            if (self.numDim > 1):
                unit = 0
                for j in range(len(gradVector)):
                    gradVector[j] = ((gradScalar / 1000 ** j)
                    - (gradScalar / 1000 ** (j + 1)) * 1000)
                    - 499.5
                    unit += gradVector[j] ** 2
            
                unit = unit ** 0.5
            
                for j in range(len(gradVector)):
                    gradVector[j] /= float(unit)
                    
            else:
                gradVector[0] = (gradScalar - 499.5)/499.5
                
            dotProducts[i] = numpy.dot(dispVector, gradVector)
            
        subWeights = [[0 for i in range(2**(self.numDim - 1))] for j in range(self.numDim)]
        for i in range(self.numDim):
            for j in range(2**(self.numDim - 1)):
                subWeights[j][i] = 0
				
		#TODO: Weighted average of n dimension dot products
                
    def getMap(self):
        if (self.isProcessed): 
            return self.noiseMap
        
        self.isProcessed = True
        numSquares = max(self.lengths)/self.gridSize
        