from PySide6.QtCore import QObject, QTranslator, QLocale

#------------------------------------------------------------------------------        
class Translation(QObject):
    def __init__(self, app):
        super().__init__()
        
        self.app = app
        self.translatorEn = QTranslator(self)        
        self.translator1 = QTranslator(self)

        
        self.translatorEn.load("t1_en", "lang")
        self.app.installTranslator(self.translatorEn)
         
        # TODO: allow override without locale, save, etc.
        self.selectLanguage(QLocale().name())# like en_US
    
#------------------------------------------------------------------------------
    def selectLanguage(self, hl):
        print(hl)
        if hl.startswith("fr"):
            self.translator1.load("t1_fr", "lang")
            self.app.installTranslator(self.translator1)
        