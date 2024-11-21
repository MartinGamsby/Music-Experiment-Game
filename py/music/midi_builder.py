import music.midi_helper as mid
import music.midi_instruments as instr

from mingus.core import chords
from random import random, choice, randrange, shuffle
from enum import Enum

import logging
logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
class MusicBuildType(Enum):
    FILE, DROPS, GAME, MINGUS = range(4)

#------------------------------------------------------------------------------
def add_semitones(chord, semitones):
    if type(chord) is not str:
        raise Exception(f"chord ({chord}) should be a string")
    to = mid.Note(chord).number    
    return mid.Note.from_number(to-5).note
    

#------------------------------------------------------------------------------
def tension_chord_going_to(to_chord):
    # -5 semitones, add "7" if possible?
    return add_semitones(to_chord, -5)+"7"
    
#------------------------------------------------------------------------------
def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))
    
    
#------------------------------------------------------------------------------
TEST_JAZZ=False#True
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
    
    
    
#------------------------------------------------------------------------------
def add_chord_progression(chord_progression, measure_duration=4, note_duration=[1], 
    octave_start=4, group_chord=False, skip_random=0.0, skip_over_silence=0, randomize=0.5, repeat_chord=1):
    
    beats = []
    velocity = 100
    for chord in chord_progression:
        for i in range(repeat_chord): #TODO: repeat_chord depending on measure_duration instead... 
            if TEST_JAZZ:
                sub_notes = jazz_scale(chord)            
            else:
                sub_notes = chords.from_shorthand(chord)
            logger.debug( f"{chord}, {sub_notes}" )
            octave = octave_start
            
            # TODO: different if note_duration is not 1.
            if len(sub_notes) == 0:
                raise Exception("No notes in chord progression!")
            if len(sub_notes) > measure_duration:
                sub_notes = sub_notes[:measure_duration]
            if len(sub_notes) < measure_duration:
                i = 0
                to = measure_duration-len(sub_notes)
                
                for idx in range(i,to):
                    sub_notes.append(sub_notes[idx])# TODO: one more octave??
            
            sub_beats = []
            last_note = 0
            
            for name in sub_notes:
                velocity += randrange(-20,22)
                velocity = clamp(25, velocity, 127)
                note = mid.Note(note=name, octave=octave, velocity=velocity)
                logger.debug(velocity)
                
                if skip_random > 0:
                    if random() < skip_random:
                        # Not always silence, perhaps?
                        if random() > skip_over_silence:# TODO:
                            # Add silence
                            note.note = mid.SILENCE
                            logger.debug("SILENCE")
                        else:
                            #Skip to next note
                            logger.debug("SKIP")
                            continue
                        
                        
                notes = [note]#Only one note
                if last_note > note.number:
                    octave += 1
                    note.octave = octave
                beat = mid.Beat(duration=choice(note_duration), notes=notes, name=chord)
                sub_beats.append(beat)
                
                last_note = note.number
                
            if random() < randomize:
                shuffle(sub_beats)
                
            if group_chord:
            
                beat_notes = []
                for beat in sub_beats:
                    assert len(beat.notes) == 1
                    beat_notes.append(beat.notes[0])
                common_beat = mid.Beat(choice(note_duration), beat_notes, name=chord)
                beats.append(common_beat)
            else:
                beats.extend(sub_beats)
            #notes.extend(sub_notes)
    return beats
    
#------------------------------------------------------------------------------
def add_note(beats, note):
    beats.append(mid.Beat(duration=1, notes=[mid.Note.from_number(int(note))], name=""))#duration?
    
#------------------------------------------------------------------------------
def add_notes(beats, notes):
    all_notes = []
    for n in notes:
        all_notes.append(mid.Note.from_number(int(n)))
    beats.append(mid.Beat(duration=1, notes=all_notes, name=""))#duration?
    
#------------------------------------------------------------------------------
def add_silence(beats):
    beats.append(mid.Beat(duration=1, notes=[mid.Note()], name=""))#duration?   

#------------------------------------------------------------------------------
def make_midi(filename, type):

    chord = choice(mid.NOTES)
    
    chord_progression = [chord]
    
    #if random() > 0.8:# sometimes start with tension?
    #    chord_progression = [tension_chord_going_to(chord),chord]
        
    
    for i in range(randrange(4,13)):
        if random() < 0.2:# sometimes keep the same
            pass
        else:
            chord = add_semitones(chord, 5)
        chord_progression.append(tension_chord_going_to(chord))
        chord_progression.append(chord)
        
    logger.info(f"chord_progression: {chord_progression}")

    channels = []

    if type == MusicBuildType.DROPS:
        # TODO: Notes with the octave. Return Note() here, and make sure we go up if we go over G.
        beats = add_chord_progression(chord_progression, octave_start=6, note_duration=[3], skip_random=0.33, group_chord=False)
        channels.append(mid.Channel(beats=beats, instrument=115)) 
        beats = add_chord_progression(chord_progression, octave_start=7, note_duration=[3], skip_random=0.33, group_chord=False)
        beats.insert(0,mid.Beat(duration=0.25, notes=[mid.Note("", octave=1)]))
        channels.append(mid.Channel(beats=beats, instrument=113)) 
    
    #elif type == MusicBuildType.MINGUS:        
    else: # MusicBuildType.GAME
                
        # bass, I think
        instrument1 = instr.random_instrument(instr.acoustic_bass())#randrange(0,79)#47)#piano#int(random_acoustic_bass)
        # 2nd bass, I think
        instrument2 = instr.midi_instrument("Acoustic Bass")#instr.random_instrument(instr.acoustic_guitar())#randrange(0,79)#47)#piano#int(random_guitar2)
        # +1 octave
        instrument3 = 0#instr.random_instrument(instr.piano())#randrange(0,79)#47)#piano#int(random_acoustic_guitar)
        
        #if random() < 0.3:
        #    instrument1 = randrange(56, 79)
    
        OCTAVE = 3 # TODO: Get ovtace from instrument (use mingus?)
        beats = []
        #skip_random = 0.5#0.5 # 0 to 1
        #randomize = True
        #note_duration1 = [2,2,4,8]
        #note_duration2 = [0.5,0.5,1,2]
        #skip_over_silence = 0.5
        #repeat_chord = 1
        skip_random = 0.4 if TEST_JAZZ else 0.67
        skip_random2 = 0.2 if TEST_JAZZ else 0.42
        randomize = 0.2#True#
        #note_duration1 = [2]# TODO: Should match. Go to my 8 years old code and start from that instead of doing nothing really useful here...
        #note_duration2 = [1]
        note_duration1 = [1,1,2,4]#[1,1,2,2,2,2,2,4]
        note_duration2 = [0.5,0.5,1,2]#[0.5,0.5,1,1,1,1,1,2]
        skip_over_silence = 0
        repeat_chord = 2
        
        #for chord in chord_progression:
        #    beats.append(mid.Beat(duration=1, notes=[mid.Note(chords.from_shorthand(chord)[0], OCTAVE)]))
        beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration1, skip_random=skip_random, group_chord=True, skip_over_silence=skip_over_silence, repeat_chord=repeat_chord)
        channels.append(mid.Channel(beats=beats, instrument=instrument1)) 
        
        #beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration1, skip_random=skip_random, group_chord=True, skip_over_silence=skip_over_silence, repeat_chord=repeat_chord)
        #channels.append(mid.Channel(beats=beats, instrument=instrument2)) 
        
        
        OCTAVE = 4
        beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration2, skip_random=skip_random2, group_chord=False, randomize=randomize, skip_over_silence=skip_over_silence)
        channels.append(mid.Channel(beats=beats, instrument=instrument3)) 
        
        #OCTAVE = 4
        #beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration2, skip_random=skip_random2, group_chord=False, randomize=randomize, skip_over_silence=skip_over_silence)
        #channels.append(mid.Channel(beats=beats, instrument=118, channel_id_override=9)) 
    
    
    
        
    mid.make_file(filename, channels, tempo=mid.TEMPO["VIVACE"])