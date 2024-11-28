from helpers.steps import Steps
from model import Model

import unittest
import os

#------------------------------------------------------------------------------
class TestSetting(unittest.TestCase):

    def test_steps(self):
        model = Model(app=None)
        steps = model._steps
                
        self.assertEqual(steps.to(0), 10)
        
        all_steps = steps._all()
        keys = all_steps.keys()
        
        last = list(keys)[-1]
        for s in all_steps:
            if s != last:
                #print(f"{s} to {steps.to(s)}")
                self.assertIn(steps.to(s), keys)
                
            for u in steps.unlocks(s):
                #print(f"{s} unlocks {u}:")
                self.assertNotEqual(None, getattr(model, f"_{u}"))
                
            adds =  steps.adds(s)
            for a in adds:
                #print(f"{s} adds {a} += {adds[a]}:")
                attr = getattr(model, f"_{a}")
                self.assertNotEqual(None, attr)
                #print(f" -> type {type(adds[a])} in {attr._type}")
                self.assertEqual(type(adds[a]), attr._type)
            
            seconds_to_next = steps.seconds_to_next(s)
            self.assertEqual(type(seconds_to_next), int)
            
            self.assertGreaterEqual(seconds_to_next, -1) # TODO: Greater than last?
            
#------------------------------------------------------------------------------
    def test_fake_steps(self):
        model = Model(app=None)
        steps = Steps("assets/test/steps.yaml")
        self.assertEqual(steps.get(0)["unlocks"], ["typo", "notInModel"])
        
        s = 0
        for u in steps.unlocks(s):
            #print(f"{s} DOESN'T unlock {u}:")
            with self.assertRaises(AttributeError) as context:
                self.assertEqual(None, getattr(model, f"_{u}"))    

        adds =  steps.adds(s)
        for a in adds:
            #print(f"{s} adds {a} += {adds[a]}:")
            attr = getattr(model, f"_{a}")
            self.assertNotEqual(None, attr)
            #print(f" -> DIFFERENT type {type(adds[a])} in {attr._type}")            
            self.assertNotEqual(type(adds[a]), attr._type)
            
        seconds_to_next = steps.seconds_to_next(s)
        self.assertLess(seconds_to_next, -1)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()