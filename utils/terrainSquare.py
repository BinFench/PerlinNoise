import numpy

def terrainSquare(square, lengths):
	toRet = [[0 for i in range(lengths[1])] for j in range(lengths[0])]
	for x in range(lengths[0]):
		for y in range(lengths[1]):
			# perform f(x, y) from perlin noise
			averages = []
			for x2 in range(2):
				dotProducts = []
				for y2 in range(2):
					xdir = 1
					ydir = 1
					if (x2 == 1):
						xdir = -1
					if (y2 == 1):
						ydir = -1
					dispVector = [(lengths[0]*x2 + xdir*x)/float(lengths[0]), (lengths[1]*y2 + ydir*y)/float(lengths[1])]
					gradScalar = square[x2][y2]
					gradVector = [gradScalar - int(gradScalar/1000)*1000, int(gradScalar/1000)]
					# Normalize both vectors
					unit = (dispVector[0]**2 + dispVector[1]**2)**0.5
					if (unit != 0):
						dispVector = [dispVector[0]/unit, dispVector[1]/unit]
					unit = (gradVector[0]**2 + gradVector[1]**2)**0.5
					if (unit != 0):
						gradVector = [gradVector[0]/unit, gradVector[1]/unit]
					dotProducts.append(numpy.dot(dispVector, gradVector))
				t = float(y / lengths[1])
				smooth_t = 3*t**2 - 2*t**3
				averages.append(smooth_t*dotProducts[1] + (1-smooth_t)*dotProducts[0])
			t = float(x / lengths[0])
			smooth_t = 3*t**2 - 2*t**3
			t = smooth_t*averages[1] + (1-smooth_t)*averages[0]
			if (t > 0):
				smooth_t = 6*t**5 - 15*t**4 + 10*t**3
			else:
				smooth_t = -(6*abs(t)**5 - 15*abs(t)**4 + 10*abs(t)**3)
			
			toRet[x][y] = smooth_t
	# Perform averaging for smoother terrain
	for x in range(lengths[0]):
		for y in range(lengths[1]):
			if (not (x % (lengths[0] - 1) == 0 or y % (lengths[1] - 1) == 0)):
				continue
			avg = 0
				
			coords = [(x-1, y-1), (x, y-1), (x+1, y-1),
					(x-1, y),			 (x+1, y),
					(x-1, y+1), (x, y+1), (x+1, y+1)]

			coords = list(filter((lambda coord : coord[0] >= 0 and coord[0] < lengths[0] - 1 and coord[1] >= 0 and coord[1] < lengths[1] - 1), coords))

			for coord in coords:
				avg += toRet[coord[0]][coord[1]]/len(coords)
			toRet[x][y] = avg

	for x in range(lengths[0]):
		for y in range(lengths[1]):
			if (x % (lengths[0] - 1) == 0 or y % (lengths[1] - 1) == 0):
				continue
			avg = 0
				
			coords = [(x-1, y-1), (x, y-1), (x+1, y-1),
					(x-1, y),			 (x+1, y),
					(x-1, y+1), (x, y+1), (x+1, y+1)]

			coords = list(filter((lambda coord : coord[0] >= 0 and coord[0] <= lengths[0] - 1 and coord[1] >= 0 and coord[1] <= lengths[1] - 1), coords))

			for coord in coords:
				avg += toRet[coord[0]][coord[1]]/len(coords)
			toRet[x][y] = avg
	
	return toRet