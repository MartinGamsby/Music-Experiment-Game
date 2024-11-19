import music.midi_helper as mid

import unittest

#------------------------------------------------------------------------------
class TestMidiHelper(unittest.TestCase):

    def test_notes(self):
        for octave in range(10):
            note = mid.Note(note="A", octave=octave)
            self.assertEqual(note.number, 9+12*octave)
            
        note = mid.Note(note="A", octave=-1)
        with self.assertRaises(Exception) as context:
            note.number
        self.assertIn('octave -1 not in', str(context.exception))

#------------------------------------------------------------------------------
    def test_from_number(self):
        note = mid.Note(note="A", octave=2)
        self.assertEqual(note.number, 33)
        for i in range(0,128):
            note2 = mid.Note.from_number(i)
            self.assertEqual(note2.number, i)
        
        with self.assertRaises(Exception) as context:
            note3 = mid.Note.from_number(-1)
        self.assertIn('Bad input, note number -1 not in between 0 and 127', str(context.exception))

        with self.assertRaises(Exception) as context:
            note4 = mid.Note.from_number(128)
        self.assertIn('Bad input, note number 128 not in between 0 and 127', str(context.exception))
        
        

#------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()