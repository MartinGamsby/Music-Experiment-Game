import sys
import os
import pathlib
from time import sleep, time
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, Property, QTimer, QThread
import threading
import symusic_midi
import midi_builder

from state import State, MusicState

#------------------------------------------------------------------------------
class Model(QObject):
    appExiting = Signal()

#------------------------------------------------------------------------------
    def __init__(self, parent):
        super().__init__(parent)
        self.start_time = time()
        self.generate_mp3 = True#True# TODO: Save settings
        self.t = None
        
        self.state = State.NONE
        self.music_state = MusicState.NONE
        self.title = ""
        self.music_progress = 0.0
        
        
        self.set_state(State.INIT)
        self.set_music_state(State.INIT)
        
    def __del__(self):
        self.thread.deleteLater() #TODO: stop the thread
    
#------------------------------------------------------------------------------
    def init(self):
        self.state_updated.emit()
        self.music_state_updated.emit()
        self.title_updated.emit()
        
        self.thread_init()
        
        t = threading.Thread(target=self.async_init)
        t.start()
        
#------------------------------------------------------------------------------
    def thread_init(self):
        self.thread = QThread(self)
        self.worker = symusic_midi.Worker(thread=self.thread)
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.worker_finished)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        
#------------------------------------------------------------------------------
    def async_init(self):        
        ###TODO::: not first? Or only generate?
        sleep(0.5)#Let the UI open or something?
        self.play_async("assets/town.mid")#
        
#------------------------------------------------------------------------------
    def shutdown(self):
        import pygame_midi
        pygame_midi.stop_music()
        
#------------------------------------------------------------------------------
    def play_async(self, filename="", type=midi_builder.MusicBuildType.FILE):
        self.filename = filename # TODO: Start the actual model, move things to the backend, too much in model already.
        
        # TODO: Actually kill the thread, don't do nothing!
        #if (not self.t or not self.t.is_alive()) and self.music_state != MusicState.GENERATING:
        if self.music_state != MusicState.GENERATING and self.music_state != MusicState.PREPARING:
            self.set_music_state(MusicState.PREPARING) # TODO: Prep state?
            self.t = threading.Thread(target=self._play_prepare, args=(type,))
            self.t.start()
        
#------------------------------------------------------------------------------
    def _play_prepare(self, type):
        try:
            import midi_builder
            import pygame_midi
            
            pygame_midi.stop_music()
            self.set_music_state(MusicState.GENERATING)       
            
            if not self.filename:        
                filename = "__DefaultOutput.mid"
                midi_builder.make_midi(filename, type=type)
            else:
                filename = self.filename
            if self.generate_mp3:       
                print("GENERATE WAV FROM MIDI")
                symusic_midi.midi_to_wav_worker(self.worker, self.thread, filename, force_gen=not self.filename)
            else:
                print("DON'T Generate wav from midi")
                self.out_filename = filename
                self.worker_finished()        
        except:
            # TODO: Print/Log the error
            self.out_filename = ""
            self.set_music_state(MusicState.ERROR)            
            
        
#------------------------------------------------------------------------------
    def worker_finished(self):
        self.set_music_state(MusicState.PREPARING)
        if self.generate_mp3:
            self.out_filename = self.worker.out_filename
            
            if self.worker.out_filename == "":#TODO: better error handling?            
                self.set_music_state(MusicState.ERROR)
                return #ERROR, notify the user better?
            print("finished", self.out_filename)            
        
        self.t = threading.Thread(target=self._play)
        self.t.start()
        
#------------------------------------------------------------------------------
    def _play(self):
        import pygame_midi
        pygame_midi.init(2)
        #After init. In class? Make another class that can be either pygame or something else?
        self.set_music_state(MusicState.PREPARING)
        print("Play!")
        
        if self.state == State.INIT:
            self.set_state(State.WELCOME)
            
        # Return music state from here?
        self.set_music_state(MusicState.PLAYING)
        pygame_midi.play(self.out_filename, self.music_cb)
    
#------------------------------------------------------------------------------
    def music_cb(self, at_ms, to_ms):
        progress_pc = (at_ms/to_ms)
        self.set_music_progress(progress_pc)
        
        if at_ms >= to_ms:
            self.set_music_state(MusicState.IDLE)
        
        
    
#------------------------------------------------------------------------------
    def get_time(self):
        return time()-self.start_time
        
#------------------------------------------------------------------------------
    def start(self):
        # TODO?
        pass
        
        
        
#------------------------------------------------------------------------------
    def set_state(self, state):
        if self.state != state:
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
        if self.music_state != state:
            self.music_state = state
            self.music_state_updated.emit()
            if self.music_state == MusicState.PLAYING:
                try:
                    self.set_title(os.path.splitext(os.path.basename(self.filename))[0])
                except:
                    self.set_title("Unnamed")                    
            else:
                self.set_title("")
    
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
        elif self.music_state == MusicState.PREPARING:
            return "Preparing"
        elif self.music_state == MusicState.GENERATING:
            return "Generating"
        elif self.music_state == MusicState.PLAYING:
            return "Playing"
        return self.music_state.name
    p_music_state_pretty_name = Property(str, get_music_state_pretty_name, notify=music_state_updated)

#------------------------------------------------------------------------------
    # -------------- str property title --------------
    def set_title(self, title):
        if self.title != title:
            self.title = title
            self.title_updated.emit()
        
    title_updated = Signal()
    
    @Slot()
    def get_title(self):
        return self.title
    p_title = Property(str, get_title, notify=title_updated)
    
#------------------------------------------------------------------------------
    # -------------- bool property generate_mp3 --------------
    @Slot(bool)
    def set_generate_mp3(self, generate_mp3: bool):
        if self.generate_mp3 != generate_mp3:
            self.generate_mp3 = generate_mp3
            self.generate_mp3_updated.emit()
        
    generate_mp3_updated = Signal()
    
    @Slot()
    def get_generate_mp3(self):
        return self.generate_mp3
    p_generate_mp3 = Property(bool, get_generate_mp3, notify=generate_mp3_updated)
    
#------------------------------------------------------------------------------
    # -------------- float property music_progress --------------
    @Slot(float)
    def set_music_progress(self, music_progress: float):
        if self.music_progress != music_progress:
            self.music_progress = music_progress
            self.music_progress_updated.emit()
        
    music_progress_updated = Signal()
    
    @Slot()
    def get_music_progress(self):
        return self.music_progress
    p_music_progress = Property(float, get_music_progress, notify=music_progress_updated)
    