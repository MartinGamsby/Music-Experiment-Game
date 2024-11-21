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
if __name__ == "__main__":
    unittest.main()