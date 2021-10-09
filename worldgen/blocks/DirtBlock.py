from worldgen.blocks.Voxel import *

class DirtBlock(Voxel):
    def __init__(self, position=(0,0,0), chunk=None):
        super().__init__(position=position, texture='assets/dirt_block.png', chunk=chunk)