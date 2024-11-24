from PySide6.QtCore import QObject, Property, Signal, Slot
        
from PySide6.QtQml import QmlElement
        
import logging
logger = logging.getLogger(__name__)


QML_IMPORT_NAME = "com.martingamsby.music"
QML_IMPORT_MAJOR_VERSION = 1

#------------------------------------------------------------------------------
@QmlElement
class Setting(QObject):
    name_updated = Signal()
    value_updated = Signal()
    unlocked_updated = Signal()
    
#------------------------------------------------------------------------------
    def __init__(self, default_value, fullname="", save=None, save_progress=None, 
            sub_unlock=True, auto_unlock=False):
        
        super().__init__()
                
        try:
            slash_index = fullname.index("/")
            self._section = fullname[:slash_index]
            self._name = fullname[slash_index+1:]
        except:
            self._name = fullname
            self._section = "Default"
        
        self._default_value = default_value
        self._value = default_value
        self._type = type(self._value)
        self._notify_sig = None
        self._save = save
        self._save_progress = save_progress
        if save_progress == None and save is not None:
            self._save_progress = save
            
        if self._save:
            self._save.model_changed.connect(self.model_changed)
        
        
        self._initialized = False
        
        # TODO: different save?
        if sub_unlock:
            self._unlocked = Setting(auto_unlock, f"Unlocked/{self._name}", save=self._save_progress, sub_unlock=False)
        else:
            self._unlocked = None
    
#------------------------------------------------------------------------------
    @staticmethod
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")
        
#------------------------------------------------------------------------------
    def init(self):
        if self._save:
            val = self._save.load(self._name, section=self._section)
            logger.debug(f"Get {self._name} == {val} ({self._value})")
            if val is not None:
                if self._type == str:
                    pass # val = val
                elif self._type == bool:
                    val = self.str2bool(val)
                elif self._type == float:
                    val = float(val)
                elif self._type == int:
                    val = int(val)
                else:
                    raise Exception("TO IMPLEMENT {self._type}")
                
                self._value = val
        self._initialized = True
        
#------------------------------------------------------------------------------
    @Slot()
    def model_changed(self):
        self._value = self._default_value
        if self._unlocked:
            self._unlocked.model_changed()
        
#------------------------------------------------------------------------------
    def get(self):
        if not self._initialized: # TODO: Better than that? (It's weird because of the Property of Qt...)
            self.init()
        logger.debug(f"{self._name} == {self._value}")
        return self._value
        
#------------------------------------------------------------------------------
    def set(self, value):
        logger.debug(f"{self._name} set to: \"{value}\"")
        if type(value) != self._type:
            raise Exception(f"Wrong type for {self._name}: {type(value)} ({value}) is not {self._type} ({self._value})")
        try:
            if self._value != value:
                self._value = value
                self.value_updated.emit()
                try:
                    if self._save:
                        self._save.save(self._name, self._value, section=self._section)
                        
                except:
                    logging.exception("save val")
        except (AttributeError, TypeError) as e:
            # Handle potential exceptions during attribute access or type mismatch
            logger.error(f"Error setting property '{value}': {e}")
            
#------------------------------------------------------------------------------
    def add(self, add_value):
        self.set(self.get()+add_value)
            
#------------------------------------------------------------------------------
    def unlocked(self):
        if not self._unlocked:
            raise Exception("Not unlockable")
        return self._unlocked.get()
        
#------------------------------------------------------------------------------
    #@Slot()
    def unlock(self):
        if not self._unlocked:
            raise Exception("Not unlockable")
            
        if not self._unlocked.get():
            self._unlocked.set(True)
            self.unlocked_updated.emit()
        
#------------------------------------------------------------------------------
    def lock(self):
        if not self._unlocked:
            raise Exception("Not lockable")
        if self._unlocked.get():
            self._unlocked.set(False)
            self.unlocked_updated.emit()
            
#------------------------------------------------------------------------------
    def name(self):
        if not self._unlocked:
            raise Exception("Not unlockable")
        return self._name
        
        
#------------------------------------------------------------------------------
    s = Property(str, get, set, notify=value_updated)
    b = Property(bool, get, set, notify=value_updated)
    f = Property(float, get, set, notify=value_updated)
    i = Property(int, get, set, notify=value_updated)
    
    p_name = Property(str, name, notify=name_updated)
    p_unlocked = Property(int, unlocked, notify=unlocked_updated)
    