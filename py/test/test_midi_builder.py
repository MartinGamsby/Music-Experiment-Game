import music.midi_helper as mid
from music import midi_builder as mb

import unittest

#------------------------------------------------------------------------------
class TestMidiHelper(unittest.TestCase):

    def test_mingus_chord_I_guess(self):
        #well ... using mingus... not super useful...
        from mingus.core import chords
        self.assertEqual(["C", "E", "G"], chords.from_shorthand("C"))
        self.assertEqual(["C", "E", "G", "Bb"], chords.from_shorthand("C7"))
        
#------------------------------------------------------------------------------
    def test_add_semitones(self):
        self.assertEqual(mb.add_semitones("C", 5), "F")
        
#------------------------------------------------------------------------------
    def test_transition_chord(self):
        with self.assertRaises(Exception) as context:
            mb.tension_chord_going_to(1)
        
        self.assertEqual(mb.tension_chord_going_to("F"), "C7")
        self.assertEqual(mb.tension_chord_going_to("A#"), "F7")
        self.assertEqual(mb.tension_chord_going_to("D#"), "Bb7")#A#7")
        self.assertEqual(mb.tension_chord_going_to("G#"), "Eb7")#D#7")
        self.assertEqual(mb.tension_chord_going_to("C#"), "Ab7")#G#7")
        self.assertEqual(mb.tension_chord_going_to("F#"), "C#7")
        self.assertEqual(mb.tension_chord_going_to("B"), "F#7")
        self.assertEqual(mb.tension_chord_going_to("E"), "B7")
        self.assertEqual(mb.tension_chord_going_to("A"), "E7")
        self.assertEqual(mb.tension_chord_going_to("D"), "A7")
        self.assertEqual(mb.tension_chord_going_to("G"), "D7")
        self.assertEqual(mb.tension_chord_going_to("C"), "G7")
        
        #self.assertEqual(mb.tension_chord_going_to("Fmin"), "??")
        
        
#------------------------------------------------------------------------------
    def test_jazz_scale(self):
        self.assertEqual(mb.jazz_scale("C"), ['C', 'D', 'Eb', 'E', 'G', 'A'])

#------------------------------------------------------------------------------
    def test_transition_chord(self):
    
        from mingus.core import chords
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("A")), ["D","E","A"])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("A7")), ["D"])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Am")), ["C","F","G"])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Am7")), ["C","F","G"])
        
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Bb")), ['Eb', 'F', 'Bb'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Bb7")), ['Eb'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Bbm")), ['Ab'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Bbm7")), ['Ab'])
        
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("B")), ["E","F#","B"])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("B7")), ["E"])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Bm")), ['D', 'G', 'A'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Bm7")), ['D', 'G', 'A'])
        
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("C")), ['C', 'F', 'G'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("C7")), ['F'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Cm")), ['Eb', 'Ab', 'Bb'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Cm7")), ['Eb', 'Ab', 'Bb'])
        
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("C#")), ['C#', 'F#'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("C#7")), ['F#'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("C#m")), ['E', 'A', 'B'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("C#m7")), ['E', 'A', 'B'])
        
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("D")), ['D', 'G', 'A'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Dm")), ['C', 'F', 'Bb'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Eb")), ['Eb', 'Ab', 'Bb'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Ebm")), [])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("E")), ['E', 'A', 'B'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Em")), ['C', 'D', 'G'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("F")), ['C', 'F', 'Bb'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("F7")), ['Bb'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Fm")), ['Eb', 'Ab'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("F#")), ['C#', 'F#', 'B'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("F#m")), ['D', 'E', 'A'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("G")), ['C', 'D', 'G'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("G7")), ['C'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Gm")), ['Eb', 'F', 'Bb'])        
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Ab")), ['Eb', 'Ab'])
        self.assertEqual(mb.scales_with_notes(chords.from_shorthand("Abm")), [])
        
        

#------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()