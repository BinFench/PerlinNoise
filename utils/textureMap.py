from enum import Enum
from PIL import Image

grassBlock = Image.open('assets/grass_block.png')
stoneBlock = Image.open('assets/stone_block.png')
brickBlock = Image.open('assets/brick_block.png')
dirtBlock = Image.open('assets/dirt_block.png')

textureList = [grassBlock, stoneBlock, brickBlock, dirtBlock]

Texture = Enum('Texture', 
'assets/grass_block.png assets/stone_block.png assets/brick_block.png assets/dirt_block.png')

mapLength = len(list(Texture))
singleWidth = grassBlock.width
singleWidthFrac = 1.0/mapLength
width = singleWidth*mapLength
height = grassBlock.height

textureMap = Image.new('RGBA', (width, height))

for _, member in Texture.__members__.items():
    textureIndex = member.value
    texture = textureList[textureIndex - 1]
    textureMap.paste(texture, (singleWidth*(textureIndex - 1), 0))

textureMap.save('assets/textureMap.png')

def getUV(tri, texture):
    v1 = tri[0]
    v2 = tri[1]
    v3 = tri[2]
    off = singleWidth*(Texture[texture].value - 1)/width

    if (v1 == (0,0,0)):
        if (v2 == (0,0,1) and v3 == (0,1,0)):
            return ((0.375*singleWidthFrac + off, 0.75),
                    (0.375*singleWidthFrac + off, 1),
                    (0.625*singleWidthFrac + off, 0.75))
        elif (v2 == (0,1,0) and v3 == (1,0,0)):
            return ((0.375*singleWidthFrac + off, 0.75),
                    (0.625*singleWidthFrac + off, 0.75),
                    (0.375*singleWidthFrac + off, 0.5))
        elif (v2 == (0,0,1) and v3 == (1,0,0)):
            return ((0.375*singleWidthFrac + off, 0.75),
                    (0.125*singleWidthFrac + off, 0.75),
                    (0.125*singleWidthFrac + off, 0.5))
    elif (v1 == (0,0,1)):
        if (v2 == (0,1,0) and v3 == (0,1,1)):
            return ((0.375*singleWidthFrac + off, 1),
                    (0.625*singleWidthFrac + off, 0.75),
                    (0.625*singleWidthFrac + off, 1))
        elif (v2 == (0,1,1) and v3 == (1,0,1)):
            return ((0.375*singleWidthFrac + off, 0),
                    (0.625*singleWidthFrac + off, 0),
                    (0.375*singleWidthFrac + off, 0.25))
        elif (v2 == (1,0,0) and v3 == (1,0,1)):
            return ((0.125*singleWidthFrac + off, 0.75),
                    (0.375*singleWidthFrac + off, 0.5),
                    (0.125*singleWidthFrac + off, 0.5))
    elif (v1 == (0,1,0)):
        if (v2 == (1,0,0) and v3 == (1,1,0)):
            return ((0.625*singleWidthFrac + off, 0.75),
                    (0.375*singleWidthFrac + off, 0.5),
                    (0.625*singleWidthFrac + off, 0.5))
        elif (v2 == (0,1,1) and v3 == (1,1,0)):
            return ((0.625*singleWidthFrac + off, 0.75),
                    (0.875*singleWidthFrac + off, 0.75),
                    (0.625*singleWidthFrac + off, 0.5))
    elif (v1 == (0,1,1)):
        if (v2 == (1,0,1) and v3 == (1,1,1)):
            return ((0.625*singleWidthFrac + off, 0),
                    (0.375*singleWidthFrac + off, 0.25),
                    (0.625*singleWidthFrac + off, 0.25))
        elif (v2 == (1,1,0) and v3 == (1,1,1)):
            return ((0.875*singleWidthFrac + off, 0.75),
                    (0.625*singleWidthFrac + off, 0.5),
                    (0.875*singleWidthFrac + off, 0.5))
    elif (v1 == (1,0,0)):
        if (v2 == (1,0,1) and v3 == (1,1,0)):
            return ((0.375*singleWidthFrac + off, 0.5),
                    (0.375*singleWidthFrac + off, 0.25),
                    (0.625*singleWidthFrac + off, 0.5))
    elif (v1 == (1,0,1)):
        if (v2 == (1,1,0) and v3 == (1,1,1)):
            return ((0.375*singleWidthFrac + off, 0.25),
                    (0.625*singleWidthFrac + off, 0.5),
                    (0.625*singleWidthFrac + off, 0.25))