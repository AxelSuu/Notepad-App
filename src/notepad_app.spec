# -*- mode: python ; coding: utf-8 -*-

import os
import sys
block_cipher = None

# Get the absolute path using the current working directory instead of __file__
base_path = os.getcwd()

# Get the src path
src_path = os.path.join(base_path, "src") if os.path.exists(os.path.join(base_path, "src")) else base_path

# Define data files to be included
datas = []

# Add fonts
font_path = os.path.join(base_path, "assets", "fonts")
if os.path.exists(font_path):
    datas.append((font_path, "assets/fonts"))

# Add images
img_path = os.path.join(base_path, "assets", "imgs")
if os.path.exists(img_path):
    datas.append((img_path, "assets/imgs"))

# Check both locations for the icon file
icon_path = None
possible_icon_paths = [
    os.path.join(base_path, 'icon.ico'),           # Base directory
    os.path.join(src_path, 'icon.ico'),            # src directory
    os.path.join(base_path, 'src', 'icon.ico')     # src subdirectory
]

for path in possible_icon_paths:
    if os.path.exists(path):
        icon_path = path
        print(f"Found icon at: {icon_path}")
        break

if not icon_path:
    print("Warning: Icon file not found in any of the expected locations!")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,  # Use our collected data files
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Notepad App',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    icon=icon_path
)