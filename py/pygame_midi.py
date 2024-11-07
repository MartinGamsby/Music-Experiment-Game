import pygame
from threading import Thread, Lock

mutex = Lock()

# TODO: Better than that...
music = None

#------------------------------------------------------------------------------
def stop_music():
    if is_init():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        
        global music
        if music:
            music.stop()

        with mutex:
            pass # Wait for _play_music to end
    
#------------------------------------------------------------------------------
def _play_music(music_file, cb, use_sound=False):#True):#Ugh, with sound it's still lagging? Why??. I can get the length, but not play mid files...
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    
    if use_sound:
        global music
        music = pygame.mixer.Sound(music_file)
        length = music.get_length()
        length_ms = length*1000.
        print("length", length)
        c = music.play()
        print(c, c.get_busy())
        
        #print(dir(pygame.mixer.Sound))
        
        total_ms = 0
        cb(0,length_ms)
        while pygame.mixer.get_busy():
            clock.tick(30)
            t = clock.get_time() + clock.tick_busy_loop()
            total_ms += t
            cb(total_ms,length_ms)
            if total_ms > length_ms:
                break
        del music
        music = None
        return
        
    try:
        pygame.mixer.music.load(music_file)
        print( "Music file %s loaded!" % music_file )
    except pygame.error:
        print( "File %s not found! (%s)" % (music_file, pygame.get_error()) )
        return        
        
    try:
        music = pygame.mixer.Sound(music_file)
        length_ms = music.get_length()*1000 #Doesn't even work for midi files, so...
    except:
        from mido import MidiFile
        mid = MidiFile(music_file)
        length_ms = mid.length*1000

    music = None
    pygame.mixer.music.play()
    
        
    total_ms = 0
    while pygame.mixer.music.get_busy():
        clock.tick(30)
        t = clock.get_time() + clock.tick_busy_loop()
        total_ms += t
        cb(total_ms,length_ms)
        if total_ms > length_ms:
            break
        
        
# pick a midi music file you have ...
# (if not in working folder use full path)

#------------------------------------------------------------------------------
def init(channels=2):# 1 is mono, 2 is stereo
    with mutex:
        if not is_init():
            freq = 44100    # audio CD quality
            bitsize = -16   # unsigned 16 bit
            buffer = 1024    # number of samples
            pygame.mixer.init(freq, bitsize, channels, buffer)
            
#------------------------------------------------------------------------------
def is_init():
    return pygame.mixer.get_init() != None

#------------------------------------------------------------------------------
def play(midi_file, cb, volume=1.0):
    
    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(volume)
    try:
        with mutex:
            _play_music(midi_file, cb)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
        
        