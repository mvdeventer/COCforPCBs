# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for COC Report Generator
Builds standalone executable with all dependencies
"""

import sys
from pathlib import Path

block_cipher = None

# Get version from git or use default
import subprocess
try:
    version = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'],
                                      text=True, stderr=subprocess.DEVNULL).strip()
    version = version.lstrip('v')
except:
    version = '1.0.0'

a = Analysis(
    ['generate_coc_report.py'],
    pathex=[],
    binaries=[],
    datas=[item for item in [
        ('README.md', '.') if Path('README.md').exists() else None,
        ('CHANGELOG.md', '.') if Path('CHANGELOG.md').exists() else None,
    ] if item is not None],
    hiddenimports=[
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.cell._writer',
        'pandas',
        'PyPDF2',
        'docx',
        'fitz',
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'numpy.distutils',
        'tkinter.test',
    ],
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
    name='COC_Report_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='company_logo.ico' if Path('company_logo.ico').exists() else None,
    version_file='version_info.txt',
)
