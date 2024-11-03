import os
from symusic import Score, Synthesizer, dump_wav#, BuiltInSF3
    
from PySide6.QtCore import QObject, Signal, QThread
# https://stackoverflow.com/questions/72737506/pyside6-qthread-still-freezing-main-gui


#------------------------------------------------------------------------------
class Worker(QObject):
    finished = Signal()
    progress = Signal(int)

#------------------------------------------------------------------------------
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        
#------------------------------------------------------------------------------
    def midi_to_wav(self):
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
    return Worker(filename).midi_to_wav()

#------------------------------------------------------------------------------
def midi_to_wav_async(filename):
    worker = Worker(filename)
    thread = QThread()
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    thread.start()
    thread.wait()
    return worker.out_filename

#------------------------------------------------------------------------------
#if __name__ == "__main__":
#    midi_to_wav()

