import music.midi_helper as mid
#import music.midi_instruments as instr
#import music.builder_rpt as rpt
#import numpy as np
#from model import Model
#
from mingus.core import scales, chords
from random import choice

import logging
logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------
def add_semitones(chord, semitones):
    if type(chord) is not str:
        raise Exception(f"chord ({chord}) should be a string")
    to = mid.Note(chord).number    
    return mid.Note.from_number(to+semitones).note
    
#------------------------------------------------------------------------------
def tension_chord_going_to(to_chord):
    # -5 semitones, add "7" if possible?
    return add_semitones(to_chord, -5)+"7"
  
#------------------------------------------------------------------------------
def scales_with_notes(notes):
    """ From the notes passed in argument, return all the scales that contain all the notes """
    matching_scales = []
    for s in mid.NOTES:
        scale_notes = scales.get_notes(s)
        skip = False
        for n in notes:
            if not n in scale_notes:
                skip = True
                break
        if not skip:
            matching_scales.append(s)
    return matching_scales
    
#------------------------------------------------------------------------------
def change_scale(from_chord):
    choices = scales_with_notes(chords.from_shorthand(from_chord))
    if from_chord in choices:
        choices.remove(from_chord)
    to_chord = choice(choices)
    logger.info(f"from {from_chord} ({chords.from_shorthand(from_chord)}) to {choices} ({to_chord})")
    return to_chord

#------------------------------------------------------------------------------
def jazz_scale(chord):
    if type(chord) is not str:
        raise Exception(f"chord ({chord}) should be a string")
    if "7" in chord:
        return chords.from_shorthand(chord)
    
    first = mid.Note(chord).number
    n2  = mid.Note.from_number(first+2).note
    nb3 = mid.Note.from_number(first+3).note
    n3  = mid.Note.from_number(first+4).note
    nb5  = mid.Note.from_number(first+7).note
    n5   = mid.Note.from_number(first+9).note
    #nb7   = mid.Note.from_number(first-2).note
    scale = [chord,n2,nb3,n3,nb5,n5]#,nb7]
    return scale
        