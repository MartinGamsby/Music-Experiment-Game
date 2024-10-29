import helpers.midi_helper as mid
from mingus.core import chords


def add_chord_progression(chord_progression, duration=4):    
    notes = []
    for chord in chord_progression:
        sub_notes = chords.from_shorthand(chord)
        
        if len(sub_notes) == 0:
            raise Exception("No notes in chord progression!")
        if len(sub_notes) > duration:
            sub_notes = sub_notes[:duration]
        if len(sub_notes) < duration:
            i = 0
            to = duration-len(sub_notes)
            
            for idx in range(i,to):
                sub_notes.append(sub_notes[idx])# TODO: one more octave??
        notes.extend(sub_notes)
    return notes

def make_midi(filename):

    chord_progression = ["Cmaj", "Fmaj", "Cmaj", "Cmaj7", "Fmaj", "Gmaj", "Cmaj"]
    
    channels = []


    
    
    notes = add_chord_progression(chord_progression)        

    array_of_note_numbers = []
    for note in notes:
        OCTAVE = 4
        array_of_note_numbers.append(mid.Note(note, OCTAVE, duration=1))
    channels.append(mid.Channel(array_of_note_numbers=array_of_note_numbers)) 
    
    
    
    
    
    notes = []
    for chord in chord_progression:
        notes.append(chords.from_shorthand(chord)[0])

    array_of_note_numbers = []
    for note in notes:
        OCTAVE = 3
        array_of_note_numbers.append(mid.Note(note, OCTAVE, duration=4))
    channels.append(mid.Channel(array_of_note_numbers=array_of_note_numbers)) 

    
    
        
    mid.make_file(filename, channels, tempo=120)