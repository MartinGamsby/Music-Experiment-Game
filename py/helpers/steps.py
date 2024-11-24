import os
import yaml

import logging
logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------
class Steps:

    def __init__(self, filename="assets/steps.yaml"):
        super().__init__()       
        self.__load(filename)
        
#------------------------------------------------------------------------------
    def __load(self, filename):        
        with open(filename) as stream:
            try:
                self.__yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logging.exception("YAML load")

#------------------------------------------------------------------------------
    def get(self, id):
        return self.__yaml[id]
        
#------------------------------------------------------------------------------
    def __attrib(self, id, name, default):
        try:
            return self.__yaml[id][name]
        except Exception:
            return default(id)
        
#------------------------------------------------------------------------------
    def to(self, id):
        return self.__attrib(id, "to", lambda id: id+1)
            
#------------------------------------------------------------------------------
    def name(self, id):
        return self.__attrib(id, "name", lambda id: "")
        
#------------------------------------------------------------------------------
    def unlocks(self, id):
        return self.__attrib(id, "unlocks", lambda id: [])
        
#------------------------------------------------------------------------------
    def adds(self, id):
        return self.__attrib(id, "adds", lambda id: {})
        
#------------------------------------------------------------------------------
    def seconds_to_next(self, id):
        return self.__attrib(id, "seconds_to_next", lambda id: -1)
        
        