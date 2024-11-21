import os
import pathlib

from PySide6.QtCore import QUrl

#------------------------------------------------------------------------------
def get_appdata_folder(subfolder=""):
    
    folder= os.path.join("GamesByGamsby", "MusicExperiment")
    
    appdata_main_folder = os.path.join( os.getenv('APPDATA'), folder)
    if not os.path.isdir(appdata_main_folder):
        os.makedirs(appdata_main_folder)
    
    if subfolder:
        appdata_sub_folder = os.path.join( appdata_main_folder, subfolder)
        if not os.path.isdir(appdata_sub_folder):
            os.makedirs(appdata_sub_folder)
        return appdata_sub_folder
    return appdata_main_folder
        
#------------------------------------------------------------------------------
def get_appdata_file(filename, subfolder=""):
    return os.path.join( get_appdata_folder(subfolder), filename)

#------------------------------------------------------------------------------
def replace_extension(filename, new_extension):
    if new_extension:
        p, ext = os.path.splitext(filename)
        return p + new_extension
    return filename
    
#------------------------------------------------------------------------------
def tempfile_path(filename, extension, subfolder="Music"):
    appdata_sub_folder = get_appdata_folder(subfolder)
    return os.path.join( appdata_sub_folder, replace_extension(os.path.basename(filename), extension))
    
#------------------------------------------------------------------------------
def abspath(filename): 
    """ This makes it work for both running .py and pyinstaller (and Qt stuff) """
    if not filename:
        return filename
    if os.path.isfile(filename):
        return filename    
    possible_filename = QUrl(filename).toLocalFile()
    
    if os.path.isfile(possible_filename):
        return possible_filename
    
    path = pathlib.Path(filename).resolve()
    path = path.resolve()
    if path.exists():
        return str(path)
            
    import sys
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = pathlib.Path(sys._MEIPASS).parent # To test
    else:
        bundle_dir = pathlib.Path(__file__).parent.parent
        
    return os.path.join(bundle_dir.resolve(), filename)
        