import pygame

#------------------------------------------------------------------------------
def stop_music():
    if is_init():
        pygame.mixer.music.stop()
    
#------------------------------------------------------------------------------
def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print( "Music file %s loaded!" % music_file )
    except pygame.error:
        print( "File %s not found! (%s)" % (music_file, pygame.get_error()) )
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)
        
# pick a midi music file you have ...
# (if not in working folder use full path)

#------------------------------------------------------------------------------
def init(channels=2):# 1 is mono, 2 is stereo
    if not is_init():
        freq = 44100    # audio CD quality
        bitsize = -16   # unsigned 16 bit
        buffer = 1024    # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        
#------------------------------------------------------------------------------
def is_init():
    return pygame.mixer.get_init() != None

#------------------------------------------------------------------------------
def play(midi_file, volume=1.0):
    
    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(volume)
    try:
        play_music(midi_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
        
        