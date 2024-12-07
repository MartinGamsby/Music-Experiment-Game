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
def get_rpt_progression(first_chord, first_scale, nb_chords):
    measure = mid.MeasureDesc([first_chord], [first_scale], [])
    
    if len(measure.chord_progression) != 1:
        raise Exception(f"chord_progression ({measure.chord_progression}) needs to have a starting chord")
    if len(measure.scale_progression) != 1:
        raise Exception(f"scale_progression ({measure.scale_progression}) needs to have a starting chord")
    class ProgressionsState(Enum):
        R, P, T, End = range(4)
            
    measure.desc.append("R: I")
    
    first_chord = measure.chord_progression[0]
    for i in range(nb_chords+3): # Breaking lower, adding 3 to make sure we end on an R
        state = ProgressionsState(i%ProgressionsState.End.value)
        if i >= len(measure.chord_progression):
            logger.debug(f"state {state}, from chord {last_chord}" )
            
            if state == ProgressionsState.P:
                if len(measure.chord_progression) >= nb_chords:
                    logger.debug("done")
                    break
                # P: ii or IV
                if random() < 0.5:
                    # ii:
                    new_chord = notes.add_semitones(first_chord, 2) + "min"
                    measure.desc.append("P: ii")
                    logger.debug(f"P: ii ({first_chord} -> {new_chord})")
                else:
                    # IV:
                    new_chord = notes.add_semitones(first_chord, 5)
                    measure.desc.append("P: IV")
                    logger.debug(f"P: IV ({first_chord} -> {new_chord})")
                    
            elif state == ProgressionsState.T:
                # T: V7 or vii*
                if random() < 0.5:
                    # V7:
                    new_chord = notes.add_semitones(first_chord, -5) + "7"
                    measure.desc.append("T: V7")
                    logger.debug(f"T: V7 ({first_chord} -> {new_chord})")
                else:
                    #vii*
                    new_chord = notes.add_semitones(first_chord, -1) + "dim"
                    measure.desc.append("T: vii*")
                    logger.debug(f"T: vii* ({first_chord} -> {new_chord})")
                
            elif state == ProgressionsState.R:            
                # R: I or vi
                if random() < 0.5:
                    # I:
                    new_chord = first_chord
                    measure.desc.append("R: I")
                    logger.debug(f"R: I ({first_chord} -> {new_chord})")
                else:
                    # vi:
                    new_chord = notes.add_semitones(first_chord, -3) + "min"
                    measure.desc.append("R: vi")
                    logger.debug(f"R: vi ({first_chord} -> {new_chord})")
                # Change first_chord?
                #TODO: That's not how you do it... first_chord = new_chord.replace("min","")
            measure.chord_progression.append(new_chord)
            measure.scale_progression.append(first_chord)
            
        last_chord = measure.chord_progression[i]
        
        
        
    return measure
