call qtstuff.bat
python ut.py
pause 1
pyinstaller MusicExperimentGame.spec --noconfirm
pause 1
"dist/MusicExperimentGame/MusicExperimentGame.exe"