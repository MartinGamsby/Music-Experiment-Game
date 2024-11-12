# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=[''],
    		 binaries=[('C:\\Users\\Martin\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\symusic\\bin\\*.exe','symusic\\bin'),('ffmpeg.exe', '.'),('ffprobe.exe', '.')],
             datas=[('ui\\main.qml', 'ui'),('ui\\controls\\*.qml', 'ui\\controls'),('lang\\*.qm', 'lang'),('assets\\*.mid', 'assets'),('assets\\*.sf3', 'assets')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='MusicExperimentGame',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='MusicExperimentGame')
