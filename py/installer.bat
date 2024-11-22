pyside6-rcc "assets/resources.qrc" -o rc_resources.py
pyside6-lrelease "lang/t1_fr.ts" "lang/t1_en.ts"
pause 1
pyinstaller MusicExperimentGame.spec
pause 1
"dist/MusicExperimentGame/MusicExperimentGame.exe"