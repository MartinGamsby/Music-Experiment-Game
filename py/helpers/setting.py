from PySide6.QtCore import QObject, Property, Signal
        
from PySide6.QtQml import QmlElement
        
import logging
logger = logging.getLogger(__name__)


QML_IMPORT_NAME = "com.martingamsby.music"
QML_IMPORT_MAJOR_VERSION = 1

#------------------------------------------------------------------------------
@QmlElement
class Setting(QObject):
    value_updated = Signal()
    
#------------------------------------------------------------------------------
    def __init__(self, default_value, fullname="", save=None):#, type, name):
        super().__init__()
        
        try:
            slash_index = fullname.index("/")
            self._section = fullname[:slash_index]
            self._name = fullname[slash_index+1:]
        except:
            self._name = fullname
            self._section = "Default"
        
        self._value = default_value
        self._type = type(self._value)
        self._notify_sig = None
        self._save = save
        
        self._initialized = False
    
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
                else:
                    assert False, f"TO IMPLEMENT {self._type}"
                
                self._value = val
        self._initialized = True
        
#------------------------------------------------------------------------------
    def get(self):
        if not self._initialized: # TODO: Better than that? (It's weird because of the Property of Qt...)
            self.init()
        logger.debug(f"{self._name} == {self._value}")
        return self._value
        
#------------------------------------------------------------------------------
    def set(self, value):
        logger.debug(f"{self._name} set to: \"{value}\"")
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
    s = Property(str, get, set, notify=value_updated)
    b = Property(bool, get, set, notify=value_updated)
    f = Property(float, get, set, notify=value_updated)
    