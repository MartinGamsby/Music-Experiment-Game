import os
from helpers.file_helper import abspath

from PySide6.QtCore import QObject, QTranslator, QUrl

import logging
logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------        
class Translation(QObject):
    def __init__(self, app, language):
        super().__init__()
        
        self.app = app
        self.translatorEn = QTranslator(self)        
        self.translator1 = QTranslator(self)

        
        self.load(self.translatorEn, "t1_en")
        self.app.installTranslator(self.translatorEn)
         
        # TODO: allow override without locale, save, etc.
        self.selectLanguage(language)# like en_US
    
#------------------------------------------------------------------------------
    def load(self, translator, path):
        lang_path = abspath("lang")
        translator.load(path, lang_path)

#------------------------------------------------------------------------------
    def selectLanguage(self, hl):
        logger.info(f"Using language {hl}")
        self.app.removeTranslator(self.translator1)
        
        self.app.installTranslator(self.translatorEn)
        if hl.startswith("fr"):
            self.load(self.translator1, "t1_fr")
            self.app.installTranslator(self.translator1)
        
        