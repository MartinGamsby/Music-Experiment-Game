import sys
import os
import pathlib
from time import sleep, time
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, Property, QTimer
from enum import Enum
import threading

#------------------------------------------------------------------------------
State = Enum(
    'State',
    [
        ('INIT',1),
        ('WELCOME',2),
    ]
)


#------------------------------------------------------------------------------
class Model(QObject):
    appExiting = Signal()

#------------------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.start_time = time()
        self.set_state(State.INIT)
        
        # Fake init async for now.
        t = threading.Thread(target=self.fake_init)
        t.start()
        
#------------------------------------------------------------------------------
    def fake_init(self):
        sleep(1)
        self.set_state(State.WELCOME)
        
    
#------------------------------------------------------------------------------
    def set_state(self, state):
        self.state = state
        self.state_updated.emit()
        
#------------------------------------------------------------------------------
    def init(self):
        self.state_updated.emit()
        
#------------------------------------------------------------------------------
    def get_time(self):
        return time()-self.start_time
        
#------------------------------------------------------------------------------
    def start(self):
        # TODO?
        pass
        
#------------------------------------------------------------------------------
    state_updated = Signal()
    
    # -------------- str property --------------
    @Slot()
    def get_state_name(self):
        return self.state.name
    p_state_name = Property(str, get_state_name, notify=state_updated)
    
    # -------------- int property --------------
    @Slot()
    def get_state_id(self):
        return self.state.value
    p_state_id = Property(int, get_state_id, notify=state_updated)

    # -------------- str property --------------
    @Slot()
    def get_state_pretty_name(self):
        # TODO: Translate mechanism instead.
        if self.state == State.INIT:
            return "Initializing"
        elif self.state == State.WELCOME:
            return "Welcome"
        return self.state.name
    p_state_pretty_name = Property(str, get_state_pretty_name, notify=state_updated)
    

