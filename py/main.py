import midi_builder
import pygame_midi

#------------------------------------------------------------------------------
def main() -> None:
    filename = "output.mid"
    midi_builder.make_midi(filename)
    
    pygame_midi.init(2)
    print("Play!")
    pygame_midi.play(filename)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

