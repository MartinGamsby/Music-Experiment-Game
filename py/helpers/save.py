import logging
logger = logging.getLogger(__name__)

import configparser


ALWAYS_SAVE = True # TODO: Do I want to always save?

#------------------------------------------------------------------------------
class Save:
    def __init__(self):
        super().__init__()
        self._initialized = False
        
#------------------------------------------------------------------------------
    def init(self, filename):
        if self._initialized:
            logger.critical("Cannot intitialize twice")
            return
        logger.info("Initializing save")
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.load_config()
        self._initialized = True
        
#------------------------------------------------------------------------------
    def load_config(self):
        logger.info(f"Loading save {self.filename}")
        self.config.read(self.filename)
        
#------------------------------------------------------------------------------
    def write_config(self):
        if not self._initialized:
            logger.critical("Cannot saved unitialized save")
            return
        logger.info(f"Saving save {self.filename}")
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
          
#------------------------------------------------------------------------------
    def save(self, name, value, section="Default"):
        if not self._initialized:
            logger.critical("Cannot set value to unitialized save")
            return
        
        logger.debug(f"Setting {section}/{name} = {value}")
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        self.config.set(section, name, str(value))
        #uh ... mutex?
        if ALWAYS_SAVE:
            self.write_config()
        
#------------------------------------------------------------------------------
    def load(self, name, section="Default"):
        if not self.config.has_option(section, name):
            return None
        return self.config.get(section, name, raw=True)