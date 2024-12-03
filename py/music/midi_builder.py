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
    
def get_mode_from_idx(list, mode):
    # TODO: Is this skewed? Probably...
    return list.index(mode)/len(list)
    
#------------------------------------------------------------------------------
def add_progression(chord_progression, attrs, scale=False, measure_duration=4, note_duration=[1], 
    octave_start=4, group_chord=False, skip_random=0.0, skip_over_silence=0, randomize=0.5, repeat_chord=1):
    
    group_chord = group_chord and attrs["_chords"].gete()
    if not group_chord:
        repeat_chord = 1
        
    beats = []
    velocity = 100
    for chord in chord_progression:
        for i in range(repeat_chord): #TODO: repeat_chord depending on measure_duration instead... 
            if not attrs["_scales"].gete():
                sub_notes = mid.NOTES
            elif scale:
                if attrs["_test_jazz_scales"].gete():
                    sub_notes = jazz_scale(chord)            
                else:
                    simplified_chord = chord.replace("7","")# TODO!! (For min/maj/etc too?)
                    sub_notes = scales.get_notes(simplified_chord)
                    # TODO: Also get more notes from the chords (more chance to get #3, then #1, etc.)                                        
                    sub_notes.extend(chords.from_shorthand(simplified_chord))
            else:
                sub_notes = chords.from_shorthand(chord)
            # TODO: This is really bad, move away from mingus...
            for idx, i in enumerate(sub_notes):
                swapped = mid.swap_accidentals(sub_notes[idx])
                sub_notes[idx] = swapped
                
            
            randomized = (random() < randomize)
            if randomized:
                shuffle(sub_notes)
                if attrs["_more_same_notes"].gete():#not attrs["_another_kind_of_random_notes"].gete():
                    new_sub_notes = []
                    for s in sub_notes:
                        new_sub_notes.append(s)
                        while random() < 0.5: #setting for percentage of times to repeat
                            new_sub_notes.append(s)
                    logger.debug(f"added same notes: {sub_notes} to {new_sub_notes}")
                    sub_notes = new_sub_notes
                
            logger.debug( f"{chord}, {sub_notes}" )
            octave = octave_start
            
            # TODO: different if note_duration is not 1.
            if len(sub_notes) == 0:
                raise Exception("No notes in chord progression!")
            if len(sub_notes) < measure_duration:
                # TODO: Remove?
                i = 0
                to = measure_duration-len(sub_notes)
                
                for idx in range(i,to):
                    sub_notes.append(sub_notes[idx])# TODO: one more octave??
            
            sub_beats = []
            
            last_note = 0
            #idx = 0
            # ++, then check every loop measure_duration
            
            current_measure_dur = 0
            duration = note_duration[int(len(note_duration)/2)]#Defaultm middle duration
            name = note=sub_notes[int(len(sub_notes)/2)]# TODO: Real middle ... same for the others... also, use 3rd instead? (TODO: last_name instead?)
            
            for i in range(len(sub_notes)):#TODO: more than that? but not while true...
                # TODO: UT and make better / settings:
                if attrs["_another_kind_of_random_notes"].gete():
                    if randomized:
                        name = pick_on_curve(sub_notes, get_mode_from_idx(sub_notes, name))
                    else:
                        name = sub_notes[i]
                else:
                    name = sub_notes[i]
                
                velocity += randrange(-10,12)#add tempo? and note speed?
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
                        
                
                #if not attrs["_another_kind_of_random_notes"] and random() < 0.3:#TODO:setting, right now always same duration? (0.3: 30% repeat duration)
                if random() < 0.3:#setting, right now always same duration? (0.3: 30% repeat duration)
                    pass #Keep same duration
                else:                    
                    if attrs["_another_kind_of_random_duration"].gete():
                        duration = pick_on_curve(note_duration, 1.0)#note_duration.index(duration)/len(note_duration))#TODO:
                        # TODO: That's not enough, it needs to be CLOSE too. Check back the c++ code, it was better...
                        note_duration.append(duration)
                    else:
                        # TODO: Make the mode last duration instead (It was done, but I think this is skewed... fix it)
                        # TODO: make it pick from previous durations too (add them to a note_duration equivalent list? with mode beind the last one...) ortransformer-like, I guess, ugh
                        duration = pick_on_curve(note_duration, get_mode_from_idx(note_duration, duration))
                if not group_chord:
                    current_measure_dur += duration
                    if current_measure_dur > measure_duration:
                        note.note = mid.SILENCE
                        dur = measure_duration - (current_measure_dur - duration)
                        if dur <= 0 or not (dur in note_duration):
                            #TODO: add silences
                            break
                        duration = dur # Because python
                        
                notes = [note]#Only one note
                if group_chord and last_note > note.number:
                    octave += 1
                    note.octave = octave
                beat = mid.Beat(duration=duration, notes=notes, name=chord)
                sub_beats.append(beat)
                
                last_note = note.number
                
            if group_chord:
            
                beat_notes = []
                for beat in sub_beats:
                    assert len(beat.notes) == 1
                    beat_notes.append(beat.notes[0])
                #TODO: duration mode from last duration too?
                common_beat = mid.Beat(pick_on_curve(note_duration, 1.0), beat_notes, name=chord)
                beats.append(common_beat)
            else:
                beats.extend(sub_beats)
            logger.debug( f"{chord}, {[b.notes[0].note for b in sub_beats]}" )
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
def split_in_colors(names_list, separator=", "):
    import colorsys
    
    while '' in names_list:
        names_list.remove('')
        
    N = len(names_list)
    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    
    desc = ""
    for i, rgb in enumerate(RGB_tuples):
        hex = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        desc += f"<font color='{hex}'>{names_list[i]}</font>{separator}"
    return desc
    
            
#------------------------------------------------------------------------------
def describe_music(app, attrs, suffix="<br /><font color='silver'>Generating...</font>"):#TODO:tr    
    desc = ""
    bool_desc_true = ""
    bool_desc_false = ""
    for a in attrs:
        setting = attrs[a]
        
        if setting.unlocked() and setting.enabled():
            name = app.tr(a[1:]).replace("instrument_","").replace("_", ' ')
            val = setting.gete()
            if setting.isBool():                
                if val:                    
                    bool_desc_true += f"{name}, "
                else:
                    bool_desc_false += f"{name}, "
            else:
                desc += f"{name}: {val}, "
                
    desc += "☑: " + split_in_colors(bool_desc_true.split(", ")) + "<br />"
    desc += "☒: " + split_in_colors(bool_desc_false.split(", "))
    
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
        beats = add_progression(chord_progression, attrs, octave_start=6, note_duration=[4], skip_random=skip_random, group_chord=False)
        channels.append(mid.Channel(beats=beats, instrument=115)) 
        beats = add_progression(chord_progression, attrs, octave_start=7, note_duration=[4], skip_random=skip_random, group_chord=False)
        beats.insert(0,mid.Beat(duration=0.25, notes=[mid.Note("", octave=1)]))
        channels.append(mid.Channel(beats=beats, instrument=113)) 
        #TODO: Change to switch_to_drops(channels, beats) ?
        
        tempo = mid.TEMPO["PRESTO"]
    
    #elif type == MusicBuildType.MINGUS:        
    else: # MusicBuildType.GAME
                  
        
        nb_chords = randrange(3,13)
        if not attrs["_chord_progression"].gete():         
            for i in range(nb_chords):
                chord_progression.append(choice(mid.NOTES))
        elif False: # TODO: Setting using scales_with_notes()?
            chord_progression = ["Am7", "G"]
            # Am7 -> Do, Sol ou Fa
        else:
            #TODO: Length (int setting)
            for i in range(nb_chords):#4,13)):
                if False:#TODO: setting?random() < 0.15:# sometimes keep the same
                    pass
                else:
                    chord = add_semitones(chord, 5)
                if False:#TODO: setting? random() < 0.25:# sometimes add tension chords:
                    chord_progression.append(tension_chord_going_to(chord))
                chord_progression.append(chord)
            
        if attrs["_scales"].gete():
            if not attrs["_chord_progression"].gete(): 
                music_desc += f"Random "
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
        
        
        skip_random_bass = 0.4 if attrs["_test_jazz_scales"].gete() else 0.05
        skip_random_melody = 0.2 if attrs["_test_jazz_scales"].gete() else 0.1
        randomize = 0.2 if attrs["_less_random_test"].gete() else 1.0 # TODO: int
        # TODO: Flip sometimes?
        #note_duration1 = [2]# TODO: Should match. Go to my 8 years old code and start from that instead of doing nothing really useful here...
        #note_duration2 = [1]
        if attrs["_frequency"].gete():
            # TODO: I really need to have measures here, not random things, so that they MATCH (bass and melody)            
            # From least to most probable
            note_duration1 = [2]#Until repeat_chord is fixed[0.25, 3, 1.5, 0.5, 4, 1, 2, 2]
            note_duration2 = [4, 3, 0.25, 1.5, 2, 0.5, 1, 1]
        else:
            note_duration1 = [4]
            note_duration2 = [4]
            skip_random_bass = 0.0
            skip_random_melody = 0.0
        
        skip_over_silence = 0
        repeat_chord = 2#TODO: Remove repeat_chord! (Use measure_time instead)
        
        #for chord in chord_progression:
        #    beats.append(mid.Beat(duration=1, notes=[mid.Note(chords.from_shorthand(chord)[0], OCTAVE)]))
        if not s_drops and attrs["_bass_tracks"].gete():
            beats = add_progression(chord_progression, attrs, octave_start=OCTAVE, note_duration=note_duration1, skip_random=skip_random_bass, group_chord=True, skip_over_silence=skip_over_silence, repeat_chord=repeat_chord, randomize=randomize)        
            channels.append(mid.Channel(beats=beats, instrument=instrument_bass)) 
        
        #beats = add_progression(chord_progression, attrs, octave_start=OCTAVE, note_duration=note_duration1, skip_random=skip_random_bass, group_chord=True, skip_over_silence=skip_over_silence, repeat_chord=repeat_chord)
        #channels.append(mid.Channel(beats=beats, instrument=instrument_bass2)) 
        
        #5 sometimes? needs to go higher sometimes?
        OCTAVE = 4
        beats = add_progression(chord_progression, attrs, scale=True, octave_start=OCTAVE, note_duration=note_duration2, skip_random=skip_random_melody, group_chord=False, randomize=randomize, skip_over_silence=skip_over_silence)
        if not s_drops:
            channels.append(mid.Channel(beats=beats, instrument=instrument_melody)) 
        else:
            switch_to_drops(channels, beats)
        
        #OCTAVE = 4
        #beats = add_progression(chord_progression, attrs, octave_start=OCTAVE, note_duration=note_duration2, skip_random=skip_random_melody, group_chord=False, randomize=randomize, skip_over_silence=skip_over_silence)
        #channels.append(mid.Channel(beats=beats, instrument=118, channel_id_override=9)) 
    
    
    
        
    mid.make_file(filename, channels, tempo=tempo)
    music_desc += f"tempo: <font color='red'>{tempo_str}</font> ({tempo}bps)"
    logger.info(music_desc)
    return describe_music(app, attrs, music_desc), tempo