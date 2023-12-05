# -*- mode: python ; coding: utf-8 -*-
# Cài pyinstaller
# Chạy pyinstaller Signify.spec

from kivy_deps import sdl2, glew, gstreamer

from kivymd import hooks_path as kivymd_hooks_path

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ('assets','assets'),
        ('local','local'),
        ('kvfiles','kvfiles'),
        ('local','local'),
        ('model','model')
        ],
    hiddenimports=[],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Signify',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + gstreamer.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Signify',
)
