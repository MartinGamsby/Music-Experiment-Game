import music.midi_helper as mid
import music.builder_notes as notes
#import numpy as np
#from model import Model
#
#from mingus.core import chords, scales
from random import random #, choice, randrange, shuffle
from enum import Enum

import logging
logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------
def get_rpt_progression(chord_progression, scale_progression, nb_chords):
    if len(chord_progression) != 1:
        raise Exception(f"chord_progression ({chord_progression}) needs to have a starting chord")
    if len(scale_progression) != 1:
        raise Exception(f"scale_progression ({scale_progression}) needs to have a starting chord")
    class ProgressionsState(Enum):
        R, P, T, End = range(4)
            
    ret_chords = [chord_progression[0]]
    ret_scales = [scale_progression[0]]
    desc = "R: I"
            
    first_chord = chord_progression[0]
    for i in range(nb_chords+3): # Breaking lower, adding 3 to make sure we end on an R
        state = ProgressionsState(i%ProgressionsState.End.value)
        if i >= len(chord_progression):
            logger.debug(f"state {state}, from chord {last_chord}" )
            
            if state == ProgressionsState.P:
                if len(ret_chords) >= nb_chords:
                    logger.debug("done")
                    break
                # P: ii or IV
                if random() < 0.5:
                    # ii:
                    new_chord = notes.add_semitones(first_chord, 2) + "min"
                    desc += ", P: ii"
                    logger.debug(f"P: ii ({first_chord} -> {new_chord})")
                else:
                    # IV:
                    new_chord = notes.add_semitones(first_chord, 5)
                    desc += ", P: IV"
                    logger.debug(f"P: IV ({first_chord} -> {new_chord})")
                    
            elif state == ProgressionsState.T:
                # T: V7 or vii*
                if random() < 0.5:
                    # V7:
                    new_chord = notes.add_semitones(first_chord, -5) + "7"
                    desc += ", T: V7"
                    logger.debug(f"T: V7 ({first_chord} -> {new_chord})")
                else:
                    #vii*
                    new_chord = notes.add_semitones(first_chord, -1) + "dim"
                    desc += ", T: vii*"
                    logger.debug(f"T: vii* ({first_chord} -> {new_chord})")
                
            elif state == ProgressionsState.R:            
                # R: I or vi
                if random() < 0.5:
                    # I:
                    new_chord = first_chord
                    desc += ", R: I"
                    logger.debug(f"R: I ({first_chord} -> {new_chord})")
                else:
                    # vi:
                    new_chord = notes.add_semitones(first_chord, -3) + "min"
                    desc += ", R: vi/I"
                    logger.debug(f"R: vi ({first_chord} -> {new_chord})")
                # Change first_chord?
                first_chord = new_chord.replace("min","")
            ret_chords.append(new_chord)
            ret_scales.append(first_chord)
            
        last_chord = ret_chords[i]
        
        
        
    return mid.MeasureDesc(ret_chords, ret_scales, desc)
