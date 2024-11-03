import os
from symusic import Score, Synthesizer, dump_wav#, BuiltInSF3
    
from PySide6.QtCore import QObject, Signal, QThread
# https://stackoverflow.com/questions/72737506/pyside6-qthread-still-freezing-main-gui


#------------------------------------------------------------------------------
class Worker(QObject):

    finished = Signal()
    progress = Signal(int)

#------------------------------------------------------------------------------
    def __init__(self, thread, filename=""):
        super().__init__()
        self.filename = filename
        self.thread = thread
        
#------------------------------------------------------------------------------
    def debug_audio(self, audio):        
        for i, p in enumerate(audio):                
            if p:
                print(i, p)
            if i == 100:
                break
                
#------------------------------------------------------------------------------
    def normalize_stereo_audio(self, audio, verbose):      
        left = audio[0]
        right = audio[1]
        if verbose:
            self.debug_audio(left)
        max_value = 0.0

        for t in range(len(left)):
            if abs(left[t]) > max_value:
                max_value = abs(left[t])

            if abs(right[t]) > max_value:
                max_value = abs(right[t])

        if max_value < 1.0:
            a = 0.99 / max_value
            print("Normalizing audio by amplifying %.01fx" % a)
            audio *= a
            if verbose:
                print(a, max_value)
                self.debug_audio(left)  
                
                
#------------------------------------------------------------------------------
    def midi_to_wav(self, normalize=True, verbose=False):
        self.out_filename = "out.wav"
        filename = self.filename
        
        if os.path.isfile(self.out_filename):
            os.remove(self.out_filename)
           
        s = Score(filename)

        # You could choose a builtin soundfont
        # And the following one is the default soundfont if you don't specify it when creating a synthesizer
        sf_path = "assets/MuseScore_General.sf3"#BuiltInSF3.MuseScoreGeneral().path(download=True)

        synth = Synthesizer(
            sf_path = sf_path, # the path to the soundfont
            sample_rate = 44100, # the sample rate of the output wave, 44100 is the default value
        )

        # audio is a 2D numpy array of float32, [channels, time]
        audio = synth.render(s, stereo=True) # stereo is True by default, which means you will get a stereo wave
        
        if normalize:
            self.normalize_stereo_audio(audio, verbose)
        
        # you could also dump the wave to a file
        # use_int16 is True by default, which means the output wave is int16, otherwise float32
        dump_wav(self.out_filename, audio, sample_rate=44100, use_int16=True)
        return self.out_filename
    
#------------------------------------------------------------------------------
    def run(self):
        self.midi_to_wav()        
        self.finished.emit()
        
        
#------------------------------------------------------------------------------
def midi_to_wav(filename):
    return Worker(filename, thread=None).midi_to_wav()

#------------------------------------------------------------------------------
def midi_to_wav_worker(worker, thread, filename, parent=None):
    worker.filename = filename
    thread.start()

#------------------------------------------------------------------------------
def midi_to_wav_async(filename, parent):
    worker = Worker(filename)
    midi_to_wav_worker(worker, filename, parent=parent)
