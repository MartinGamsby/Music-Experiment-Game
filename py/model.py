import sys
import os
import pathlib
from time import sleep, time
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, Property, QTimer
import threading

from state import State, MusicState

#------------------------------------------------------------------------------
class Model(QObject):
    appExiting = Signal()

#------------------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.start_time = time()
        
        self.set_state(State.INIT)
        self.set_music_state(State.INIT)
        
        t = threading.Thread(target=self.async_init)
        t.start()
        
#------------------------------------------------------------------------------
    def init(self):
        self.state_updated.emit()
        self.music_state_updated.emit()
        
#------------------------------------------------------------------------------
    def shutdown(self):
        import pygame_midi
        pygame_midi.stop_music()
        
#------------------------------------------------------------------------------
    def play_async(self):
        self.t = threading.Thread(target=self._play)
        self.t.start()
        
#------------------------------------------------------------------------------
    def _play(self):
        import midi_builder
        import pygame_midi
        
        pygame_midi.stop_music()
        
        
        
        self.set_music_state(MusicState.GENERATING)
        filename = "output.mid"
        midi_builder.make_midi(filename)
        #sleep(1)
        
        pygame_midi.init(2)
        #After init. In class? Make another class that can be either pygame or something else?
        self.set_music_state(MusicState.IDLE)
        print("Play!")
        
        if self.state == State.INIT:
            self.set_state(State.WELCOME)
            
        # Return music state from here?
        self.set_music_state(MusicState.PLAYING)
        pygame_midi.play(filename)
        self.set_music_state(MusicState.IDLE)
        

#------------------------------------------------------------------------------
    def async_init(self):
        self.play_async()        
    
#------------------------------------------------------------------------------
    def get_time(self):
        return time()-self.start_time
        
#------------------------------------------------------------------------------
    def start(self):
        # TODO?
        pass
        
#------------------------------------------------------------------------------
    def set_state(self, state):
        self.state = state
        self.state_updated.emit()
        
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
    
#------------------------------------------------------------------------------
    def set_music_state(self, state):
        self.music_state = state
        self.music_state_updated.emit()
    
    music_state_updated = Signal()
        
    # -------------- int property --------------
    @Slot()
    def get_music_state_id(self):
        return self.music_state.value
    p_music_state_id = Property(int, get_music_state_id, notify=music_state_updated)
    
    # -------------- str property --------------
    @Slot()
    def get_music_state_pretty_name(self):
        # TODO: Translate mechanism instead.
        if self.music_state == MusicState.INIT:
            return "Initializing"
        elif self.music_state == MusicState.IDLE:
            return "Idle"
        elif self.music_state == MusicState.GENERATING:
            return "Generating"
        elif self.music_state == MusicState.PLAYING:
            return "Playing"
        return self.music_state.name
    p_music_state_pretty_name = Property(str, get_music_state_pretty_name, notify=music_state_updated)

