# TODO: async init
#import midi_builder
#import pygame_midi

import sys

import backend as bak
import model

import rc_resources

#------------------------------------------------------------------------------
def main() -> None:

    backend = bak.Backend( qml_file="main.qml", model=model.Model() )
    sys.exit(backend.run())
    
    #TODO:
    #filename = "output.mid"
    #midi_builder.make_midi(filename)
    #
    #pygame_midi.init(2)
    #print("Play!")
    #pygame_midi.play(filename)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

