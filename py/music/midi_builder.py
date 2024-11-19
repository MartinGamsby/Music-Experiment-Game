import music.midi_helper as mid
from mingus.core import chords
import random
from enum import Enum

import logging
logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
class MusicBuildType(Enum):
    FILE, DROPS, GAME = range(3)

#------------------------------------------------------------------------------
def add_chord_progression(chord_progression, measure_duration=4, note_duration=[1], 
    octave_start=4, group_chord=False, skip_random=0.0, skip_over_silence=0, randomize=False, repeat_chord=1):
    
    beats = []
    for chord in chord_progression:
        for i in range(repeat_chord): #TODO: repeat_chord depending on measure_duration instead... 
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
                note = mid.Note(note=name, octave=octave)
                
                if skip_random > 0:
                    if random.random() < skip_random:
                        # Not always silence, perhaps?
                        if random.random() > skip_over_silence:# TODO:
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
                beat = mid.Beat(duration=random.choice(note_duration), notes=notes, name=chord)
                sub_beats.append(beat)
                
                last_note = note.number
                
            if randomize:
                random.shuffle(sub_beats)
                
            if group_chord:
            
                beat_notes = []
                for beat in sub_beats:
                    assert len(beat.notes) == 1
                    beat_notes.append(beat.notes[0])
                common_beat = mid.Beat(random.choice(note_duration), beat_notes, name=chord)
                beats.append(common_beat)
            else:
                beats.extend(sub_beats)
            #notes.extend(sub_notes)
    return beats
    
#------------------------------------------------------------------------------
def make_midi(filename, type):

    #chord_progression = ["Cmaj", "Fmaj", "Cmaj", "Cmaj7", "Fmaj", "Gmin", "Fmaj", "Gmin", "Cmaj7", "Fmaj", "Cmaj", "Fmaj", "Gmin", "Cmaj", "Cmaj7", "Cmaj"]
    #chord_progression = ["Cmaj", "Fmaj", "Bmaj", "Emaj", "Amaj", "Dmaj", "Gmaj", "Cmaj"]
    chord_progression = ["C", "F", "A#", "D#", "G#", "C#", "F#", "B", "E", "A", "D", "G", "C"]
    
    channels = []


    if type == MusicBuildType.DROPS:
        # TODO: Notes with the octave. Return Note() here, and make sure we go up if we go over G.
        beats = add_chord_progression(chord_progression, octave_start=6, note_duration=[3], skip_random=0.33, group_chord=False)
        channels.append(mid.Channel(beats=beats, instrument=115)) 
        beats = add_chord_progression(chord_progression, octave_start=7, note_duration=[3], skip_random=0.33, group_chord=False)
        beats.insert(0,mid.Beat(duration=0.25, notes=[mid.Note("", octave=1)]))
        channels.append(mid.Channel(beats=beats, instrument=113)) 
    
    else: # MusicBuildType.GAME
    
        instrument1 = int(random.random()*47)#119)
        instrument2 = int(random.random()*47)#119)
        instrument3 = int(random.random()*47)#119)
    
        OCTAVE = 4
        beats = []
        #skip_random = 0.5#0.5 # 0 to 1
        #randomize = True
        #note_duration1 = [2,2,4,8]
        #note_duration2 = [0.5,0.5,1,2]
        #skip_over_silence = 0.5
        #repeat_chord = 1
        skip_random = 0.4
        randomize = True#True#
        note_duration1 = [2]# TODO: Should match. Go to my 8 years old code and start from that instead of doing nothing really useful here...
        note_duration2 = [1]
        skip_over_silence = 0
        repeat_chord = 2
        
        #for chord in chord_progression:
        #    beats.append(mid.Beat(duration=1, notes=[mid.Note(chords.from_shorthand(chord)[0], OCTAVE)]))
        beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration1, skip_random=skip_random, group_chord=True, skip_over_silence=skip_over_silence, repeat_chord=repeat_chord)
        channels.append(mid.Channel(beats=beats, instrument=instrument1)) 
        beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration1, skip_random=skip_random, group_chord=True, skip_over_silence=skip_over_silence, repeat_chord=repeat_chord)
        channels.append(mid.Channel(beats=beats, instrument=instrument2)) 
        
        
        OCTAVE = 5
        beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration2, skip_random=skip_random, group_chord=False, randomize=randomize, skip_over_silence=skip_over_silence)
        channels.append(mid.Channel(beats=beats, instrument=instrument3)) 
    
    
    
        
    mid.make_file(filename, channels, tempo=mid.TEMPO["VIVACE"])