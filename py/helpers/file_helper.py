import os

#------------------------------------------------------------------------------
def get_appdata_folder(subfolder=""):
    
    folder="GamesByGamsby"
    
    appdata_main_folder = os.path.join( os.getenv('LOCALAPPDATA'), folder)
    if not os.path.isdir(appdata_main_folder):
        os.makedirs(appdata_main_folder)
    
    if subfolder:
        appdata_sub_folder = os.path.join( appdata_main_folder, subfolder)
        if not os.path.isdir(appdata_sub_folder):
            os.makedirs(appdata_sub_folder)
        return appdata_sub_folder
    return appdata_main_folder
        
#------------------------------------------------------------------------------
def replace_extension(filename, new_extension):
    p, ext = os.path.splitext(filename)
    return p + new_extension
    
#------------------------------------------------------------------------------
def tempfile_path(filename, extension, subfolder="Music"):
    appdata_sub_folder = get_appdata_folder(subfolder)
    return os.path.join( appdata_sub_folder, replace_extension(os.path.basename(filename), extension))