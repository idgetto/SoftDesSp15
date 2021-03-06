""" Synthesizes a blues solo algorithmically """

from Nsound import *
import numpy as np
import random

def add_note(out, instr, key_num, duration, bpm, volume):
    """ Adds a note from the given instrument to the specified stream

        out: the stream to add the note to
        instr: the instrument that should play the note
        key_num: the piano key number (A 440Hzz is 49)
        duration: the duration of the note in beats
        bpm: the tempo of the music
        volume: the volume of the note
	"""
    freq = (2.0**(1/12.0))**(key_num-49)*440.0
    stream = instr.play(duration*(60.0/bpm),freq)
    stream *= volume
    out << stream

# this controls the sample rate for the sound file you will generate
sampling_rate = 44100.0
Wavefile.setDefaults(sampling_rate, 16)

bass = GuitarBass(sampling_rate)	# use a guitar bass as the instrument
solo = AudioStream(sampling_rate, 1)

""" these are the piano key numbers for a 3 octave blues scale in A
	See: http://en.wikipedia.org/wiki/Blues_scale """
blues_scale = [25, 28, 30, 31, 32, 35, 37, 40, 42, 43, 44, 47, 49, 52, 54, 55, 56, 59, 61]
beats_per_minute = 45				# Let's make a slow blues solo
note_diffs = [-1, 0, 1]

# set a starting note
note1 = random.randint(0, len(blues_scale) - 1)

# compose the solo
for i in range(16):
    # change the note by some value
    note1_diff = random.choice(note_diffs)
    note2_diff = random.choice(note_diffs)

    note1 += note1_diff
    note2 = note1 + note2_diff

    # don't go out of bounds
    note1 = note1 % len(blues_scale)
    note2 = note2 % len(blues_scale)
        
    # add the note to the stream
    add_note(solo, bass, blues_scale[note1], 1, beats_per_minute, 1.0)
    add_note(solo, bass, blues_scale[note2], 1, beats_per_minute, 1.0)

# create the backing track
backing_track = AudioStream(sampling_rate, 1)
Wavefile.read('backing.wav', backing_track)

# mix the solo and backing track
mixer = Mixer()
mixer.add(2.25, 0, solo)
mixer.add(0, 0, backing_track)

# write the audio file
mixer.getStream(500.0) >> "blues_solo.wav"
