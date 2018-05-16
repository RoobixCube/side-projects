from uuid import UUID
from game.base import BaseGame
from game.model import PineTree
from game.music import *
from game.common import *
from game.input import numbers
from pprint import pprint
import pyglet
from pyglet.window import key

my_screen = pyglet.window.Window()  # fullscreen=True)

pprint(my_screen)

my_seed = UUID("c6f8f230-65bc-4a70-8e19-0979f716ceb6")
pprint(("my_seed", my_seed), indent=4)

tile_factor = 96
tile_width = 48

assets = [
    PineTree(x=tile_factor*i, y=tile_factor*j, w=tile_width, h=tile_width)
    for i in range(0, int(my_screen.width/tile_factor))
    for j in range(0, int(my_screen.height/tile_factor))
]

my_game = BaseGame(constructables=assets, screen=my_screen)  # , local_seed=my_seed)
# pprint(("my_game", my_game), indent=4)
# pprint(("pre-assets", my_game.assets), indent=4)


my_game.build()
# pprint(
#     {
#         "built-assets": my_game.assets
#     },
#     indent=4
# )

intro_timing = Timing(tempo=130)
ascent_timing = Timing(tempo=120)
mid_timing = Timing(tempo=140.688)

pad_1_2 = Voice(clip_file="assets/music/pad_1-2.mp3", beats=4)
pad_3_4 = Voice(clip_file="assets/music/pad_3-4.mp3", beats=8)
pad_5 = Voice(clip_file="assets/music/pad_5.mp3", beats=8)
pad_6 = Voice(clip_file="assets/music/pad_5.mp3", beats=8)
pad_7_8 = Voice(clip_file="assets/music/pad_7_8.mp3", beats=8)
pad_9 = Voice(clip_file="assets/music/pad_9.mp3", beats=8)

piano_bass_1 = Voice(clip_file="assets/music/piano_bass_1.mp3", beats=4)
piano_bass_2 = Voice(clip_file="assets/music/piano_bass_2.mp3", beats=4)
piano_bass_3 = Voice(clip_file="assets/music/piano_bass_3.mp3", beats=8)
piano_bass_4 = Voice(clip_file="assets/music/piano_bass_4.mp3", beats=8)
piano_bass_5_6 = Voice(clip_file="assets/music/piano_bass_5_6.mp3", beats=8)
piano_bass_7 = Voice(clip_file="assets/music/piano_bass_7.mp3", beats=8)
piano_bass_8_9 = Voice(clip_file="assets/music/piano_bass_8_9.mp3", beats=8)

piano_treble_3 = Voice(clip_file="assets/music/piano_treble_3.mp3", beats=8)
piano_treble_4 = Voice(clip_file="assets/music/piano_treble_4.mp3", beats=8)
piano_treble_5_6 = Voice(clip_file="assets/music/piano_treble_5_6.mp3", beats=8)
piano_treble_8 = Voice(clip_file="assets/music/piano_treble_8.mp3", beats=8)
piano_treble_9 = Voice(clip_file="assets/music/piano_treble_9.mp3", beats=8)

lead_5_6 = Voice(clip_file="assets/music/lead_5_6.mp3", beats=8)
lead_9 = Voice(clip_file="assets/music/lead_9.mp3", beats=8)

drums_6 = Voice(clip_file="assets/music/drums_6.mp3", beats=8)
drums_7 = Voice(clip_file="assets/music/drums_7.mp3", beats=8)
drums_8 = Voice(clip_file="assets/music/drums_8.mp3", beats=8)
drums_9 = Voice(clip_file="assets/music/drums_9.mp3", beats=8)

ascent_1 = Voice(clip_file="assets/music/ascent1.mp3", beats=4)

cloudy_7 = Voice(clip_file="assets/music/cloudy_7.mp3", beats=8)
cloudy_8 = Voice(clip_file="assets/music/cloudy_8.mp3", beats=8)
cloudy_9 = Voice(clip_file="assets/music/cloudy_9.mp3", beats=8)

# my_voices = [
#     pad_1_2,
#     pad_3_4,
#     pad_5,
#     piano_bass_1,
#     piano_bass_2,
#     piano_bass_3,
#     piano_bass_4,
#     piano_bass_5,
#     piano_treble_3,
#     piano_treble_4,
#     piano_treble_5,
#     lead_5
# ]
#
# for n in my_voices:
#     print({
#         "VOICE": n.filename,
#         "LENGTH": len(n.clip),
#         "BEATS": n.beats,
#         "GUESS": int(round(len(n.clip) / 1000 / 5))
#
#     })


intro_0 = Loop(voices=[pad_1_2])

intro_1 = Loop(voices=[
    pad_1_2,
    piano_bass_1,
])

intro_2 = Loop(voices=[
    pad_1_2,
    piano_bass_2,
])

intro_3 = Loop(voices=[
    pad_3_4,
    piano_bass_3,
    piano_treble_3
])

intro_4 = Loop(voices=[
    pad_3_4,
    piano_bass_4,
    piano_treble_4
])

intro_5 = Loop(voices=[
    pad_5,
    piano_bass_5_6,
    piano_treble_5_6,
    lead_5_6
])

intro_6 = Loop(voices=[
    pad_6,
    piano_bass_5_6,
    piano_treble_5_6,
    lead_5_6,
    drums_6,
])

ascent_loop = Loop(voices=[
    ascent_1
])

mid_0 = Loop(voices=[
    cloudy_7,
    pad_7_8,
    drums_7,
    piano_bass_7
])

mid_1 = Loop(voices=[
    cloudy_8,
    pad_7_8,
    drums_8,
    piano_bass_8_9,
    piano_treble_8
])

mid_2 = Loop(voices=[
    cloudy_9,
    pad_9,
    drums_9,
    piano_bass_8_9,
    piano_treble_9,
    lead_9
])


my_song = Song(
    name="demo",
    sections=[
        Section(
            name="intro",
            timing=intro_timing,
            loops=[
                intro_0,
                intro_1,
                intro_2,
                intro_3,
                intro_4,
                intro_5,
                intro_6
            ]),
        Section(
            name="ascent1",
            timing=ascent_timing,
            loops=[
                ascent_loop
            ]
        ),
        Section(
            name="mid",
            timing=mid_timing,
            loops=[
                mid_0,
                mid_1,
                mid_2
            ]
        )
    ]
)

current_section = my_song.sections[0]
current_loop = current_section.loops[0]


@my_screen.event
def on_key_press(symbol, modifiers):
    global current_loop
    global current_section

    def change_music_section(sec_ix: int):
        global current_loop
        global current_section

        if 0 < sec_ix <= len(my_song.sections):
            MUSIC.SECTION = sec_ix
            MUSIC.POSITION = 0
            MUSIC.set_voices(1)
            current_section = my_song.sections[MUSIC.SECTION]
            current_loop = current_section.loops[0]
            current_loop.restart()
            label.draw()

    if symbol in numbers:
        val = numbers[symbol]
        label = pyglet.text.Label("Loading pattern {0}".format(val))
        label.draw()
        current_loop.stop()
        new_loop = current_section.get_loop(val)
        if not new_loop:
            return
        print("**KEYPRESS: Loop changed to ", val)
        new_loop.restart()
        current_loop = new_loop

    if symbol == key.MOTION_UP:
        print("**KEYPRESS: Raising voices")
        MUSIC.raise_voices()
        label = pyglet.text.Label("Raising voices")
        current_loop.change_voices()
        label.draw()
    if symbol == key.MOTION_DOWN:
        print("**KEYPRESS: Lowering voices")
        MUSIC.lower_voices()
        label = pyglet.text.Label("Lowering voices")
        current_loop.change_voices()
        label.draw()

    if symbol == key.MOTION_RIGHT:
        print("**KEYPRESS: Next Section")
        label = pyglet.text.Label("Next section")
        current_loop.stop()
        new_section = MUSIC.SECTION + 1
        change_music_section(new_section)

    if symbol == key.MOTION_LEFT:
        print("**KEYPRESS: Previous Section")
        label = pyglet.text.Label("Previous section")
        current_loop.stop()
        new_section = MUSIC.SECTION - 1
        change_music_section(new_section)


my_game.start(window_title="HELLO")

if break_prompt("Exit?"):
    exit()
