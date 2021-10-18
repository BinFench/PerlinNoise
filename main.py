from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

from player import *
from worldgen import *

chunks = []
player = FirstPersonController()
count = 0
player.y = 8
player.gravity = 0
mouse.visible = False
player.cursor.visible = False
sky = Sky()
hand = Hand()

def dist3D(p1, p2):
	return ((p1[0]-p2[0])**2.0 + (p1[1]-p2[1])**2.0 + (p1[2]-p2[2])**2.0)**0.5

def update():
	global block_pick, chunks, player, count

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
		pos = (chunk.position[0] + 8, chunk.position[1] + 8, chunk.position[2] + 8)
		if (dist3D(pos, player.world_position) <= 25):
			chunk.enable()
		else:
			chunk.disable()

	if (count == 3):
		player.gravity = 1
	elif (count < 3):
		count += 1

def run():
	# window.fps_counter.enabled = False
	window.exit_button.visible = False

	biome = Biome()

	SurfaceChunk(biome, (0,0), globchunks=chunks)
	app.run()

run()