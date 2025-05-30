# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs
import glob
import os

block_cipher = None
# 收集动态库
binaries = collect_dynamic_libs('onnxruntime', destdir='onnxruntime/capi')

# 获取所有模块文件
module_base_files = glob.glob(os.path.join('modules', 'base', '*.py'))
module_genshin_files = glob.glob(os.path.join('modules', 'genshin', '*.py'))
module_starRail_files = glob.glob(os.path.join('modules', 'starRail', '*.py'))
module_zzz_files = glob.glob(os.path.join('modules', 'zzz', '*.py'))

# 数据文件和配置文件
datas = [
    ('venv/Lib/site-packages/rapidocr_onnxruntime/config.yaml', 'rapidocr_onnxruntime'),
    ('venv/Lib/site-packages/rapidocr_onnxruntime/models', 'rapidocr_onnxruntime/models'),
    ('src', 'src')
]

# 合并所有模块文件
all_modules = ['main.py'] + module_base_files + module_genshin_files + module_starRail_files + module_zzz_files

a = Analysis(
    all_modules,
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='评分工具',
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
    icon='src/keqing.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ratingTools-0.0.14'
)
