from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

from player.hand import Hand
from worldgen.surfaceChunk import SurfaceChunk
from worldgen.chunk import Chunk
from worldgen.voxel import Voxel

block_pick = 1
chunks = []
player = FirstPersonController()

# window.fps_counter.enabled = False
window.exit_button.visible = False
# window.display_mode = 'wireframe'

def update():
	global block_pick, chunks, player
	# print(player.world_position)

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4
	for i in range(len(chunks)):
		chunk = chunks[i]
		if (chunk.toEnable and distance_xz((chunk.position[0], 0, chunk.position[1]), player.world_position) <= 23):
			chunk.toEnable = False
			chunk.enable()
		if (chunk.toDisable and distance_xz((chunk.position[0], 0, chunk.position[1]), player.world_position) > 23):
			chunk.disable()

singleBlock = Chunk(position=(0,0,0))
singleBlock.addVoxel(Voxel(position=(8,15,8)))
singleBlock.generateMesh()
chunks.append(singleBlock)

# chunks.append(SurfaceChunk((0,0), globchunks=chunks))
player.y = 8
player.gravity = 0
sky = Sky()
hand = Hand()
app.run()