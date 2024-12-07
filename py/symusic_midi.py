import os
import shutil
import logging
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
        self.thread = thread
        
#------------------------------------------------------------------------------
    def debug_audio(self, audio):        
        for i, p in enumerate(audio):                
            if p:
                logger.debug(f"{i}, {p}")
            if i == 100:
                break
                
#------------------------------------------------------------------------------
    def normalize_stereo_audio(self, audio, verbose):      
        left = audio[0]
        right = audio[1]
        if verbose:
            self.debug_audio(left)
        max_value = max(abs(max(left, key=abs)),abs(max(right, key=abs)))

        a = 0.99 / max_value
        if a < 0.1:
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
        assert(os.path.isfile(wav_filename))
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
    def midi_to_wav(self, normalize=True, verbose=False, to_mp3=True):        
        filename = self.filename
        
        mp3_filename = fh.tempfile_path(filename, ".mp3")
        wav_filename = fh.tempfile_path(filename, ".wav")
        
        
        if os.path.isfile(mp3_filename) and not self.force_gen:
            self.out_filename = mp3_filename
            logger.info(f"-- Using mp3 {mp3_filename}")
            return self.out_filename
            
        
        self.out_filename = wav_filename
        if os.path.isfile(wav_filename) and not self.force_gen:
            if to_mp3:
                self.out_filename = self.wav_to_mp3(wav_filename, mp3_filename)
            logger.info(f"-- Using existing {self.out_filename}")
            return self.out_filename
        
        
        if os.path.isfile(self.out_filename):
            os.remove(self.out_filename)
           
        if normalize:
            i = 0
            audio = self._synth_from_path(filename)
            
            while not self.normalize_stereo_audio(audio, verbose):
                i += 1
                del audio
                if i >= 1: #TODO: Always same results when it fails? why??
                    logger.warning("FAILED, fallback to mid")
                    self.out_filename = self.filename
                    return self.out_filename
                audio = self._synth_from_path(filename)
        else:
            audio = self._synth_from_path(filename)
        
        
        # you could also dump the wave to a file
        # use_int16 is True by default, which means the output wave is int16, otherwise float32
        dump_wav(self.out_filename, audio, sample_rate=44100, use_int16=False)
        del audio
        audio = None
        
        
        if to_mp3 and not self.force_gen:
            self.out_filename = self.wav_to_mp3(wav_filename, mp3_filename)    
        
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
def midi_to_wav_worker(worker, thread, filename, parent=None, force_gen=False):
    worker.filename = filename
    worker.force_gen = force_gen
    thread.start()

#------------------------------------------------------------------------------
def midi_to_wav_async(filename, parent):
    worker = Worker(filename)
    midi_to_wav_worker(worker, filename, parent=parent)
