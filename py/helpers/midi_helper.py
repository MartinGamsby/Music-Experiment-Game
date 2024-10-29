from midiutil import MIDIFile
from mingus.core import chords
from dataclasses import dataclass
from typing import List

NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

errors = {
    'notes': 'Bad input, please refer this spec-\n'
}
        
        
def swap_accidentals(note):
    if note == 'Db':
        return 'C#'
    if note == 'D#':
        return 'Eb'
    if note == 'E#':
        return 'F'
    if note == 'Gb':
        return 'F#'
    if note == 'G#':
        return 'Ab'
    if note == 'A#':
        return 'Bb'
    if note == 'B#':
        return 'C'

    return note


def note_to_number(note: str, octave: int) -> int:
    note = swap_accidentals(note)
    assert note in NOTES, errors['notes']
    assert octave in OCTAVES, errors['notes']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, errors['notes']

    return note

@dataclass
class Note:
    note: str
    octave: int
    duration: int #TODO:(find better name)
    
    @property
    def number(self):
        return note_to_number(self.note, self.octave)
    
@dataclass
class Channel:
    #name: str
    array_of_note_numbers: List[Note]
    volume: int = 100 # 0-127, as per the MIDI standard
        
        
def make_file(filename, channels, tempo):
    track = 0
    
    MyMIDI = MIDIFile(len(channels))
    # automatically)
    MyMIDI.addTempo(track, 0, tempo)

    for channel_id, channel in enumerate(channels):
        time = 0
        for note in channel.array_of_note_numbers:
            print(note)
            MyMIDI.addNote(track, channel_id, note.number, time, note.duration, channel.volume)
            time += note.duration
            
    with open(filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)