from midiutil import MIDIFile
from dataclasses import dataclass
from typing import List

import logging
logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
# Help for midi: https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
NOTES_FROM_A = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)
SILENCE = ""

# Inspired from http://cfugue.sourceforge.net/docs/html/_tempo_8h_source.html
TEMPO = {
  "GRAVE": 40
, "LARGO": 45
, "LARGHETTO": 50
, "LENTO": 55
, "ADAGIO": 60
, "ADAGIETTO": 65

, "ANDANTE": 70
, "ANDANTINO": 80
, "MODERATO": 95
, "ALLEGRETTO": 110

, "ALLEGRO": 120
, "VIVACE": 145
, "PRESTO": 180
, "PRETISSIMO": 220 }
        
#------------------------------------------------------------------------------        
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

    if note == 'A##':
        return 'B'
    if note == 'B##':
        return 'C'
    if note == 'C##':
        return 'D'
    if note == 'D##':
        return 'E'
    if note == 'F##':
        return 'G'
    if note == 'G##':
        return 'A'
        
    return note

#------------------------------------------------------------------------------
@dataclass
class Note:
    note: str = SILENCE
    octave: int = 5
    velocity: int = 100 # 0-127
    
    #------------------------------------------------------------------------------
    @property
    def number(self):
        return Note._note_to_number(self.note, self.octave)
        
    #------------------------------------------------------------------------------
    @staticmethod
    def from_number(number):
        return Note._number_to_note(number)
        
    #------------------------------------------------------------------------------
    @staticmethod
    def _note_to_number(note: str, octave: int) -> int:
        note = swap_accidentals(note)
        if note is SILENCE:
            return 0
            
        if not note in NOTES:
            raise Exception(f"Bad input, note name {note} not recognized")
        if not octave in OCTAVES:
            raise Exception(f"Bad input, octave {octave} not in {OCTAVES}")

        number = NOTES.index(note)
        number += (NOTES_IN_OCTAVE * octave)

        if not 0 <= number <= 127:
            raise Exception(f"Bad input, note number {number} not in between 0 and 127")
        
        return number
        
    #------------------------------------------------------------------------------
    @staticmethod
    def _number_to_note(number: int):
    
        if not 0 <= number <= 127:
            raise Exception(f"Bad input, note number {number} not in between 0 and 127")
        
        octave = int(number / NOTES_IN_OCTAVE)
        pitch = number-9
        pitch -= (NOTES_IN_OCTAVE * octave)
        pitch = int(pitch)
        if pitch > len(NOTES_FROM_A):
            raise Exception(f"Bad input, pitch {pitch} not in {NOTES_FROM_A}")
        pitch = NOTES_FROM_A[int(pitch)]
    
        if not octave in OCTAVES:
            raise Exception(f"Bad input, octave {octave} not in {OCTAVES}")
        if not pitch in NOTES:
            raise Exception(f"Bad input, note name {note} not recognized")
    
        if pitch is SILENCE:
            return 0
        return Note(pitch, octave)

#------------------------------------------------------------------------------
@dataclass
class Beat:
    duration: int
    notes: List[Note]
    name: str = SILENCE
        
#------------------------------------------------------------------------------
@dataclass
class Channel:
    #name: str
    beats: List[Beat]
    volume: int = 100 # 0-127, as per the MIDI standard
    
    instrument: int = 0
    channel_id_override: int = -1
    
#------------------------------------------------------------------------------
def make_file(filename, channels, tempo):
    track = 0
    
    MyMIDI = MIDIFile(len(channels))
    MyMIDI.addTempo(track, 0, tempo)
    
    

    for channel_id, channel in enumerate(channels):
        if channel.channel_id_override >= 0:
            channel_id = channel.channel_id_override
        if channel.instrument > 0:
            MyMIDI.addProgramChange(0, channel_id, 0, channel.instrument)        
        time = 0
        for beat in channel.beats:
            for note in beat.notes:
                if note.note != SILENCE:
                    MyMIDI.addNote(track, channel_id, note.number, time, beat.duration, note.velocity)
                #TODO: change_note_tuning?
            logger.debug(f"{time}, {beat}")
            time += beat.duration
            
            
    with open(filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)

#------------------------------------------------------------------------------
def something():
    pass