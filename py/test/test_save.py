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
        save.save("two", 2)
        self.assertEqual('1', save.load("one"))
        self.assertEqual('2', save.load("two"))
        
        
        # 2nd object (not only stored in memory, but on file too)
        save2 = Save()
        save2.init(save_filename)
        self.assertEqual('1', save2.load("one"))
        self.assertEqual('2', save2.load("two"))
        
        # 3rd object after deleting the file
        save2.reset() # equivalent of os.remove(save_filename)++
        
        
        self.assertEqual(None, save2.load("one"))
        self.assertEqual(None, save2.load("two"))
        
        save3 = Save()
        save3.init(save_filename)
        self.assertEqual(None, save3.load("one"))
        self.assertEqual(None, save3.load("two"))
        

#------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()