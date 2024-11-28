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
from music import midi_builder

import helpers.translator as translator

import logging
logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
class Backend(QObject):
    
    def __init__(self, qml_file, app, model: model.Model):
        super().__init__()

        self.model = model
        # TODO: Not the best way ... need to have real multiple save files.
        logger.info(f"game progress: {self.model._game_progress.get()}")
        self._has_save_files.set(self.model._game_progress.get() > 0)
        
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
        logger.info(f" [User pressed]  play_mid_pressed({value})")
        value = abspath(value)
        if value:
            self.model.play_async(midi_builder.MusicBuildType.FILE, value)
        else:
            self.model.play_async(midi_builder.MusicBuildType.DROPS, value)
        
#------------------------------------------------------------------------------
    @Slot(bool)
    def toMainMenu(self, play: bool):
        logger.info(f" [User pressed]  toMainMenu({play})")
        if play:
            self.model.play_main_menu(state.State.MAIN_MENU)
        self.model.set_state(state.State.MAIN_MENU)
        
#------------------------------------------------------------------------------
    @Slot(None)
    def playMidis(self):
        logger.info(f" [User pressed]  playMidis")
        self.model.set_state(state.State.PLAY_MIDIS)
        
#------------------------------------------------------------------------------
    @Slot(None)
    def newGame(self):
        logger.info(f" [User pressed]  newGame")
        self.model.newGame()
        self._has_save_files.set(True) # TODO: Not the best way ... need to have real multiple save files.
        
        self.model.set_state(state.State.GAME)
        
#------------------------------------------------------------------------------
    @Slot(None)
    def loadGame(self):
        logger.info(f" [User pressed]  loadGame")
        self.model.loadGame()
        
        self.model.set_state(state.State.GAME)
        
#------------------------------------------------------------------------------
    @Slot(None)
    def toSettings(self):
        logger.info(f" [User pressed]  toSettings")
        self.model.set_state(state.State.SETTINGS)
        
#------------------------------------------------------------------------------
    @Slot(None)
    def makeAnotherMusic(self):
        logger.info(f" [User pressed]  makeAnotherMusic")
        self.model.play_async(type=midi_builder.MusicBuildType.GAME)
        
#------------------------------------------------------------------------------
    @Slot(None)
    def exit(self):
        self.app.exit()
        
#------------------------------------------------------------------------------
    model_changed = Signal()
    _has_save_files = Setting(False, "has_save_files")
    def get_has_save_files(self): return self._has_save_files
    p_has_save_files = Property(QObject, get_has_save_files, notify=model_changed)
    
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
        