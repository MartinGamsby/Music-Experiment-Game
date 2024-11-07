import sys
import os
import pathlib
from time import sleep, time
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, Property, QStandardPaths

import model
import state
import midi_builder

#------------------------------------------------------------------------------
class Backend(QObject):
    
    def __init__(self, qml_file, app, model: model.Model):
        super().__init__()        
        self.model = model
        
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
    def ok_pressed(self, value: str):
        print(f"BUTTON PRESSED: {value}")
        if value:
            self.model.play_async(value, type=midi_builder.MusicBuildType.FILE)
        else:
            self.model.play_async(value, type=midi_builder.MusicBuildType.DROPS)
        
#------------------------------------------------------------------------------
    @Slot(bool)
    def toMainMenu(self, play: bool):
        print(f"TO MAIN MENU")
        if play:
            self.model.play_async("assets/town.mid")
        self.model.set_state(state.State.MAIN_MENU)
        
#------------------------------------------------------------------------------
    @Slot(None)
    def playMidis(self):
        print(f"PLAY MIDIS")
        self.model.set_state(state.State.PLAY_MIDIS)
        
#------------------------------------------------------------------------------
    @Slot(None)
    def newGame(self):
        print(f"NEW GAME")
        self.model.play_async(type=midi_builder.MusicBuildType.GAME)
        self.model.set_state(state.State.GAME)
        
#------------------------------------------------------------------------------
    @Slot(None, result=str)
    def get_media_folder(self):
        return "file:///" + QStandardPaths.writableLocation(QStandardPaths.MusicLocation)
        
#------------------------------------------------------------------------------
    def run(self) -> int:
        self.model.start()
        retval = self.app.exec()
        print("Shutting down...")
        self.model.shutdown()
                
        sys.exit(retval)
        