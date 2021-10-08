from worldgen.perlin import noiseGenerator

class Biome():
    def __init__(self):
        self.gen = noiseGenerator(2, [20, 20], 8)
        self.nmap = self.gen.getMap()
        for i in range(160):
            for j in range(160):
                if (not (i % 8 == 0 or j % 8  == 0)):
                    continue
                avg = 0
                
                coords = [(i-1, j-1), (i, j-1), (i+1, j-1),
                          (i-1, j),             (i+1, j),
                          (i-1, j+1), (i, j+1), (i+1, j+1)]

                coords = list(filter((lambda coord : coord[0] >= 0 and coord[0] <= 159 and coord[1] >= 0 and coord[1] <= 159 and \
                                    not(coord[0] % 8 == 0 or coord[1] % 8 == 0)), coords))

                for coord in coords:
                    avg += self.nmap[coord[0]][coord[1]]/len(coords)

                self.nmap[i][j] = avg

        for i in range(160):
            for j in range(160):
                avg = 0
                
                coords = [(i-1, j-1), (i, j-1), (i+1, j-1),
                          (i-1, j),             (i+1, j),
                          (i-1, j+1), (i, j+1), (i+1, j+1)]

                coords = list(filter((lambda coord : coord[0] >= 0 and coord[0] <= 159 and coord[1] >= 0 and coord[1] <= 159), coords))

                for coord in coords:
                    avg += self.nmap[coord[0]][coord[1]]/len(coords)

                self.nmap[i][j] = avg + 1

    def getChunk(self, pos):
        return [[self.nmap[64 + 16*pos[0] + i][64 + 16*pos[1] + j] for j in range(16)] for i in range(16)]