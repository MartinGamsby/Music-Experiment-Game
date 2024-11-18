import sys
import os
import pathlib
#import flagpy
from helpers.file_helper import abspath
from helpers.setting import Setting
from time import sleep, time
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, Property, QStandardPaths, QUrl

import model
import state
import midi_builder

import helpers.translator as translator

import logging
logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
class Backend(QObject):
    
    def __init__(self, qml_file, app, model: model.Model):
        super().__init__()

        self.model = model
        self.translator = translator.Translation(app, self.model._language.s)
        
        self.app = app
        
        state.register_for_qml(self.app)
                
        self.engine = QQmlApplicationEngine()
        self.engine.load(os.path.join(pathlib.Path(__file__).parent.resolve(), "ui", qml_file))
        
        self.engine.quit.connect(self.app.quit)
         

        # Pass self and add accessors instead?
        self.engine.rootObjects()[0].setProperty("model", self.model)
        self.engine.rootObjects()[0].setProperty("backend", self)
        
        self.engine.rootObjects()[0].setIcon(QIcon(":/logo"))
        
        # After we set the model to the qml
        retval = self.model.init()
    
#------------------------------------------------------------------------------
    @Slot(str)
    def play_mid_pressed(self, value: str):
        logger.info(f"PLAY MID PRESSED: {value}")
        value = abspath(value)
        if value:
            self.model.play_async(value, type=midi_builder.MusicBuildType.FILE)
        else:
            self.model.play_async(value, type=midi_builder.MusicBuildType.DROPS)
        
#------------------------------------------------------------------------------
    @Slot(bool)
    def toMainMenu(self, play: bool):
        logger.info(f"TO MAIN MENU")
        if play:
            self.model.play_main_menu()
        self.model.set_state(state.State.MAIN_MENU)
        
#------------------------------------------------------------------------------
    @Slot(None)
    def playMidis(self):
        logger.info(f"PLAY MIDIS")
        self.model.set_state(state.State.PLAY_MIDIS)
        
#------------------------------------------------------------------------------
    @Slot(None)
    def newGame(self):
        logger.info(f"NEW GAME")
        self.model.play_async(type=midi_builder.MusicBuildType.GAME)
        self.model.set_state(state.State.GAME)
        
#------------------------------------------------------------------------------
    @Slot(None, result=str)
    def get_media_folder(self):
        return QUrl.fromLocalFile(os.path.join(os.environ["SystemRoot"], "Media")).toString()
        
#------------------------------------------------------------------------------
    @Slot(str, result=str)
    def tr(self, key):
        return self.app.tr(key)
    
#------------------------------------------------------------------------------
    @Slot(str, result=None)
    def selectLanguage(self, hl):
        # TODO: Save the user's choice!
        self.model._language.set(hl)
        self.translator.selectLanguage(hl)
        self.languageChanged.emit()
        
# -------------- str property --------------
# This is needed to update string in qml, it's weird, but it's what they do in Qt's doc.
# (See tr() in main.qml)
    @Slot()
    def get_empty_string(self):
        return ""
    languageChanged = Signal()
    p_ = Property(str, get_empty_string, notify=languageChanged)
    
#------------------------------------------------------------------------------
    def run(self) -> int:
        self.model.start()
        retval = self.app.exec()
        logger.info("Shutting down...")
        self.model.shutdown()
                
        return retval
        