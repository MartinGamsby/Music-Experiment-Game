import os
from helpers.file_helper import abspath

from PySide6.QtCore import QObject, QTranslator, QLocale, QUrl

#------------------------------------------------------------------------------        
class Translation(QObject):
    def __init__(self, app):
        super().__init__()
        
        self.app = app
        self.translatorEn = QTranslator(self)        
        self.translator1 = QTranslator(self)

        
        self.load(self.translatorEn, "t1_en")
        self.app.installTranslator(self.translatorEn)
         
        # TODO: allow override without locale, save, etc.
        self.selectLanguage(QLocale().name())# like en_US
    
#------------------------------------------------------------------------------
    def load(self, translator, path):
        lang_path = abspath("lang")
        translator.load(path, lang_path)

#------------------------------------------------------------------------------
    def selectLanguage(self, hl):
        print(hl)
        self.app.removeTranslator(self.translator1)
        
        self.app.installTranslator(self.translatorEn)
        if hl.startswith("fr"):
            self.load(self.translator1, "t1_fr")
            self.app.installTranslator(self.translator1)
        
        