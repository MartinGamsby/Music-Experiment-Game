import os
import time
import shutil
import logging
import threading
import helpers.file_helper as fh
from symusic import Score, Synthesizer, dump_wav#, BuiltInSF3
    
from PySide6.QtCore import QObject, Signal, QThread
# https://stackoverflow.com/questions/72737506/pyside6-qthread-still-freezing-main-gui

import logging
logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
class Worker(QObject):

    finished = Signal()
    progress = Signal(int)

#------------------------------------------------------------------------------
    def __init__(self, thread, filename=""):
        super().__init__()
        self.filename = filename
        self.force_gen = False
        self.progress_cb = None
        self.thread = thread
        
#------------------------------------------------------------------------------
    def debug_audio(self, audio):        
        for i, p in enumerate(audio):                
            if p:
                logger.info(f"{i}, {p}")
            if i == 100:
                break
                
#------------------------------------------------------------------------------
    def normalize_stereo_audio(self, audio, verbose):      
        left = audio[0]
        right = audio[1]
        if verbose:
            self.debug_audio(left)
        max_value = max(abs(max(left, key=abs)),abs(max(right, key=abs)))
        
        logger.info(f"Left: {len(left)} ({abs(max(left, key=abs))})")
        print(left)
        logger.info(f"Right: {len(right)} ({abs(max(right, key=abs))})")
        print(right)
        

        a = 0.99 / max_value
        if a < 0.01:
            logger.warning(f"Could not normalize audio by amplifying %.02fx (%.02f max)" % (a, max_value))
            return False
        logger.debug(f"Normalizing audio by amplifying %.02fx (%.02f max)" % (a, max_value))
        audio *= a
        if verbose:
            logger.debug(f"{a}, {max_value}")
            self.debug_audio(left)  
        return True
                
                
#------------------------------------------------------------------------------
    def _synth_from_path(self, score_filename, sf_path=fh.abspath("assets/MuseScore_General.sf3")):#BuiltInSF3.MuseScoreGeneral().path(download=True)
        score_filename = score_filename.replace("file:///","")#TODO: This is weird ... is there a better way?
        score = Score(score_filename)
        
        synth = Synthesizer(
            sf_path = sf_path, # the path to the soundfont
            sample_rate = 44100, # the sample rate of the output wave, 44100 is the default value
        )
        # return is a 2D numpy array of float32, [channels, time]
        audio = synth.render(score, stereo=True) # stereo is True by default, which means you will get a stereo wave
        #self.debug_audio(audio[0])
        del synth
        del score
        synth = None
        score = None
        return audio
               
#------------------------------------------------------------------------------
    def wav_to_mp3(self, wav_filename, mp3_filename):
        # NOTE: Does it need ffmpeg installed? Use ffmpeg python instead?
        logger.info(f"wav_to_mp3: {wav_filename} to {mp3_filename}")
        #if not os.path.isfile(wav_filename):
        #    raise Exception(f"{wav_filename} is not a file")
        try: # TODO: Add ffmpeg executable to the installer!!
            import pydub
            sound = pydub.AudioSegment.from_wav(wav_filename)            
            sound.export(mp3_filename, format="mp3")
            logger.info(f"converted {mp3_filename}")
            os.remove(wav_filename)
            return mp3_filename
        except:
            logger.warning("Failed to convert to mp3")
        return wav_filename
    
#------------------------------------------------------------------------------
    def audio_to_video(self, midi_filename, audio_filename, mp4_filename):
        logger.info(f"audio_to_video: {audio_filename} to {mp4_filename}")
        if True: # TODO: Setting
            try:
                from music.midi_render import create_video
                create_video(midi_filename, audio_filename, video_filename=mp4_filename,
                    image_width  = 512,
                    image_height = 192,
                    black_key_height = 2/3,
                    vertical_speed = 1/2,
                    fps = 30,
                    progress_cb = self.on_video_progress)
                logger.info(f"converted {audio_filename} to {mp4_filename}")
                os.remove(audio_filename)
                return mp4_filename
            except:
                logging.exception("run")
                logger.warning("failed to convert audio to video")
        return audio_filename
       
#------------------------------------------------------------------------------
    def add_progress(self, step):
        self.video_from_step += step
        self.on_progress(self.video_from_step)
    
#------------------------------------------------------------------------------
    def on_progress(self, step):
        if self.progress_cb != None:
            self.progress_cb(step)
            
#------------------------------------------------------------------------------
    def on_video_progress(self, step):
        max_step = 80
        self.on_progress(self.video_from_step+int(step*((max_step-self.video_from_step)/100)))
        
#------------------------------------------------------------------------------
    def thread_progress(self):
        i = 1
        while self.thread_running:
            for j in range(i):
                if self.thread_running:
                    time.sleep(0.001)
                    
            if self.video_from_step > 60:
                break
            self.add_progress(1)
            logger.debug(f"ADD PROGRESS: {self.video_from_step}")
            i *= 2
        
#------------------------------------------------------------------------------
    def stop_thread(self, thread):
        self.thread_running = False
        thread.join()

#------------------------------------------------------------------------------
    def midi_to_wav(self, normalize=True, verbose=False, to_mp3=True, to_mp4=True):        
        filename = self.filename
        
        self.video_from_step = 0
        self.add_progress(1)
        
        self.thread_running = True
        progress_thread = threading.Thread(target=self.thread_progress)
        progress_thread.start()
        
        try:
            mp3_filename = fh.tempfile_path(filename, ".mp3")
            wav_filename = fh.tempfile_path(filename, ".wav")
            mp4_filename = fh.tempfile_path(filename, ".mp4")
            
            if os.path.isfile(mp4_filename) and not self.force_gen:
                self.out_filename = mp4_filename
                logger.info(f"-- Using mp4 {mp4_filename}")
                self.stop_thread(progress_thread)
                return self.out_filename
                
            if os.path.isfile(mp3_filename) and not self.force_gen:
                self.out_filename = mp3_filename
                logger.info(f"-- Using mp3 {mp3_filename}")
                if to_mp4:            
                    self.stop_thread(progress_thread)
                    self.out_filename = self.audio_to_video(filename, self.out_filename, mp4_filename)
                self.stop_thread(progress_thread)
                return self.out_filename
                
            
            self.out_filename = wav_filename
            if os.path.isfile(wav_filename) and not self.force_gen:
                if to_mp3:
                    self.out_filename = self.wav_to_mp3(wav_filename, mp3_filename)
                    self.add_progress(10)
                if to_mp4:
                    self.stop_thread(progress_thread)
                    self.out_filename = self.audio_to_video(filename, self.out_filename, mp4_filename)
                logger.info(f"-- Using existing {self.out_filename}")
                self.stop_thread(progress_thread)
                return self.out_filename
            
            
            if os.path.isfile(self.out_filename):
                os.remove(self.out_filename)
               
            if normalize:
                i = 0
                audio = self._synth_from_path(filename)
                
                self.add_progress(5)
                self.normalize_stereo_audio(audio, verbose)
                
                self.add_progress(3)
            else:
                audio = self._synth_from_path(filename)
                self.on_progress(8)
            
            
            # you could also dump the wave to a file
            # use_int16 is True by default, which means the output wave is int16, otherwise float32
            dump_wav(self.out_filename, audio, sample_rate=44100, use_int16=False)
            self.add_progress(10)
            del audio
            audio = None
            self.add_progress(1)
            
            logger.info(f"to_mp3: {to_mp3}, to_mp4: {to_mp4}")
            if to_mp3:# and not self.force_gen:
                self.out_filename = self.wav_to_mp3(wav_filename, mp3_filename)
                self.add_progress(9)
                
            if to_mp4:
                self.stop_thread(progress_thread)
                self.out_filename = self.audio_to_video(filename, self.out_filename, mp4_filename)
        except:
            logger.exception("Failed to generate")
            self.stop_thread(progress_thread)
            raise Exception("Failed to generate")
            
        self.stop_thread(progress_thread)
    
        return self.out_filename
    
#------------------------------------------------------------------------------
    def run(self):
        try:
            self.midi_to_wav()
        except:
            logging.exception("run")
            logger.warning("failed to convert midi to wav")
            self.out_filename = ""
        self.finished.emit()
        
        
#------------------------------------------------------------------------------
def midi_to_wav(filename):
    return Worker(filename, thread=None).midi_to_wav()

#------------------------------------------------------------------------------
def midi_to_wav_worker(worker, thread, filename, parent=None, force_gen=False, progress_cb=None):
    worker.filename = filename
    worker.force_gen = force_gen
    worker.progress_cb = progress_cb
    thread.start()

#------------------------------------------------------------------------------
def midi_to_wav_async(filename, parent):
    worker = Worker(filename)
    midi_to_wav_worker(worker, filename, parent=parent)
