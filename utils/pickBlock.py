from worldgen.blocks import *

picks = [GrassBlock, StoneBlock, BrickBlock, DirtBlock]

def pickBlock(blockPick):
    global picks
    return picks[blockPick]