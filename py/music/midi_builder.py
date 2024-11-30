import music.midi_helper as mid
import music.midi_instruments as instr
import numpy as np
from model import Model

from mingus.core import chords, scales
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
                velocity += randrange(-int(velocity/4+9),int(velocity/4+13))#add tempo? and note speed?
                velocity = clamp(36, velocity, 127)
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
            logger.info( f"{chord}, {[b.notes[0].note for b in sub_beats]}" )
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
def switch_to_drops(channels, beats):    
    for b in beats:
        for n in b.notes:
            n.octave = 6
    channels.append(mid.Channel(beats=beats, instrument=115))
    
    beats = beats.copy()
    for b in beats:
        for n in b.notes:
            n.octave = 7
    # 0.25 offset for the drop effect        
    beats.insert(0,mid.Beat(duration=0.25, notes=[mid.Note("", octave=1)]))
    channels.append(mid.Channel(beats=beats, instrument=113))
            
#------------------------------------------------------------------------------
def describe_music(app, attrs, suffix="<br /><font color='silver'>Generating...</font>"):#TODO:tr    
    desc = ""
    for a in attrs:
        if attrs[a].unlocked() and attrs[a].enabled():
            desc += f"{app.tr(a[1:])}: {attrs[a].gete()}, "
    
    return desc + suffix

#------------------------------------------------------------------------------
def pick_on_curve(choices, mode=0.5):
    nb = len(choices)
    if not 0 <= mode <= 1:
        raise Exception(f"{mode} needs to be between 0 and 1")
    return choices[int(np.random.triangular(0, int(nb*mode), nb, size=None))]
    
            
#------------------------------------------------------------------------------
def make_midi(filename, app, attrs, type):
    
    music_desc = "<br /><font color='silver'>Generated:</font><br />"# TODO: translate
    s_drops = False #TODO
    
    chord = choice(mid.NOTES)
    chord_progression = [chord]
    
    #tempo_choices = ["GRAVE", "LARGO", "LARGHETTO", "LENTO", "ADAGIO", "ADAGIETTO", "ANDANTE", "ANDANTINO", "MODERATO", "ALLEGRETTO", "ALLEGRO", "VIVACE", "PRESTO", "PRETISSIMO"]
    tempo_choices = ["ADAGIO", "ADAGIETTO", "ANDANTE", "ANDANTINO", "MODERATO", "ALLEGRETTO", "ALLEGRO", "VIVACE", "PRESTO", "PRETISSIMO"]
    
    # Easier for now:
    tempo_str = pick_on_curve(tempo_choices, 0.5)
    tempo = mid.TEMPO[tempo_str]
    
    #if random() > 0.8:# sometimes start with tension?
    #    chord_progression = [tension_chord_going_to(chord),chord]
        
    channels = []

    if type == MusicBuildType.DROPS:
        # TODO: Notes with the octave. Return Note() here, and make sure we go up if we go over G.
        #skip_random = 0.33
        skip_random = 0.0
        beats = add_chord_progression(chord_progression, octave_start=6, note_duration=[4], skip_random=skip_random, group_chord=False)
        channels.append(mid.Channel(beats=beats, instrument=115)) 
        beats = add_chord_progression(chord_progression, octave_start=7, note_duration=[4], skip_random=skip_random, group_chord=False)
        beats.insert(0,mid.Beat(duration=0.25, notes=[mid.Note("", octave=1)]))
        channels.append(mid.Channel(beats=beats, instrument=113)) 
        
        tempo = mid.TEMPO["PRESTO"]
    
    #elif type == MusicBuildType.MINGUS:        
    else: # MusicBuildType.GAME
                  
        
        if False: # TODO: Setting using scales_with_notes()?
            chord_progression = ["Am7", "G"]
            # Am7 -> Do, Sol ou Fa
        else:
            for i in range(randrange(2,4)):#4,13)):
                if random() < 0.2:# sometimes keep the same
                    pass
                else:
                    chord = add_semitones(chord, 5)
                chord_progression.append(tension_chord_going_to(chord))
                chord_progression.append(chord)
            
        music_desc += f"<font color='blue'>Chords:</font> {', '.join(chord_progression)}<br />"

        # randrange(0,79)
        
        possible_instruments = []
        
        # Do I need "_instrument" ? probably not...
        if attrs["_instrument_piano"].gete():
            possible_instruments.extend(instr.piano())
        if attrs["_instrument_piano_electric"].gete():
            possible_instruments.extend(instr.piano_electric())
        if attrs["_instrument_percussions"].gete():
            possible_instruments.extend(instr.percussive())
        if attrs["_instrument_chromatic_percussion"].gete():
            possible_instruments.extend(instr.chromatic_percussion())
        if attrs["_instrument_organ"].gete():
            possible_instruments.extend(instr.organ())
        if attrs["_instrument_guitar"].gete():
            possible_instruments.extend(instr.guitar())
        if attrs["_instrument_guitar_electric"].gete():
            possible_instruments.extend(instr.guitar_electric())
        if attrs["_instrument_bass"].gete():
            possible_instruments.extend(instr.bass())
        if attrs["_instrument_bass_electric"].gete():
            possible_instruments.extend(instr.bass_electric())
        if attrs["_instrument_strings"].gete():
            possible_instruments.extend(instr.strings())
        if attrs["_instrument_ensemble"].gete():
            possible_instruments.extend(instr.ensemble())
        if attrs["_instrument_brass"].gete():
            possible_instruments.extend(instr.brass())
        if attrs["_instrument_reed"].gete():
            possible_instruments.extend(instr.reed())
        if attrs["_instrument_free_reed"].gete():
            possible_instruments.extend(instr.free_reed())
        if attrs["_instrument_pipe"].gete():
            possible_instruments.extend(instr.pipe())
        if attrs["_instrument_synth_lead"].gete():
            possible_instruments.extend(instr.synth_lead())
        if attrs["_instrument_synth_pad"].gete():
            possible_instruments.extend(instr.synth_pad())
        if attrs["_instrument_synth_effects"].gete():
            possible_instruments.extend(instr.synth_effects())
        if attrs["_instrument_ethnic"].gete():
            possible_instruments.extend(instr.ethnic())
        if attrs["_instrument_sound_effects"].gete():
            possible_instruments.extend(instr.sound_effects())
            
        if possible_instruments:            
            instrument_melody, name_melody = instr.random_instrument(possible_instruments)
            if attrs["_multi_instruments"].gete():
                instrument_bass, name_bass = instr.random_instrument(possible_instruments)
            else:
                instrument_bass, name_bass = instrument_melody, name_melody
                
            instrument_bass2, name_bass2 = instr.random_instrument(possible_instruments)
            
            music_desc += f"<font color='green'>melody:</font> {name_melody}"
            if attrs["_bass_tracks"].gete():
                music_desc += f", <font color='green'>bass:</font> {name_bass}"
            music_desc += "<br />"
        else:
            s_drops = True
            
        #if random() < 0.3:
        #    instrument_bass = randrange(56, 79)
    
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
        randomize = 0.2#0.2
        # TODO: Flip sometimes?
        #note_duration1 = [2]# TODO: Should match. Go to my 8 years old code and start from that instead of doing nothing really useful here...
        #note_duration2 = [1]
        if attrs["_frequency"].gete():
            # TODO: I really need to have measures here, not random things, so that they MATCH (bass and melody)
            
            note_duration1 = [2]#[0.5,0.5,1,1,1,1,1,2,2,2,2,2,2,4,4,4,4]#[2]#[0.5,0.5,0.5,0.5,1,1,2,4,4]#[1,1,2,2,2,2,2,4]
            note_duration2 = [1]#[0.25,0.25,0.25,0.25,0.5,0.5,1,2,2,2,2]#[1]#[0.25,0.25,0.25,0.25,0.5,0.5,1,2,2,2,2]#[0.5,0.5,1,1,1,1,1,2]
        else:
            note_duration1 = [0.5,0.5,1,1,1,1,1,2,2,2,2,2,2,4,4,4,4]#[2]#[0.5,0.5,0.5,0.5,1,1,2,4,4]#[1,1,2,2,2,2,2,4]
            note_duration2 = [0.25,0.25,0.25,0.25,0.5,0.5,1,2,2,2,2]#[1]#[0.25,0.25,0.25,0.25,0.5,0.5,1,2,2,2,2]#[0.5,0.5,1,1,1,1,1,2]
            skip_random = 0.0
            skip_random2 = 0.0
            randomize = 1.0
        
        skip_over_silence = 0
        repeat_chord = 2
        
        #for chord in chord_progression:
        #    beats.append(mid.Beat(duration=1, notes=[mid.Note(chords.from_shorthand(chord)[0], OCTAVE)]))
        if not s_drops and attrs["_bass_tracks"].gete():
            beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration1, skip_random=skip_random, group_chord=True, skip_over_silence=skip_over_silence, repeat_chord=repeat_chord)        
            channels.append(mid.Channel(beats=beats, instrument=instrument_bass)) 
        
        #beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration1, skip_random=skip_random, group_chord=True, skip_over_silence=skip_over_silence, repeat_chord=repeat_chord)
        #channels.append(mid.Channel(beats=beats, instrument=instrument_bass2)) 
        
        OCTAVE = 4
        beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration2, skip_random=skip_random2, group_chord=False, randomize=randomize, skip_over_silence=skip_over_silence)
        if not s_drops:
            channels.append(mid.Channel(beats=beats, instrument=instrument_melody)) 
        else:
            switch_to_drops(channels, beats)
        
        #OCTAVE = 4
        #beats = add_chord_progression(chord_progression, octave_start=OCTAVE, note_duration=note_duration2, skip_random=skip_random2, group_chord=False, randomize=randomize, skip_over_silence=skip_over_silence)
        #channels.append(mid.Channel(beats=beats, instrument=118, channel_id_override=9)) 
    
    
    
        
    mid.make_file(filename, channels, tempo=tempo)
    music_desc += f"tempo: <font color='red'>{tempo_str}</font> ({tempo}bps)"
    logger.info(music_desc)
    return describe_music(app, attrs, music_desc), tempo