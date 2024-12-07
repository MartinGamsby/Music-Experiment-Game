import os
import logging
logger = logging.getLogger(__name__)

import configparser

from PySide6.QtCore import QObject, Signal


ALWAYS_SAVE = True # TODO: Do I want to always save?

#------------------------------------------------------------------------------
class Save(QObject):
    model_changed = Signal()

    def __init__(self):
        super().__init__()
        self._initialized = False
        
#------------------------------------------------------------------------------
    def init(self, filename):
        if self._initialized:
            logger.error("Cannot initialize twice")
            return
        logger.debug("Initializing save")
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.__load_config()
        self._initialized = True
        
#------------------------------------------------------------------------------
    def __load_config(self):
        logger.info(f"Loading save {self.filename}")
        self.config.read(self.filename)
        
#------------------------------------------------------------------------------
    def write_config(self):
        if not self._initialized:
            raise Exception("Cannot save unitialized save")
        logger.debug(f"Saving save {self.filename}")
        with open(self.filename, 'w') as configfile:
            #uh ... mutex?
            self.config.write(configfile)
          
#------------------------------------------------------------------------------
    def reset(self):
        if not self._initialized:
            raise Exception("Cannot reset unitialized save")
        logger.info(f"Resetting save {os.path.basename(self.filename)}")
        if os.path.isfile(self.filename):
            os.remove(self.filename)
            
        self.config = configparser.ConfigParser()
        self.model_changed.emit()
            
#------------------------------------------------------------------------------
    def save(self, name, value, section="Default"):
        if not self._initialized:
            raise Exception("Cannot save value to unitialized save")
        
        logger.debug(f"Setting {section}/{name} = {value}")
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        self.config.set(section, name, str(value))
        if ALWAYS_SAVE:
            self.write_config()
        
#------------------------------------------------------------------------------
    def load(self, name, section="Default"):
        if not self._initialized:
            raise Exception("Cannot load value of unitialized save")
        if not self.config.has_option(section, name):
            return None
        return self.config.get(section, name, raw=True)