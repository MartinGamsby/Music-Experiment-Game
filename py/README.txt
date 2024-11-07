# Generating MIDI help

Thank you medium.com/@stevehiehn/how-to-generate-music-with-python-the-basics-62e8ea9b99a5

# Playing MIDI help

https://www.reddit.com/r/Python/comments/1032r08/i_made_a_soundfont_midi_synthesizer/
https://musescore.org/en/handbook/3/soundfonts-and-sfz-files#gm_soundfonts
(MuseScore_General.sf3)


# If we want to add assets (images):
from https://doc.qt.io/qtforpython-6/tutorials/basictutorial/qrcfiles.html
pyside6-rcc assets/resources.qrc -o rc_resources.py

The qml files are NOT in the qrc file, because it causes issues with debugging/developping.
And instead of finding the perfect way to do that, just bundle the qml files in the installer and access them directly.

Same thing for the mp3 file, but it's because Qt doesn't play sounds in Qt apparently.

# translation

pyside6-lupdate ui/main.qml ui/controls/Splash.qml ui/controls/MainMenu.qml -ts lang/t1_fr.ts lang/t1_en.ts
...
(TODO: for all qml files?)

pyside6-linguist lang/t1_fr.ts lang/t1_en.ts

pyside6-lrelease lang/t1_fr.ts lang/t1_en.ts


## Installer
pyinstaller MusicExperimentGame.spec
-> onefile exe in dist folder
