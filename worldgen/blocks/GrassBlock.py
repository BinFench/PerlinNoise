from worldgen.blocks.Voxel import *

class GrassBlock(Voxel):
    def __init__(self, position=(0,0,0), chunk=None):
        super().__init__(position=position, texture='assets/grass_block.png', chunk=chunk)