import helpers.midi_helper as mid
from mingus.core import chords

#------------------------------------------------------------------------------
def add_chord_progression(chord_progression, measure_duration=4, note_duration=1, octave_start=4, group_chord=False):    
    beats = []
    for chord in chord_progression:
        sub_notes = chords.from_shorthand(chord)
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
        #print(sub_notes)
        
        sub_beats = []
        last_note = 0
        for name in sub_notes:
            note = mid.Note(note=name, octave=octave)
            
            notes = [note]#Only one note
            if last_note > note.number:
                octave += 1
                note.octave = octave
            #print(note.number)
            beat = mid.Beat(duration=note_duration, notes=notes, name=chord)
            sub_beats.append(beat)
        
            last_note = note.number
            
        if group_chord:
        
            beat_notes = []
            for beat in sub_beats:
                assert len(beat.notes) == 1
                beat_notes.append(beat.notes[0])
            common_beat = mid.Beat(note_duration, beat_notes, name=chord)
            beats.append(common_beat)
        else:
            beats.extend(sub_beats)
            
        #notes.extend(sub_notes)
    return beats
    
#------------------------------------------------------------------------------
def make_midi(filename):

    chord_progression = ["Cmaj", "Fmaj", "Cmaj", "Cmaj7", "Fmaj", "Gmin", "Dmaj7", "Fmaj", "Cmaj"]
    
    channels = []


    
    # TODO: Notes with the octave. Return Note() here, and make sure we go up if we go over G.
    beats = add_chord_progression(chord_progression, octave_start=8, note_duration=3)
    channels.append(mid.Channel(beats=beats, instrument=115)) 
    beats = add_chord_progression(chord_progression, octave_start=8, note_duration=3)
    beats.insert(0,mid.Beat(duration=0.25, notes=[mid.Note("C", octave=1)]))
    channels.append(mid.Channel(beats=beats, instrument=113)) 
    
    
    ##chord_progression = ["Cmaj", "Cmaj", "Fmaj", "Fmaj", "Cmaj", "Cmaj", "Cmaj7", "Cmaj7", "Fmaj", "Fmaj", "Gmin", "Gmin", "Dmaj7", "Dmaj7", "Fmaj", "Fmaj", "Cmaj", "Cmaj"] 
    #chord_progression = ["Cmaj", "Cmaj", "Fmaj", "Fmaj", "Gmaj7", "Gmaj7", "Cmaj7", "Cmaj7", "Cmaj7", "Cmaj7", "Fmaj", "Fmaj", "Fmin", "Fmin", "Cmaj", "Cmaj"]
    #beats = add_chord_progression(chord_progression, octave_start=6, group_chord=True, note_duration=1*2)
    #channels.append(mid.Channel(beats=beats)) 
    #
    #beats = add_chord_progression(chord_progression, octave_start=8, group_chord=True, note_duration=1*2)
    #beats.insert(0,mid.Beat(duration=0.5, notes=[mid.Note("C", octave=1)]))
    #channels.append(mid.Channel(beats=beats)) 
    
    
    
    
    #OCTAVE = 3
    #beats = []
    #for chord in chord_progression:
    #    beats.append(mid.Beat(duration=1, notes=[mid.Note(chords.from_shorthand(chord)[0], OCTAVE)]))
    #channels.append(mid.Channel(beats=beats)) 

    
    
        
    mid.make_file(filename, channels, tempo=240)