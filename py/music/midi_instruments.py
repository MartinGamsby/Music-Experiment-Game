from mingus.containers import instrument as instr
#TODO: Check https://bspaans.github.io/python-mingus/doc/wiki/tutorialInstrumentModule.html and https://github.com/bspaans/python-mingus/blob/master/mingus/containers/instrument.py
from random import random, choice, randrange, shuffle

import logging
logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------
def random_instrument(choices):
    instrument = choice(choices)
    midi_instr = midi_instrument(instrument)
    logger.info(f"Instrument {instrument}: {midi_instr}")
    return midi_instr
    
#------------------------------------------------------------------------------
def midi_instrument(name):
    return instr.MidiInstrument().names.index(name)
    
#------------------------------------------------------------------------------
def piano():
    return ["Acoustic Grand Piano", "Bright Acoustic Piano", "Electric Grand Piano", "Honky-tonk Piano", "Electric Piano 1", "Electric Piano 2", "Harpsichord", "Clavi"]

def chromatic_percussion():
    return ["Celesta", "Glockenspiel", "Music Box", "Vibraphone", "Marimba", "Xylophone", "Tubular Bells", "Dulcimer"]
        
def organ():
    return ["Drawbar Organ", "Percussive Organ", "Rock Organ", "Church Organ", "Reed Organ", "Accordion", "Harmonica", "Tango Accordion"]
        
def guitar():
    """ In most synthesizer interpretations, guitar and bass sounds are set an octave lower than other instruments. """
    return ["Acoustic Guitar (nylon)", "Acoustic Guitar (steel)", "Electric Guitar (jazz)", "Electric Guitar (clean)", "Electric Guitar (muted)", "Overdriven Guitar", "Distortion Guitar", "Guitar harmonics"]
    
def acoustic_guitar():
    """ In most synthesizer interpretations, guitar and bass sounds are set an octave lower than other instruments. """
    return ["Acoustic Guitar (nylon)", "Acoustic Guitar (steel)"]
        
def bass():
    """ In most synthesizer interpretations, guitar and bass sounds are set an octave lower than other instruments. """
    return ["Acoustic Bass", "Electric Bass (finger)", "Electric Bass (pick)", "Fretless Bass", "Slap Bass 1", "Slap Bass 2", "Synth Bass 1", "Synth Bass 2"]
    
def acoustic_bass():
    """ In most synthesizer interpretations, guitar and bass sounds are set an octave lower than other instruments. """
    return ["Acoustic Bass"]
    
def strings():
    return ["Violin", "Viola", "Cello", "Contrabass", "Tremolo Strings", "Pizzicato Strings", "Orchestral Harp", "Timpani" ]
        
def ensemble():
    return ["String Ensemble 1", "String Ensemble 2", "SynthStrings 1", "SynthStrings 2", "Choir Aahs", "Voice Oohs", "Synth Voice", "Orchestra Hit"]
        
def brass():
    return ["Trumpet", "Trombone", "Tuba", "Muted Trumpet", "French Horn", "Brass Section", "SynthBrass 1", "SynthBrass 2"]
        
def reed():
    return ["Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax", "Oboe", "English Horn", "Bassoon", "Clarinet"]
        
def pipe():
    return ["Piccolo", "Flute", "Recorder", "Pan Flute", "Blown Bottle", "Shakuhachi", "Whistle", "Ocarina"]
        
def synth_lead():
    return ["Lead1 (square)", "Lead2 (sawtooth)", "Lead3 (calliope)", "Lead4 (chiff)", "Lead5 (charang)", "Lead6 (voice)", "Lead7 (fifths)", "Lead8 (bass + lead)"]
        
def synth_pad():
    return ["Pad1 (new age)", "Pad2 (warm)", "Pad3 (polysynth)", "Pad4 (choir)", "Pad5 (bowed)", "Pad6 (metallic)", "Pad7 (halo)", "Pad8 (sweep)"]
        
def synth_effects():
    return ["FX1 (rain)", "FX2 (soundtrack)", "FX 3 (crystal)", "FX 4 (atmosphere)", "FX 5 (brightness)", "FX 6 (goblins)", "FX 7 (echoes)", "FX 8 (sci-fi)"]
        
def ethnic():
    return ["Sitar", "Banjo", "Shamisen", "Koto", "Kalimba", "Bag pipe", "Fiddle", "Shanai"]
        
def percussive():
    return ["Tinkle Bell", "Agogo", "Steel Drums", "Woodblock", "Taiko Drum", "Melodic Tom", "Synth Drum", "Reverse Cymbal"]
        
def sound_effects():
    return ["Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet", "Telephone Ring", "Helicopter", "Applause", "Gunshot"]


#TODO: defs
#random_violin = randrange(40,47)
#random_guitar = randrange(24,31)
#random_acoustic_guitar = randrange(24,25)
#random_guitar2 = randrange(24,31)
#random_bass = randrange(32,39)
#random_acoustic_bass = 32
