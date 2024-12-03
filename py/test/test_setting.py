from helpers.setting import Setting
from helpers.save import Save

import unittest
import os

#------------------------------------------------------------------------------
class TestSetting(unittest.TestCase):

    def test_setting(self):
        setting_bool = Setting(True, "bool1", save=None)
        self.assertEqual(True, setting_bool.get())
        setting_bool.set(False)
        with self.assertRaises(Exception) as context:
            setting_bool.set(1)
        self.assertIn('Wrong type', str(context.exception))
        self.assertEqual(False, setting_bool.get())
        
        setting_float = Setting(1.2, "float1", save=None)
        self.assertEqual(1.2, setting_float.get())
        setting_float.set(-3.)
        with self.assertRaises(Exception) as context:
            setting_float.set("string")
        self.assertIn('Wrong type', str(context.exception))
        self.assertEqual(-3., setting_float.get())
        
        setting_str = Setting("val", "str1", save=None)
        self.assertEqual("val", setting_str.get())
        setting_str.set("val2")
        with self.assertRaises(Exception) as context:
            setting_str.set(13)
        self.assertIn('Wrong type', str(context.exception))
        self.assertEqual("val2", setting_str.get())
        
        setting_int = Setting(-1, "int1", save=None)
        self.assertEqual(-1, setting_int.get())
        setting_int.set(4)
        with self.assertRaises(Exception) as context:
            setting_int.set(False)
        self.assertIn('Wrong type', str(context.exception))
        self.assertEqual(4, setting_int.get())
        
#------------------------------------------------------------------------------
    def test_locked(self):
        setting_int = Setting(1, "int2", save=None)
        self.assertEqual(False, setting_int.unlocked())
        
        setting_int.unlock()
        self.assertEqual(True, setting_int.unlocked())
        
        setting_int.lock()
        self.assertEqual(False, setting_int.unlocked())
        
#------------------------------------------------------------------------------
    def test_unlockeable(self):
        setting_int1 = Setting(1, "int1", save=None)
        setting_int2 = Setting(2, "int2", save=None, dependencies=[setting_int1])
        setting_int3 = Setting(3, "int3", save=None, dependencies=[setting_int2])
        
        setting_int1.set(10)
        setting_int2.set(20)
        setting_int3.set(30)
        
        # wrong, but test .gete(), and unlocked and enabled all the way down
        self.assertEqual(False, setting_int1.unlocked())
        self.assertEqual(False, setting_int2.unlocked())
        self.assertEqual(False, setting_int3.unlocked())
        self.assertEqual(10, setting_int1.get())
        self.assertEqual(20, setting_int2.get())
        self.assertEqual(30, setting_int3.get())
        self.assertEqual(10, setting_int1.gete())
        self.assertEqual(20, setting_int2.gete())
        self.assertEqual(30, setting_int3.gete())
        
        setting_int3.unlock()
        
        self.assertEqual(False, setting_int1.unlocked())
        self.assertEqual(False, setting_int2.unlocked())
        self.assertEqual(False, setting_int3.unlocked())
        self.assertEqual(10, setting_int1.get())
        self.assertEqual(20, setting_int2.get())
        self.assertEqual(30, setting_int3.get())
        self.assertEqual(10, setting_int1.gete())
        self.assertEqual(20, setting_int2.gete())
        self.assertEqual(30, setting_int3.gete())
        
        setting_int2.unlock()
        
        self.assertEqual(False, setting_int1.unlocked())
        self.assertEqual(False, setting_int2.unlocked())
        self.assertEqual(False, setting_int3.unlocked())
        self.assertEqual(10, setting_int1.get())
        self.assertEqual(20, setting_int2.get())
        self.assertEqual(30, setting_int3.get())
        self.assertEqual(10, setting_int1.gete())
        self.assertEqual(20, setting_int2.gete())
        self.assertEqual(30, setting_int3.gete())
        
        setting_int1.unlock()
        
        self.assertEqual(True, setting_int1.unlocked())
        self.assertEqual(True, setting_int2.unlocked())
        self.assertEqual(True, setting_int3.unlocked())
        self.assertEqual(10, setting_int1.get())
        self.assertEqual(20, setting_int2.get())
        self.assertEqual(30, setting_int3.get())
        self.assertEqual(10, setting_int1.gete())
        self.assertEqual(20, setting_int2.gete())
        self.assertEqual(30, setting_int3.gete())
        
        # Same for enabled:
        self.assertEqual(True, setting_int1.enabled())
        self.assertEqual(True, setting_int2.enabled())
        self.assertEqual(True, setting_int3.enabled())
        self.assertEqual(10, setting_int1.get())
        self.assertEqual(20, setting_int2.get())
        self.assertEqual(30, setting_int3.get())
        self.assertEqual(10, setting_int1.gete())
        self.assertEqual(20, setting_int2.gete())
        self.assertEqual(30, setting_int3.gete())
                
        setting_int1.setEnabled(False)
        
        self.assertEqual(False, setting_int1.enabled())
        self.assertEqual(False, setting_int2.enabled())
        self.assertEqual(False, setting_int3.enabled())
        self.assertEqual(10, setting_int1.get())
        self.assertEqual(20, setting_int2.get())
        self.assertEqual(30, setting_int3.get())
        self.assertEqual(1, setting_int1.gete())
        self.assertEqual(2, setting_int2.gete())
        self.assertEqual(3, setting_int3.gete())
                
        setting_int1.setEnabled(True)
        setting_int2.setEnabled(False)
        
        self.assertEqual(True, setting_int1.enabled())
        self.assertEqual(False, setting_int2.enabled())
        self.assertEqual(False, setting_int3.enabled())
        self.assertEqual(10, setting_int1.get())
        self.assertEqual(20, setting_int2.get())
        self.assertEqual(30, setting_int3.get())
        self.assertEqual(10, setting_int1.gete())
        self.assertEqual(2, setting_int2.gete())
        self.assertEqual(3, setting_int3.gete())
                
        setting_int2.setEnabled(True)
        setting_int3.setEnabled(False)
        
        self.assertEqual(True, setting_int1.enabled())
        self.assertEqual(True, setting_int2.enabled())
        self.assertEqual(False, setting_int3.enabled())
        self.assertEqual(10, setting_int1.get())
        self.assertEqual(20, setting_int2.get())
        self.assertEqual(30, setting_int3.get())
        self.assertEqual(10, setting_int1.gete())
        self.assertEqual(20, setting_int2.gete())
        self.assertEqual(3, setting_int3.gete())
            
#------------------------------------------------------------------------------
    def test_gete(self):
        setting_int = Setting(1, "int2", save=None)
        self.assertEqual(False, setting_int.unlocked())
        
        setting_int.unlock()
        self.assertEqual(True, setting_int.unlocked())
        
        setting_int.lock()
        self.assertEqual(False, setting_int.unlocked())
        
#------------------------------------------------------------------------------
    # TODO: save_progress
    
    
#------------------------------------------------------------------------------
    def test_locked_permanent(self):
        # TODO: Test if permanent
        save_filename = "ut.sav"
        if os.path.isfile(save_filename):
            os.remove(save_filename)
        
        save = Save()
        save.init(save_filename)      
        
        setting_int = Setting(1, "int2", save=save)
        self.assertEqual(False, setting_int.unlocked())
        
        setting_int.unlock()
        self.assertEqual(True, setting_int.unlocked())
        
        #2nd item, read from disk (unlocked)
        save2 = Save()
        save2.init(save_filename)
        
        setting_int2 = Setting(1, "int2", save=save2)
        self.assertEqual(True, setting_int2.unlocked())
        
        # 3rd item, not reading from file
        os.remove(save_filename)
        save3 = Save()
        save3.init(save_filename)
        
        setting_int3 = Setting(1, "int2", save=save3)
        self.assertEqual(False, setting_int3.unlocked())
        
        

#------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()