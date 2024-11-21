import sys
import os
import pathlib
from helpers.file_helper import abspath, tempfile_path, get_appdata_file
from helpers.setting import Setting
from helpers.save import Save
from time import sleep, time
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, Property, QTimer, QThread, QLocale
import threading
import symusic_midi
from music import midi_builder, midi_helper

from state import State, MusicState

import logging
logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
class Model(QObject):
    appExiting = Signal()
    model_changed = Signal()
    save_config = Save()
    save_progress = Save()

#------------------------------------------------------------------------------
    def __init__(self, app):
        super().__init__(app)
        self.save_config.init(get_appdata_file("config.ini", subfolder="Config"))
        self.save_progress.init(get_appdata_file("default.sav", subfolder="Save"))
        
        self.app = app
        self.start_time = time()
        self.t = None
        
        self.state = State.NONE
        self.music_state = MusicState.NONE
        #self._title = ""#Setting("DEFAULT TITLE")
        
        self.music_progress = 0.0
                
        self.set_state(State.INIT)
        self.set_music_state(State.INIT)
        
        self.last_beat_ms = 0
        
        self._language.unlock()
        self._generate_mp3.unlock()
        # TODO: When?
        # After a few water drops?
        # Is that in the backend?
        # Save number of "songs", and time spent? (in music cb?)
        #self._ideas.unlock() 
        
        
#------------------------------------------------------------------------------
    def __del__(self):
        self.save_config.write_config() # TODO: More often than that...
        self.thread.deleteLater() #TODO: stop the thread
    
#------------------------------------------------------------------------------
    def init(self):
        self.state_updated.emit()
        self.music_state_updated.emit()
        
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
        self.play_main_menu()
        
#------------------------------------------------------------------------------
    def play_main_menu(self):
        #TODO: setting for one of these:
        self.play_async(abspath("assets/town.mid"))
        #self.play_async("")
        #self.play_async("", type=midi_builder.MusicBuildType.DROPS)
        #self.play_async("", type=midi_builder.MusicBuildType.GAME)
        #self.play_async("", type=midi_builder.MusicBuildType.MINGUS)
        
        # TODO: Repeat? 
        
#------------------------------------------------------------------------------
    def shutdown(self):
        import pygame_midi
        pygame_midi.stop_music()
        
#------------------------------------------------------------------------------
    def play_async(self, filename="", type=midi_builder.MusicBuildType.FILE):
        self.filename = abspath(filename)
        # TODO: Start the actual model, move things to the backend, too much in model already.
        
        # TODO: Actually kill the thread, don't do nothing!
        #if (not self.t or not self.t.is_alive()) and self.music_state != MusicState.GENERATING:
        if self.music_state != MusicState.GENERATING and self.music_state != MusicState.PREPARING:
            self.set_music_state(MusicState.PREPARING) # TODO: Prep state?
            self.t = threading.Thread(target=self._play_prepare, args=(type,))
            self.t.start()
        
#------------------------------------------------------------------------------
    def _play_prepare(self, type):
        try:
            import pygame_midi
            
            pygame_midi.stop_music()
            self.set_music_state(MusicState.GENERATING)       
            
            if not self.filename:        
                
                filename = get_appdata_file("__DefaultOutput.mid", subfolder="Music")# "Midi"?
                midi_builder.make_midi(filename, type=type)
            else:
                filename = self.filename
            if self._generate_mp3.get():
                logger.info("GENERATE WAV FROM MIDI")
                symusic_midi.midi_to_wav_worker(self.worker, self.thread, filename, force_gen=not self.filename)
            else:
                logger.info("DON'T Generate wav from midi")
                self.out_filename = filename
                self.worker_finished()        
        except:
            logging.exception("_play_prepare")
            self.out_filename = ""
            self.set_music_state(MusicState.ERROR)            
            
        
#------------------------------------------------------------------------------
    def worker_finished(self):
        self.set_music_state(MusicState.PREPARING)
        logger.info(f"_generate_mp3: {self._generate_mp3.get()}")
        if self._generate_mp3.get():
            self.out_filename = self.worker.out_filename
            
            if self.worker.out_filename == "":#TODO: better error handling?            
                self.set_music_state(MusicState.ERROR)
                return #ERROR, notify the user better?
            logger.info(f"finished {self.out_filename}")
        
        self.t = threading.Thread(target=self._play)
        self.t.start()
        
#------------------------------------------------------------------------------
    def _play(self):
        import pygame_midi
        pygame_midi.init(2)
        #After init. In class? Make another class that can be either pygame or something else?
        self.set_music_state(MusicState.PREPARING)
        logger.info("Play!")
        
        if self.state == State.INIT:
            self.set_state(State.WELCOME)
            
        # Return music state from here?
        self.set_music_state(MusicState.PLAYING)
        pygame_midi.play(self.out_filename, self.music_cb)
    
#------------------------------------------------------------------------------
    def music_cb(self, at_ms, to_ms):
        progress_pc = (at_ms/to_ms)
        self._music_progress.set(progress_pc)
        
        #Let's assume that for now:
        tempo = midi_helper.TEMPO["VIVACE"]
        # b    b       b       60000/bps = ms per beat
        # - = --- = ------- => 
        # m   60s   60000ms
        ms_per_beat = 60000/tempo
        
        if at_ms > self.last_beat_ms:
            if self.last_beat_ms > 0:
                logger.debug(f"at {at_ms}, beat={int(ms_per_beat)}ms")
                self._music_beat.set(self._music_beat.get()+1)
                self.last_beat_ms += ms_per_beat
            else:            
                self.last_beat_ms += 0.001#ms_per_beat/2 # TODO: Is this what midi to wav does?
        elif at_ms < (self.last_beat_ms - ms_per_beat):
            self.last_beat_ms = 0# TODO: This is sketchy...
            self._music_beat.set(0)
            
        
        
        if at_ms >= to_ms:
            self.last_beat_ms = 0
            self._music_beat.set(0)
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
    
    # TODO: Bundle to enum type?
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
        if self.state == State.INIT:
            return self.app.tr("MESSAGE_INITIALIZING")
        elif self.state == State.WELCOME:
            return self.app.tr("MESSAGE_WELCOME")
        return self.state.name
    p_state_pretty_name = Property(str, get_state_pretty_name, notify=state_updated)
    
#------------------------------------------------------------------------------
    def set_music_state(self, state):
        if self.music_state != state:
            self.music_state = state
            self.music_state_updated.emit()
            if self.music_state == MusicState.PLAYING:
                try:
                    # TODO: Add a way to know if it's converted to mp3 or not? (say that the quality might be lower..)
                    self._title.set(os.path.splitext(os.path.basename(self.filename))[0])
                except:
                    self._title.set("Unnamed")
            else:
                self._title.set("")
            #self.title_updated.emit()
    
    music_state_updated = Signal()
        
    # -------------- int property --------------
    @Slot()
    def get_music_state_id(self):
        return self.music_state.value
    p_music_state_id = Property(int, get_music_state_id, notify=music_state_updated)
    
    # -------------- str property --------------
    @Slot()
    def get_music_state_pretty_name(self):
        if self.music_state == MusicState.INIT:
            return self.app.tr("STATE_INITIALIZING")
        elif self.music_state == MusicState.IDLE:
            return self.app.tr("STATE_IDLE")
        elif self.music_state == MusicState.PREPARING:
            return self.app.tr("STATE_PREPARING")
        elif self.music_state == MusicState.GENERATING:
            return self.app.tr("STATE_GENERATING")
        elif self.music_state == MusicState.PLAYING:
            return self.app.tr("STATE_PLAYING")
        return self.music_state.name
    p_music_state_pretty_name = Property(str, get_music_state_pretty_name, notify=music_state_updated)

#------------------------------------------------------------------------------
    _title = Setting("DEFAULT TITLE", "title", save=None)
    def get_title(self): return self._title # TODO: Move that inside Setting() class??
    p_title = Property(QObject, get_title, notify=model_changed)
    
#------------------------------------------------------------------------------
    _music_progress = Setting(0.0, "music_progress", save=None)
    def get_music_progress(self): return self._music_progress
    p_music_progress = Property(QObject, get_music_progress, notify=model_changed)
    
#------------------------------------------------------------------------------
    _music_beat = Setting(0, "music_beat", save=None)
    def get_music_beat(self): return self._music_beat
    p_music_beat = Property(QObject, get_music_beat, notify=model_changed)
    
#------------------------------------------------------------------------------
    _language = Setting(QLocale().name(), "Config/language", save=save_config, save_progress=save_progress)
    def get_language(self): return self._language
    p_language = Property(QObject, get_language, notify=model_changed)
    
#------------------------------------------------------------------------------
    _generate_mp3 = Setting(True, "Config/generate_mp3", save=save_config, save_progress=save_progress)
    def get_generate_mp3(self): return self._generate_mp3
    p_generate_mp3 = Property(QObject, get_generate_mp3, notify=model_changed)
    
#------------------------------------------------------------------------------
    _ideas = Setting(0, "Progress/ideas", save=save_progress)
    def get_ideas(self): return self._ideas
    p_ideas = Property(QObject, get_ideas, notify=model_changed)
    