from helpers.save import Save

import unittest
import os

#------------------------------------------------------------------------------
class TestSave(unittest.TestCase):

    def test_save(self):
        save_filename = "test.sav"
        if os.path.isfile(save_filename):
            os.remove(save_filename)

        save = Save()
        with self.assertRaises(Exception) as context:
            save.write_config()
        self.assertIn('Cannot save unitialized save', str(context.exception))
        
        with self.assertRaises(Exception) as context:
            save.save("name", "value")
        self.assertIn('Cannot save value to unitialized save', str(context.exception))
        
        with self.assertRaises(Exception) as context:
            save.load("name")
        self.assertIn('Cannot load value of unitialized save', str(context.exception))
        
        save.init(save_filename)
        
        self.assertEqual(None, save.load("anything"))
        
        save.save("one", 1)
        self.assertEqual('1', save.load("one"))
        save.save("two", 2)
        self.assertEqual('2', save.load("two"))
        
        os.remove(save_filename)
        

#------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()