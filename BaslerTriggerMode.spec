# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import pypylon
import pathlib
pypylon_dir = pathlib.Path(pypylon.__file__).parent
pylon_dlls = [(str(dll), '.') for dll in pypylon_dir.glob('*.dll')]

a = Analysis(['BaslerTriggerMode.py'],
             pathex=['D:\\Duc\\Code\\Vision\\Modules\\Camera'],
             binaries=pylon_dlls,
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='BaslerTriggerMode',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None)
