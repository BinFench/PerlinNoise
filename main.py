from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

from player import *
from worldgen import *

chunks = []
player = FirstPersonController()

# window.fps_counter.enabled = False
window.exit_button.visible = False

def update():
	global block_pick, chunks, player

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: set_block_pick(0)
	if held_keys['2']: set_block_pick(1)
	if held_keys['3']: set_block_pick(2)
	if held_keys['4']: set_block_pick(3)
	for i in range(len(chunks)):
		chunk = chunks[i]
		if (chunk.toEnable and distance_xz((chunk.position[0], 0, chunk.position[1]), player.world_position) <= 23):
			chunk.toEnable = False
			chunk.enable()
		if (chunk.toDisable and distance_xz((chunk.position[0], 0, chunk.position[1]), player.world_position) > 23):
			chunk.disable()

chunks.append(SurfaceChunk((0,0), globchunks=chunks))
player.y = 8
mouse.visible = False
player.cursor.visible = False
sky = Sky()
hand = Hand()
app.run()