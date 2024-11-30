from helpers.setting import Setting
from helpers.steps import Steps

import unittest
import os

#------------------------------------------------------------------------------
class TestSetting(unittest.TestCase):

    def test_steps(self):
        steps = Steps()
        
        self.assertEqual(steps.get(0)["to"], 10)
        with self.assertRaises(KeyError) as context:
            steps.get(1)
            
        self.assertEqual(steps.to(0), 10)
        self.assertEqual(steps.to(10), 11)
        self.assertEqual(steps.to(20), 21)
            
        self.assertEqual(steps.get(10)["name"], "HEARING_DROPS")
        self.assertEqual(steps.name(10), "HEARING_DROPS")
        self.assertEqual(steps.name(1), "")
        
        self.assertEqual(steps.get(12)["unlocks"], ["ideas", "total_ideas", "frequency"])
        self.assertEqual(steps.unlocks(12), ["ideas", "total_ideas", "frequency"])
        self.assertEqual(steps.unlocks(1), [])
            
        self.assertEqual(steps.get(12)["adds"], {"total_ideas": 1})
        self.assertEqual(steps.adds(12), {"total_ideas": 1})
        self.assertEqual(steps.adds(1), {})
        
        self.assertEqual(steps.get(12)["seconds_to_next"], 14)
        self.assertEqual(steps.seconds_to_next(12), 14)
        self.assertEqual(steps.seconds_to_next(1), -1)
    
            

#------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()