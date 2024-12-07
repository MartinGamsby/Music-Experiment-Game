import music.midi_helper as mid
from music import builder_rpt as rpt

import unittest

#------------------------------------------------------------------------------
class TestMidiHelper(unittest.TestCase):

    def test_rpt_progression(self):
        chord = "C"
        scale = "C"
        
        possibilities = [
            (["C","F","G7","C"],        ['C', 'C', 'C', 'C'],       ['R: I', 'P: IV', 'T: V7', 'R: I']),
            (["C","F","Bdim","C"],      ['C', 'C', 'C', 'C'],       ['R: I', 'P: IV', 'T: vii*', 'R: I']),
            (["C","Dmin","G7","C"],     ['C', 'C', 'C', 'C'],       ['R: I', 'P: ii', 'T: V7', 'R: I']),
            (["C","Dmin","Bdim","C"],   ['C', 'C', 'C', 'C'],       ['R: I', 'P: ii', 'T: vii*', 'R: I']),
                                                                                      
            (["C","F","G7","Amin"],        ['C', 'C', 'C', 'C'],    ['R: I', 'P: IV', 'T: V7', 'R: vi']),
            (["C","F","Bdim","Amin"],      ['C', 'C', 'C', 'C'],    ['R: I', 'P: IV', 'T: vii*', 'R: vi']),
            (["C","Dmin","G7","Amin"],     ['C', 'C', 'C', 'C'],    ['R: I', 'P: ii', 'T: V7', 'R: vi']),
            (["C","Dmin","Bdim","Amin"],   ['C', 'C', 'C', 'C'],    ['R: I', 'P: ii', 'T: vii*', 'R: vi']),
        ]
        
        for i in range(100):
            result = rpt.get_rpt_progression(chord, scale, 2) 
            
            self.assertIn((result.chord_progression, result.scale_progression, result.desc), possibilities)
            
        #self.assertEqual(rpt.get_rpt_progression("C", "C", 2), (["C","Dmin"], ['C', 'C', 'C', 'C']))
        #self.assertEqual(rpt.get_rpt_progression("C", "C", 7), (["C","Dmin", "G7", "C", "Dmin", "G7", "C"], ['C', 'C', 'C', 'C', 'C', 'C', 'C']))
        #self.assertEqual(rpt.get_rpt_progression("D", "D", 7), (["D","Emin", "A7", "D", "Emin", "A7", "D"], ['D', 'D', 'D', 'D', 'D', 'D', 'D']))
        

#------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()