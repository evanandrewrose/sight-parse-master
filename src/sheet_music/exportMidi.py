#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

# Import the library
from midiutil.MidiFile import MIDIFile

class Midi:
    def __init__(self):
        # Create the MIDIFile Object with 1 track
        self.midi = MIDIFile(1)

        # Tracks are numbered from zero. Times are measured in beats.
        track = 0
        time = 0

        # Add track name and tempo.
        self.midi.addTrackName(track,time,"Sample Track")
        self.midi.addTempo(track,time,120)

        self.timer = 0

    def add_note(self, pitch, duration, track = 0, channel = 0, volume = 100):
        # Now add the note.
        self.midi.addNote(track, channel, self.pitch_to_midi(pitch), self.timer, duration, volume)
        self.timer += duration*2

    def write(self):
        # And write it to disk.
        binfile = open("output.mid", 'wb')
        self.midi.writeFile(binfile)
        binfile.close()

    def pitch_to_midi(self, note):
        return {
            "A3" : 57,
            "B3" : 59,
            "C3" : 48,
            "D3" : 50,
            "E3" : 52,
            "F3" : 53,
            "G3" : 55,
            "A4" : 69,
            "B4" : 71,
            "C4" : 60,
            "D4" : 62,
            "E4" : 64,
            "F4" : 65,
            "G4" : 67,
        }[note]