import music.midi_helper as mid
import music.midi_instruments as instr
import music.builder_rpt as rpt
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
def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))
        
#------------------------------------------------------------------------------
def get_mode_from_idx(list, mode):
    # TODO: Is this skewed? Probably...
    return list.index(mode)/len(list)
    
#------------------------------------------------------------------------------
def pick_duration(attrs, choices_duration, last_duration, measure_duration, current_measure_dur, add_silence):
    silenced = False
    #if not attrs["_another_kind_of_random_notes"] and random() < 0.3:#TODO:setting, right now always same duration? (0.3: 30% repeat duration)
    if False:#TODO:random() < 0.3:#setting, right now always same duration? (0.3: 30% repeat duration)
        duration = last_duration
        pass #Keep same duration
    else:                    
        if attrs["_another_kind_of_random_duration"].gete():
            
            
            if False:# 3rd type of random??
                # The longer the list, the less it's skewed? (Need to change pick_on_curve for that)
                if len(choices_duration)>20:
                    duration = choice(choices_duration)
                else:
                    duration = pick_on_curve(choices_duration, 1.0)#choices_duration.index(duration)/len(choices_duration))#TODO:
                # TODO: That's not enough, it needs to be CLOSE too. Check back the c++ code, it was better...
                diff = int(4 - duration)+2
                print(f"DIFF: {diff} (for {duration})")
                for i in range(diff):
                    choices_duration.append(duration)
            else:
                duration = pick_on_curve(choices_duration, 1.0)
                choices_duration.append(duration)
                
        else:
            # TODO: Make the mode last duration instead (It was done, but I think this is skewed... fix it)
            # TODO: make it pick from previous durations too (add them to a choices_duration equivalent list? with mode beind the last one...) ortransformer-like, I guess, ugh
            duration = pick_on_curve(choices_duration, get_mode_from_idx(choices_duration, last_duration))
        last_duration = duration
    if add_silence:
        if current_measure_dur > measure_duration:
            silenced = True
            duration = measure_duration - current_measure_dur
            if duration <= 0:
                return -1, True
            elif not (duration in choices_duration):
                pass# not break, but don't update last_duration
            else:
                last_duration = duration
        else:
            last_duration = duration
        
    return duration, silenced# TODO Is last_duration, current_measure_dur, etc. updated? Python?
    
#------------------------------------------------------------------------------
def add_progression(chord_progression, scale_progression, attrs, scale=False, measure_duration=4, choices_duration=[1], 
    octave_start=4, group_chord=False, skip_random=0.0, skip_over_silence=0, randomize=0.5):
    
    group_chord = group_chord and attrs["_chords"].gete()
        
    beats = []
    velocity = 100
    for idx, chord in enumerate(chord_progression):
        scale_used = scale_progression[idx]
        
        last_group_duration = choices_duration[int(len(choices_duration)/2)]#Defaultm middle duration
        current_group_measure_dur = 0
        for i in range(8 if group_chord else 1):#TODO: more than that? but not while true... (And more for group_chord!
        #for i in range(repeat_chord): #TODO: repeat_chord depending on measure_duration instead... 
            if not attrs["_scales"].gete():
                sub_notes = mid.NOTES
            elif scale:
                if attrs["_test_jazz_scales"].gete():
                    sub_notes = jazz_scale(scale_used)            
                else:
                    #simplified_chord = chord.replace("7","")# TODO!! (For min/maj/etc too?)
                    sub_notes = scales.get_notes(scale_used)
                    # TODO: Also get more notes from the chords (more chance to get #3, then #1, etc.)                                        
                    #sub_notes.extend(chords.from_shorthand(chord))
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
            else:
                if attrs["_less_random_test"].gete() and random() < 0.5:
                    sub_notes.reverse()
                
            logger.debug( f"{chord}, {sub_notes}" )
            octave = octave_start
            
            # TODO: different if choices_duration is not 1.
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
            last_duration = choices_duration[int(len(choices_duration)/2)]#Defaultm middle duration
            name = note=sub_notes[int(len(sub_notes)/2)]# TODO: Real middle ... same for the others... also, use 3rd instead? (TODO: last_name instead?)
            
            for i in range(len(sub_notes)):#TODO: more than that? but not while true... (And more for group_chord!
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
                        
                
                duration, silenced = pick_duration(attrs, choices_duration, last_duration, measure_duration, current_measure_dur, add_silence = (not group_chord))
                if duration <= 0:
                    break
                if silenced:
                    note.note = mid.SILENCE
                current_measure_dur += duration
                #print(duration, last_duration, current_measure_dur)
                
                
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
                
                               
                
                duration, silenced = pick_duration(attrs, choices_duration, last_group_duration, measure_duration, current_group_measure_dur, add_silence = True)
                if duration <= 0:
                    break
                if silenced:
                    for note in beat_notes:
                        note.note = mid.SILENCE
                current_group_measure_dur += duration
                #print(duration, last_group_duration, current_group_measure_dur)
                
                
                common_beat = mid.Beat(duration, beat_notes, name=chord)
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
def describe_music(app, attrs, suffix):#TODO:tr    
    desc = ""
    bool_desc_true = ""
    bool_desc_false = ""
    for a in attrs:
        setting = attrs[a]
        
        if setting.unlocked() and setting.enabled():
            name = app.tr(a[1:]).replace("instrument_","").replace("_", ' ').title()
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
    
    music_desc = f"<br /><font color='silver'>{app.tr("GENERATED_")}</font><br />"# TODO: translate
    s_drops = False #TODO
    
    chord = choice(mid.NOTES)
    chord_progression = [chord]
    scale_progression = [chord]
    
    tempo_choices = ["ADAGIO", "ADAGIETTO", "ANDANTE", "ANDANTINO", "MODERATO", "ALLEGRETTO", "ALLEGRO", "VIVACE", "PRESTO", "PRETISSIMO"]
    
    if attrs["_slower"].gete():
        tempo_choices = ["GRAVE", "LARGO", "LARGHETTO", "LENTO", "ADAGIO", "ADAGIETTO", "ANDANTE", "ANDANTINO", "MODERATO"]
    if attrs["_faster"].gete():
        tempo_choices = ["ANDANTE", "ANDANTINO", "MODERATO", "ALLEGRETTO", "ALLEGRO", "VIVACE", "PRESTO", "PRETISSIMO"]
        
        
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
        beats = add_progression(chord_progression, scale_progression, attrs, octave_start=6, choices_duration=[4], skip_random=skip_random, group_chord=False)
        channels.append(mid.Channel(beats=beats, instrument=115)) 
        beats = add_progression(chord_progression, scale_progression, attrs, octave_start=7, choices_duration=[4], skip_random=skip_random, group_chord=False)
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
            scale_progression = chord_progression
        elif False: # TODO: Setting using scales_with_notes()?
            chord_progression = ["Am7", "G"]
            # Am7 -> Do, Sol ou Fa
        else:
            #TODO: Length (int setting)
            if attrs["_chord_progression2"].gete():
                
                # TODO: use mid.MeasureDesc everywhere
                result = rpt.get_rpt_progression(chord_progression, scale_progression, nb_chords)
                chord_progression = result.chords
                scale_progression = result.scales
                desc = result.desc
                music_desc += f"<font color='darkblue'>{app.tr("LOGIC_")}</font> {desc}<br />"
            else: #_chord_progression
                for i in range(nb_chords):#4,13)):
                    if False:#TODO: setting?random() < 0.15:# sometimes keep the same
                        pass
                    else:
                        chord = add_semitones(chord, -5)
                    if False:#TODO: setting? random() < 0.25:# sometimes add tension chords:
                        chord_progression.append(tension_chord_going_to(chord))
                    chord_progression.append(chord)
                scale_progression = chord_progression
        
        if attrs["_progression_random_tension"].gete():
            chord_progression, scale_progression = add_random_tension(chord_progression, scale_progression)

        
        if attrs["_scales"].gete():
            if not attrs["_chord_progression"].gete(): 
                music_desc += f"{app.tr("RANDOM_")}"
            music_desc += f"<font color='blue'>{app.tr("CHORDS_")}</font> {', '.join(chord_progression)}<br />"
            if attrs["_chord_progression2"].gete():
                music_desc += f"<font color='lightblue'>{app.tr("SCALES_")}</font> {', '.join(scale_progression)}<br />"
                

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
            
            music_desc += f"<font color='green'>{app.tr("MELODY_")}</font> {name_melody}"
            if attrs["_bass_tracks"].gete():
                music_desc += f", <font color='green'>{app.tr("BASS_")}</font> {name_bass}"
            music_desc += "<br />"
        else:
            s_drops = True
            
        #if random() < 0.3:
        #    instrument_bass = randrange(56, 79)
    
        OCTAVE = 3 # TODO: Get ovtace from instrument (use mingus?)
        beats = []
        #skip_random = 0.5#0.5 # 0 to 1
        #randomize = True
        #choices_duration_bass = [2,2,4,8]
        #choices_duration_melody = [0.5,0.5,1,2]
        #skip_over_silence = 0.5
        
        
        skip_random_bass = 0.8 if attrs["_test_jazz_scales"].gete() else 0.05
        skip_random_melody = 0.2 if attrs["_test_jazz_scales"].gete() else 0.1
        randomize = 0.2 if attrs["_less_random_test"].gete() else 1.0 # TODO: int
        # TODO: Flip sometimes?
        #choices_duration_bass = [2]# TODO: Should match. Go to my 8 years old code and start from that instead of doing nothing really useful here...
        #choices_duration_melody = [1]
        if attrs["_frequency"].gete():
            # TODO: I really need to have measures here, not random things, so that they MATCH (bass and melody)            
            # From least to most probable
            choices_duration_bass = [0.25, 3, 0.5, 1.5, 4, 1, 2, 2]
            
            choices_duration_melody = [4, 3, 0.25, 1.5, 2, 0.5, 1, 1]
            if attrs["_slower"].gete():
                choices_duration_melody.sort()
                choices_duration_melody.append(4)
            if attrs["_faster"].gete():
                choices_duration_melody.sort(reverse=True)
                choices_duration_melody.append(0.25)
        else:
            choices_duration_bass = [4]
            choices_duration_melody = [4]
            skip_random_bass = 0.0
            skip_random_melody = 0.0
        
        skip_over_silence = 0
        
        #for chord in chord_progression:
        #    beats.append(mid.Beat(duration=1, notes=[mid.Note(chords.from_shorthand(chord)[0], OCTAVE)]))
        if not s_drops and attrs["_bass_tracks"].gete():
            beats = add_progression(chord_progression, scale_progression, attrs, octave_start=OCTAVE, choices_duration=choices_duration_bass, skip_random=skip_random_bass, group_chord=True, skip_over_silence=skip_over_silence, randomize=randomize)
            channels.append(mid.Channel(beats=beats, instrument=instrument_bass)) 
        
        #beats = add_progression(chord_progression, attrs, octave_start=OCTAVE, choices_duration=choices_duration_bass, skip_random=skip_random_bass, group_chord=True, skip_over_silence=skip_over_silence)
        #channels.append(mid.Channel(beats=beats, instrument=instrument_bass2)) 
        
        #5 sometimes? needs to go higher sometimes?
        OCTAVE = 4
        beats = add_progression(chord_progression, scale_progression, attrs, scale=True, octave_start=OCTAVE, choices_duration=choices_duration_melody, skip_random=skip_random_melody, group_chord=False, randomize=randomize, skip_over_silence=skip_over_silence)
        if not s_drops:
            channels.append(mid.Channel(beats=beats, instrument=instrument_melody)) 
        else:
            switch_to_drops(channels, beats)
        
        #OCTAVE = 4
        #beats = add_progression(chord_progression, scale_progression, attrs, octave_start=OCTAVE, choices_duration=choices_duration_melody, skip_random=skip_random_melody, group_chord=False, randomize=randomize, skip_over_silence=skip_over_silence)
        #channels.append(mid.Channel(beats=beats, instrument=118, channel_id_override=9)) 
    
    
    
        
    mid.make_file(filename, channels, tempo=tempo)
    music_desc += f"{app.tr("TEMPO_")}<font color='red'>{tempo_str.title()}</font> ({tempo}{app.tr("TEMPO_BPM")})"
    logger.info(music_desc)
    return describe_music(app, attrs, music_desc), tempo