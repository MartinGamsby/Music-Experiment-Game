import os
import shutil

os.system("call qtstuff.bat")
os.system("python ut.py")
os.system("pyinstaller MusicExperimentGame.spec --noconfirm")


# Maybe remove from code: PIL
dirs = []
for d in ["torch", "torch-2.5.1.dist-info", "transformers", "tokenizers", "cv2", "matplotlib", "pandas", "pandas.lib", "safetensors"]:
    dirs.append(os.path.join("dist", "MusicExperimentGame", "_internal", d))

# I need avcodec for the video playback
for subdir in ["Qt6WebEngineCore.dll", "opengl32sw.dll", "Qt6Widgets.dll", "QtWidgets.pyd", "Qt6Pdf.dll", "translations"]:
    dirs.append(os.path.join("dist", "MusicExperimentGame", "_internal", "PySide6", subdir))

for f in dirs:
    try:
        if os.path.isfile(f):
            os.remove(f)
        else:
            shutil.rmtree(f)
    except OSError as e:
        pass#print("Error: %s - %s." % (e.filename, e.strerror))
    


os.system(os.path.join("dist", "MusicExperimentGame", "MusicExperimentGame.exe"))