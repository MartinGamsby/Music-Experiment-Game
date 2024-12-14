import sys
import os
import random
import pathlib
from helpers.file_helper import abspath, tempfile_path, get_appdata_file
from helpers.setting import Setting
from helpers.steps import Steps
from helpers.save import Save
from time import sleep, time
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, Property, QTimer, QThread, QLocale
import threading
import symusic_midi
from music import midi_helper
from datetime import datetime

from state import State, MusicState

import logging
logger = logging.getLogger(__name__)

avg_half_frame_ms = 8#1000/60/2 (TODO: Get the actual framerate, or moving avg, or something..)


DEBUG_TIME = False

BEATS_PER_MEASURE = (1 if DEBUG_TIME else 4)
MS_PER_S = (250 if DEBUG_TIME else 1000)

UPDATE_EVERY_MEASURE = True # TODO: Needs to be only when we don't play video? (Or could it be in another thread to not slow down the playback?)
UPDATE_EVERY_BEAT = False # 

#------------------------------------------------------------------------------
class Model(QObject):
    appExiting = Signal()
    model_changed = Signal()
    detailed_changed = Signal()
    save_config = Save()
    save_progress = Save()

#------------------------------------------------------------------------------
    def __init__(self, app, engine=None):
        super().__init__(app)
        self.save_config.init(get_appdata_file("config.ini", subfolder="Config"))
        self.save_progress.init(get_appdata_file("default.sav", subfolder="Save"))
        
        self.app = app
        self.engine = engine # TODO: Move all of that in backend instead...
        self.start_time = time()
        self.t = None
        
        self.state = State.NONE
        self.music_state = MusicState.NONE
        #self._title = ""#Setting("DEFAULT TITLE")
        
        self.music_progress = 0.0
                
        self.set_state(State.INIT)
        self.set_music_state(State.INIT)
        
        self.last_beat_ms = 0
                
        self._tempo = -1
        
        self._last_type = None
        
        self._steps = Steps()
        
        self.thread = None
        self.update_thread = None
        
        # Hook settings
        self._music_attrs = {}
        self._music_properties = []
        for a in dir(self):
            if a.startswith("_"):
                attr = getattr(self, a)
                if type(attr) == Setting:
                    if attr._section == "Music":
                        self._music_attrs[a] = attr
                        self._music_properties.append( attr )
                        attr.value_updated.connect(self.value_updated)
        self._measures = None
        
#------------------------------------------------------------------------------
    def __del__(self):
        self.save_config.write_config() # TODO: More often than that...
        if self.thread:
            self.thread.deleteLater() #TODO: stop the thread
        if self.update_thread:
            self.update_thread.join()
    
#------------------------------------------------------------------------------
    def init(self):
        self.state_updated.emit()
        self.music_state_updated.emit()
        
        self.thread_init()
        
        t = threading.Thread(target=self.async_init)
        t.start()
        
#------------------------------------------------------------------------------
    def value_updated(self):
        logger.info(f"value updated ({self.sender()})")
        
        ideas = 0
        
        # Uh we need to do the dependencies of dependencies and all... this is the worst way to do it, sorry
        for i in range(5):
            for a in self._music_attrs:
                attr = self._music_attrs[a]
                
                valid = True
                for d in attr._dependencies:#_weak_dependencies:
                    if not d.unlocked() or not d.gete():
                        valid = False
                        
                attr.setEnabled(valid)
                if valid:
                    attr.unlock()
                    
                if i == 0 and attr.enabled() and attr.gete():# TODO: what if not bool?
                    ideas += 1
                
            
        self._ideas.set(ideas)
        logger.info(f"Used ideas: {ideas}/{self._total_ideas.get()}")
        
        # Make another music
        self.play_async(type=self._last_type, filename=self.filename)
        
#------------------------------------------------------------------------------
    def newGame(self):
        self.save_progress.reset()
        self.model_changed.emit()
        
        self.loadGame()
        
#------------------------------------------------------------------------------
    def loadGame(self):
        self.apply_step()
        
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
        sleep(0.75)#Let the UI open or something?
        self.play_main_menu(State.GAME if self._autoload.get() else State.MAIN_MENU)
        
#------------------------------------------------------------------------------
    def play_main_menu(self, state=State.MAIN_MENU):
    
        if state == State.GAME:
            if self._game_progress.get() > 0:
                self.loadGame()
                self.set_state(state)
                return
            
        #TODO: setting for one of these:        
        from music import builder
        self.play_async(builder.MusicBuildType.FILE, abspath("assets/town.mid"))
        #self.play_async("")
        #self.play_async("", type=builder.MusicBuildType.DROPS)
        #self.play_async("", type=builder.MusicBuildType.GAME)
        #self.play_async("", type=builder.MusicBuildType.MINGUS)
        
        # TODO: Repeat? 
        
#------------------------------------------------------------------------------
    def shutdown(self):
        self.stop_music()
        
#------------------------------------------------------------------------------
    def play_async(self, type, filename=""):
        logger.debug(f"from {self._last_type} to {type}")        
        
        from music import builder
        self._music_description.set(builder.describe_music(self.app, self._music_attrs, f"<br /><font color='silver'>{self.app.tr("GENERATING_")}</font>"))
        self.update_detailed(0,0)
        
        self._last_type = type
    
        self.filename = abspath(filename)
        # TODO: Start the actual model, move things to the backend, too much in model already.
        
        # TODO: Actually kill the thread, don't do nothing!
        #if (not self.t or not self.t.is_alive()) and self.music_state != MusicState.GENERATING:
        if self.music_state != MusicState.GENERATING and self.music_state != MusicState.PREPARING:
            self.set_music_state(MusicState.PREPARING) # TODO: Prep state?
            self.t = threading.Thread(target=self._play_prepare, args=(type,))
            self.t.start()
            
#------------------------------------------------------------------------------
    def stop_music(self):
        import pygame_midi
        pygame_midi.stop_music()    
        self._gui_play_video.reset()
        self._is_video.reset()
        
#------------------------------------------------------------------------------
    def generating_step(self, step):
        self._generating_step.set(step)
        self.set_music_state(MusicState.GENERATING)
        self.music_state_updated.emit()
        
#------------------------------------------------------------------------------
    def _play_prepare(self, type):
        try:            
            self.stop_music()
            self._tempo = -1
            self.generating_step(0)
            if not self.filename:        
                filename = get_appdata_file(f"{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}.mid", subfolder="Music")# "Midi"?
                from music import builder
                self._measures, desc, self._tempo = builder.make_midi(filename, self.app, self._music_attrs, type=type)
                self._music_description.set(desc)
                self.update_detailed(0,0)
            else:
                filename = self.filename
                self._music_description.set("")
                self.update_detailed(-1)
            if self._generate_mp3.get():
                logger.debug("GENERATE WAV FROM MIDI")
                symusic_midi.midi_to_wav_worker(self.worker, self.thread, filename, force_gen=not self.filename, progress_cb=self.generating_step)
            else:
                logger.debug("DON'T Generate wav from midi")
                self.out_filename = filename
                self.worker_finished()        
        except:
            logging.exception("_play_prepare")
            self.out_filename = ""
            self.set_music_state(MusicState.ERROR)            
            
        
#------------------------------------------------------------------------------
    def worker_finished(self):
        #self.set_music_state(MusicState.PREPARING)
        logger.debug(f"_generate_mp3: {self._generate_mp3.get()}")
        if self._generate_mp3.get():
            self.out_filename = self.worker.out_filename
            
            if self.worker.out_filename == "":#TODO: better error handling?            
                self.set_music_state(MusicState.ERROR)
                return #ERROR, notify the user better?
            logger.debug(f"finished {self.out_filename}")
        
        self.t = threading.Thread(target=self._play)
        self.t.start()
        
#------------------------------------------------------------------------------
    def _play(self):
        import pygame_midi
        pygame_midi.init(2)
        #After init. In class? Make another class that can be either pygame or something else?
        if self.music_state != MusicState.GENERATING:
            self.set_music_state(MusicState.PREPARING)
        
        logger.debug("Play!")
        
        if self.state == State.INIT:
            self.set_state(State.WELCOME)
            
        # Return music state from here?
        if self.out_filename.endswith(".mp4"):
            logger.info("PLAY MP4")            
            self._gui_play_video.set(f"file:///{self.out_filename}", force=True)
            #self.generating_step
            for i in range(6):
                sleep(0.08)#TODO? (Is this why the sound is choppy sometimes?
                self.generating_step(95+i)# Relative to last step in symusic_midi.on_video_progress
            
            self.set_music_state(MusicState.PLAYING)        
            self._is_video.set(True)
            self._gui_play_video.value_updated.emit()
        else:
            self._is_video.set(False)
            pygame_midi.play(self.out_filename, self.music_cb)
    
#------------------------------------------------------------------------------
    @Slot(int, int, bool, result=None)
    def music_cb(self, at_ms, to_ms, mp4=False):
        progress_pc = (at_ms/to_ms)
        self._music_progress.set(progress_pc)
        
        #Let's assume that for now:
        if self._tempo > 0:
            tempo = self._tempo
        else:
            tempo = midi_helper.TEMPO["VIVACE"]
        # b    b       b       60000/bps = ms per beat
        # - = --- = ------- => 
        # m   60s   60000ms
        ms_per_beat = 60000/tempo
        
        
        if at_ms > (self.last_beat_ms-avg_half_frame_ms):
            if self.last_beat_ms > 0:
                nb_beats = self._music_beat.get()
                if nb_beats > 0:                
                    if self.state == State.GAME:
                        beat_idx = nb_beats % BEATS_PER_MEASURE
                        
                        do_update = False                            
                        if not(beat_idx):
                            self.add_time_listened(int(ms_per_beat*BEATS_PER_MEASURE))
                            logger.debug(f"at {at_ms} (beats#{nb_beats}, {int(ms_per_beat)}ms/beat (listened a total of: {int(self._time_listened.get()/1000)}s)")
                            if UPDATE_EVERY_MEASURE:
                                do_update = True
                        if UPDATE_EVERY_BEAT:
                            do_update = True
                        
                        # Every beat:
                        if do_update:
                            start_thread = (self.update_thread == None)
                            if self.update_thread:
                                if not self.update_thread.is_alive():
                                    start_thread = True
                            if start_thread:                                
                                if not UPDATE_EVERY_BEAT:
                                    beat_idx = -1
                                self.update_thread = threading.Thread(target = self.update_detailed, args = (int(nb_beats / BEATS_PER_MEASURE), beat_idx))
                                self.update_thread.start()
                        
                if UPDATE_EVERY_MEASURE:
                    self._music_beat.add(1)
                
                self.last_beat_ms += ms_per_beat
            else:            
                if self.state == State.GAME:
                    self.add_time_listened(1)
                # 1000 if we have midi_render.ADD_ONE_SECOND_BUFFER
                self.last_beat_ms += 1#1000 if mp4 else 1#ms_per_beat/2 # TODO: Is this what midi to wav does?
        elif at_ms < (self.last_beat_ms - ms_per_beat):
            self.last_beat_ms = 0# TODO: This is sketchy...
            self._music_beat.set(0)
            
        
        
        if at_ms >= to_ms:
            self.last_beat_ms = 0
            self._music_beat.set(0)
            self.set_music_state(MusicState.IDLE)
            
            if self._auto_replay.get():
                self.play_async(type=self._last_type)
        
#------------------------------------------------------------------------------
    def update_game_title(self):
        key = self.current_step_name()
        value = self.app.tr(key)
        if not value or value != key:
            self._game_title.set(value)
        else:
            logger.error("Translate string not found")
            self._game_title.set("GAME_LAST")
        
#------------------------------------------------------------------------------
    def get_seconds(self, s):
        return s*MS_PER_S
        
#------------------------------------------------------------------------------
    def add_time_listened(self, time_added):
        self._time_listened.add(time_added)
        
        step = self._game_progress.get()
        
        s_to_next = self.current_step_seconds_to_next()
        if s_to_next != -1:
            if self._time_listened.get() > self.get_seconds(s_to_next):
                self.next_step()
        
#------------------------------------------------------------------------------
    def current_step(self):
        return self._steps.get(self._game_progress.get())
        
    def current_step_to(self):
        return self._steps.to(self._game_progress.get())
        
    def current_step_name(self):
        return self._steps.name(self._game_progress.get())
        
    def current_step_unlocks(self):
        return self._steps.unlocks(self._game_progress.get())
        
    def current_step_adds(self):
        return self._steps.adds(self._game_progress.get())
        
    def current_step_seconds_to_next(self):
        return self._steps.seconds_to_next(self._game_progress.get())
        
#------------------------------------------------------------------------------
    def next_step(self):
        """ Things that need to be done only one when changing to step x """                
        
        self._game_progress.set(self.current_step_to())
        
        for u in self.current_step_unlocks():
            getattr(self, "_"+u).unlock()
        
        adds = self.current_step_adds()
        for key in adds:
            getattr(self, "_"+key).add(adds[key])
            
        self.apply_step()
                  
#------------------------------------------------------------------------------
    def apply_step(self):
        """ Things that need to be done every time when changing to step x (e.g. loading the game) """
        logger.info("APPLY STEP")
        step = self._game_progress.get()
        
        from music import builder
        #if step < 13375: # TODO:            
        #    desc = self.play_async(type=builder.MusicBuildType.DROPS)
        #else:
        desc = self.play_async(type=builder.MusicBuildType.GAME)            
        
        # Or ... save that in setting ... or ... always GAME, and is DROPS by default?
        
        self.update_game_title()
        self.value_updated()
            
            
#------------------------------------------------------------------------------
    def get_time(self):
        return time()-self.start_time
        
#------------------------------------------------------------------------------
    def start(self):
        # TODO?
        pass
        
#------------------------------------------------------------------------------
    @Slot()
    def get_music_settings(self):
        return self._music_properties
        
    p_music_settings = Property(list, get_music_settings, notify=model_changed)
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
    
    #------------------------------------------------------------------------------
    def getProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 0, length = 42, fill = '█'):
        """
        TODO: Better than that ... just do it in the UI ... but this is faster for now.
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '░' * (length - filledLength)
        return (f'{prefix} |{bar}| {percent}% {suffix}')
            
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
            return f"{self.app.tr("STATE_GENERATING")} {self.getProgressBar(self._generating_step.get(),100)}" #}{self._generating_step.get()}%"
        elif self.music_state == MusicState.PLAYING:
            return self.app.tr("STATE_PLAYING")
        return self.music_state.name
    p_music_state_pretty_name = Property(str, get_music_state_pretty_name, notify=music_state_updated)

#------------------------------------------------------------------------------
    _title = Setting("DEFAULT TITLE", "title")
    def get_title(self): return self._title # TODO: Move that inside Setting() class??
    p_title = Property(QObject, get_title, notify=model_changed)
    
    _game_title = Setting("GAME_0", "game_title")
    def get_game_title(self): return self._game_title
    p_game_title = Property(QObject, get_game_title, notify=model_changed)
    
    # TODO: Add a "gui" portion (to show or not) -- OR just a "what;'s shown", with a multi choice or something... maybe just a bool...
    _music_description = Setting("GAME_0", "music_description", save_progress=save_progress)
    def get_music_description(self): return self._music_description
    p_music_description = Property(QObject, get_music_description, notify=model_changed)
    
#------------------------------------------------------------------------------
    def update_detailed(self, measure, beat=-1):
        self._measure = measure
        self._measure_beat = beat
        self.detailed_changed.emit()
    def get_music_detailed_desc(self):
        from music import builder
        return self._music_description.get() + builder.get_desc_from_measure(self.app, self._music_attrs, self._measures, self._measure, self._measure_beat)
    _measure = 0
    _measure_beat = -1
    p_music_detailed_desc = Property(str, get_music_detailed_desc, notify=detailed_changed)
    
    
#------------------------------------------------------------------------------
    _music_progress = Setting(0.0, "music_progress")
    def get_music_progress(self): return self._music_progress
    p_music_progress = Property(QObject, get_music_progress, notify=model_changed)
    
    _music_beat = Setting(0, "music_beat")
    def get_music_beat(self): return self._music_beat
    p_music_beat = Property(QObject, get_music_beat, notify=model_changed)
    
    _gui_play_video = Setting("", "gui_play_video")
    def get_gui_play_video(self): return self._gui_play_video
    p_gui_play_video = Property(QObject, get_gui_play_video, notify=model_changed)
    
    _is_video = Setting(False, "is_video")
    def get_is_video(self): return self._is_video
    p_is_video = Property(QObject, get_is_video, notify=model_changed)
    
    _generating_step = Setting(0, "generating_step")
    def get_generating_step(self): return self._generating_step
    p_generating_step = Property(QObject, get_generating_step, notify=model_changed)
    
    
#------------------------------------------------------------------------------
    _language = Setting(QLocale().name(), "Config/language", save_config, save_progress=save_progress, auto_unlock=True)
    def get_language(self): return self._language
    p_language = Property(QObject, get_language, notify=model_changed)
    
    _generate_mp3 = Setting(True, "Config/generate_mp3", save_config, save_progress=save_progress, auto_unlock=True)
    def get_generate_mp3(self): return self._generate_mp3
    p_generate_mp3 = Property(QObject, get_generate_mp3, notify=model_changed)
    
    _fullscreen = Setting(True, "Config/fullscreen", save_config, save_progress=save_progress, auto_unlock=True)
    def get_fullscreen(self): return self._fullscreen
    p_fullscreen = Property(QObject, get_fullscreen, notify=model_changed)
    
    _autoload = Setting(True, "Config/autoload", save_config, save_progress=save_progress, auto_unlock=True)
    def get_autoload(self): return self._autoload
    p_autoload = Property(QObject, get_autoload, notify=model_changed)
    
    _auto_replay = Setting(True, "Config/auto_replay", save_config, save_progress=save_progress, auto_unlock=True)
    def get_auto_replay(self): return self._auto_replay
    p_auto_replay = Property(QObject, get_auto_replay, notify=model_changed)
    
    
#------------------------------------------------------------------------------
    _ideas = Setting(0, "Progress/ideas", save_progress)
    def get_ideas(self): return self._ideas
    p_ideas = Property(QObject, get_ideas, notify=model_changed)
    
    _total_ideas = Setting(0, "Progress/total_ideas", save_progress)
    def get_total_ideas(self): return self._total_ideas
    p_total_ideas = Property(QObject, get_total_ideas, notify=model_changed)    
    
    _game_progress = Setting(0, "Progress/game_progress", save_progress)
    def get_game_progress(self): return self._game_progress
    p_game_progress = Property(QObject, get_game_progress, notify=model_changed)
    
    _time_listened = Setting(0, "Progress/time_listened", save_progress, auto_unlock=True)
    def get_time_listened(self): return self._time_listened
    p_time_listened = Property(QObject, get_time_listened, notify=model_changed)
    
#------------------------------------------------------------------------------
    _gui_playback = Setting(True, "GUI/gui_playback", save_progress)
    def get_gui_playback(self): return self._gui_playback
    p_gui_playback = Property(QObject, get_gui_playback, notify=model_changed)
    
    _gui_back_to_mainmenu = Setting(True, "GUI/gui_back_to_mainmenu", save_progress)
    def get_gui_back_to_mainmenu(self): return self._gui_back_to_mainmenu
    p_gui_back_to_mainmenu = Property(QObject, get_gui_back_to_mainmenu, notify=model_changed)
    
#------------------------------------------------------------------------------
    _frequency = Setting(False, "Music/frequency", save_progress) # TODO: Split
    def get_frequency(self): return self._frequency
    p_frequency = Property(QObject, get_frequency, notify=model_changed)
    
    _faster = Setting(False, "Music/faster", save_progress, rightOf=_frequency, dependencies=[_frequency])
    def get_faster(self): return self._faster
    p_faster = Property(QObject, get_faster, notify=model_changed)
    
    _slower = Setting(False, "Music/slower", save_progress, rightOf=_faster, dependencies=[_frequency])
    def get_slower(self): return self._slower
    p_slower = Property(QObject, get_slower, notify=model_changed)
    
    _less_random_test = Setting(False, "Music/less_random_test", save_progress, leftOf=_frequency, dependencies=[_frequency])
    def get_less_random_test(self): return self._less_random_test
    p_less_random_test = Property(QObject, get_less_random_test, notify=model_changed)
    
    _ternary_rythmn = Setting(False, "Music/ternary_rythmn", save_progress, leftOf=_less_random_test, dependencies=[_frequency])
    def get_ternary_rythmn(self): return self._ternary_rythmn
    p_ternary_rythmn = Property(QObject, get_ternary_rythmn, notify=model_changed)
    
    _scales = Setting(False, "Music/scales", save_progress, over=_frequency, dependencies=[_frequency])
    def get_scales(self): return self._scales
    p_scales = Property(QObject, get_scales, notify=model_changed)
    
    _chords = Setting(False, "Music/chords", save_progress, leftOf=_scales, dependencies=[_scales])
    def get_chords(self): return self._chords
    p_chords = Property(QObject, get_chords, notify=model_changed)
    
    _chord_progression = Setting(False, "Music/chord_progression", save_progress, leftOf=_chords, dependencies=[_chords])
    def get_chord_progression(self): return self._chord_progression
    p_chord_progression = Property(QObject, get_chord_progression, notify=model_changed)
    
    _chord_progression2 = Setting(False, "Music/chord_progression2", save_progress, leftOf=_chord_progression, dependencies=[_chord_progression])
    def get_chord_progression2(self): return self._chord_progression2
    p_chord_progression2 = Property(QObject, get_chord_progression2, notify=model_changed)
    
    _progression_random_tension = Setting(False, "Music/progression_random_tension", save_progress, leftOf=_chord_progression2, dependencies=[_chord_progression])
    def get_progression_random_tension(self): return self._progression_random_tension
    p_progression_random_tension = Property(QObject, get_progression_random_tension, notify=model_changed)
    
    _more_same_notes = Setting(False, "Music/more_same_notes", save_progress, rightOf=_scales, dependencies=[_scales])
    def get_more_same_notes(self): return self._more_same_notes
    p_more_same_notes = Property(QObject, get_more_same_notes, notify=model_changed)
    
    _another_kind_of_random_notes = Setting(False, "Music/another_kind_of_random_notes", save_progress, over=_scales, dependencies=[_scales])
    def get_another_kind_of_random_notes(self): return self._another_kind_of_random_notes
    p_another_kind_of_random_notes = Property(QObject, get_another_kind_of_random_notes, notify=model_changed)
    
    _another_kind_of_random_duration = Setting(False, "Music/another_kind_of_random_duration", save_progress, rightOf=_another_kind_of_random_notes, dependencies=[_scales])
    def get_another_kind_of_random_duration(self): return self._another_kind_of_random_duration
    p_another_kind_of_random_duration = Property(QObject, get_another_kind_of_random_duration, notify=model_changed)
    
    _test_jazz_scales = Setting(False, "Music/test_jazz_scales", save_progress, leftOf=_another_kind_of_random_notes, over=_another_kind_of_random_notes, dependencies=[_scales])
    def get_test_jazz_scales(self): return self._test_jazz_scales
    p_test_jazz_scales = Property(QObject, get_test_jazz_scales, notify=model_changed)
    
    _instruments = Setting(False, "Music/instruments", save_progress, under=_frequency)
    def get_instruments(self): return self._instruments
    p_instruments = Property(QObject, get_instruments, notify=model_changed)
    
    _instrument_percussions = Setting(False, "Music/instrument_percussions", save_progress, under=_instruments, dependencies=[_instruments])
    def get_instrument_percussions(self): return self._instrument_percussions
    p_instrument_percussions = Property(QObject, get_instrument_percussions, notify=model_changed)
    
    _instrument_piano = Setting(False, "Music/instrument_piano", save_progress, under=_instrument_percussions, dependencies=[_instruments])
    def get_instrument_piano(self): return self._instrument_piano
    p_instrument_piano = Property(QObject, get_instrument_piano, notify=model_changed)
    
    _instrument_piano_electric = Setting(False, "Music/instrument_piano_electric", save_progress, leftOf=_instrument_piano, dependencies=[_instruments])
    def get_instrument_piano_electric(self): return self._instrument_piano_electric
    p_instrument_piano_electric = Property(QObject, get_instrument_piano_electric, notify=model_changed)
    
    _instrument_chromatic_percussion = Setting(False, "Music/instrument_chromatic_percussion", save_progress, leftOf=_instrument_percussions, dependencies=[_instruments])
    def get_instrument_chromatic_percussion(self): return self._instrument_chromatic_percussion
    p_instrument_chromatic_percussion = Property(QObject, get_instrument_chromatic_percussion, notify=model_changed)
    
    _instrument_organ = Setting(False, "Music/instrument_organ", save_progress, rightOf=_instrument_piano, dependencies=[_instruments])
    def get_instrument_organ(self): return self._instrument_organ
    p_instrument_organ = Property(QObject, get_instrument_organ, notify=model_changed)
    
    _instrument_guitar = Setting(False, "Music/instrument_guitar", save_progress, under=_instrument_piano, dependencies=[_instruments])
    def get_instrument_guitar(self): return self._instrument_guitar
    p_instrument_guitar = Property(QObject, get_instrument_guitar, notify=model_changed)
    
    _instrument_guitar_electric = Setting(False, "Music/instrument_guitar_electric", save_progress, leftOf=_instrument_guitar, dependencies=[_instruments])
    def get_instrument_guitar_electric(self): return self._instrument_guitar_electric
    p_instrument_guitar_electric = Property(QObject, get_instrument_guitar_electric, notify=model_changed)
    
    _instrument_bass = Setting(False, "Music/instrument_bass", save_progress, rightOf=_instrument_guitar, dependencies=[_instruments])
    def get_instrument_bass(self): return self._instrument_bass
    p_instrument_bass = Property(QObject, get_instrument_bass, notify=model_changed)
    
    _instrument_bass_electric = Setting(False, "Music/instrument_bass_electric", save_progress, rightOf=_instrument_bass, dependencies=[_instruments])
    def get_instrument_bass_electric(self): return self._instrument_bass_electric
    p_instrument_bass_electric = Property(QObject, get_instrument_bass_electric, notify=model_changed)
    
    _instrument_strings = Setting(False, "Music/instrument_strings", save_progress, under=_instrument_guitar, dependencies=[_instruments])
    def get_instrument_strings(self): return self._instrument_strings
    p_instrument_strings = Property(QObject, get_instrument_strings, notify=model_changed)
    
    _instrument_brass = Setting(False, "Music/instrument_brass", save_progress, leftOf=_instrument_strings, dependencies=[_instruments])
    def get_instrument_brass(self): return self._instrument_brass
    p_instrument_brass = Property(QObject, get_instrument_brass, notify=model_changed)
    
    _instrument_ensemble = Setting(False, "Music/instrument_ensemble", save_progress, leftOf=_instrument_brass, dependencies=[_instruments])
    def get_instrument_ensemble(self): return self._instrument_ensemble
    p_instrument_ensemble = Property(QObject, get_instrument_ensemble, notify=model_changed)
    
    _instrument_reed = Setting(False, "Music/instrument_reed", save_progress, rightOf=_instrument_strings, dependencies=[_instruments])
    def get_instrument_reed(self): return self._instrument_reed
    p_instrument_reed = Property(QObject, get_instrument_reed, notify=model_changed)
    
    _instrument_free_reed = Setting(False, "Music/instrument_free_reed", save_progress, rightOf=_instrument_reed, dependencies=[_instruments])
    def get_instrument_free_reed(self): return self._instrument_free_reed
    p_instrument_free_reed = Property(QObject, get_instrument_free_reed, notify=model_changed)
    
    _instrument_pipe = Setting(False, "Music/instrument_pipe", save_progress, rightOf=_instrument_free_reed, dependencies=[_instruments])
    def get_instrument_pipe(self): return self._instrument_pipe
    p_instrument_pipe = Property(QObject, get_instrument_pipe, notify=model_changed)
    
    _instrument_synth_lead = Setting(False, "Music/instrument_synth_lead", save_progress, under=_instrument_strings, dependencies=[_instruments])
    def get_instrument_synth_lead(self): return self._instrument_synth_lead
    p_instrument_synth_lead = Property(QObject, get_instrument_synth_lead, notify=model_changed)
    
    _instrument_synth_pad = Setting(False, "Music/instrument_synth_pad", save_progress, leftOf=_instrument_synth_lead, dependencies=[_instruments])
    def get_instrument_synth_pad(self): return self._instrument_synth_pad
    p_instrument_synth_pad = Property(QObject, get_instrument_synth_pad, notify=model_changed)
    
    _instrument_synth_effects = Setting(False, "Music/instrument_synth_effects", save_progress, leftOf=_instrument_synth_pad, dependencies=[_instruments])
    def get_instrument_synth_effects(self): return self._instrument_synth_effects
    p_instrument_synth_effects = Property(QObject, get_instrument_synth_effects, notify=model_changed)
    
    _instrument_ethnic = Setting(False, "Music/instrument_ethnic", save_progress, rightOf=_instrument_synth_lead, dependencies=[_instruments])
    def get_instrument_ethnic(self): return self._instrument_ethnic
    p_instrument_ethnic = Property(QObject, get_instrument_ethnic, notify=model_changed)
    
    _instrument_sound_effects = Setting(False, "Music/instrument_sound_effects", save_progress, rightOf=_instrument_ethnic, dependencies=[_instruments])
    def get_instrument_sound_effects(self): return self._instrument_sound_effects
    p_instrument_sound_effects = Property(QObject, get_instrument_sound_effects, notify=model_changed)
    
    
    # TODO: int, sub setting??
    _bass_tracks = Setting(False, "Music/bass_tracks", save_progress, rightOf=_instruments, dependencies=[_instruments])
    def get_bass_tracks(self): return self._bass_tracks
    p_bass_tracks = Property(QObject, get_bass_tracks, notify=model_changed)
    
    _multi_instruments = Setting(False, "Music/multi_instruments", save_progress, rightOf=_bass_tracks, dependencies=[_bass_tracks])
    def get_multi_instruments(self): return self._multi_instruments
    p_multi_instruments = Property(QObject, get_multi_instruments, notify=model_changed)
    