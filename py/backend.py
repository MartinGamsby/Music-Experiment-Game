import sys
import os
import pathlib
from time import sleep, time
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, Property

import model
import state

#------------------------------------------------------------------------------
class Backend(QObject):
    
    def __init__(self, qml_file, model: model.Model):
        super().__init__()        
        self.model = model
        
        self.app = QGuiApplication(sys.argv)
        
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
        print(f"OK PRESSED: {value}")
        self.model.play_async()
        
#------------------------------------------------------------------------------
    def run(self) -> int:
        self.model.start()
        retval = self.app.exec()
        print("Shutting down...")
        self.model.shutdown()
                
        sys.exit(retval)
        