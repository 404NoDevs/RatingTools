# -*- mode: python ; coding: utf-8 -*-


from PyInstaller.utils.hooks import collect_dynamic_libs
import glob
import os

# 读取当前版本
version_file = "globalsData.py"
with open(version_file, encoding='utf-8') as f:
    exec(f.read())

# 版本号增加
version_parts = version.split('.')
version_parts[-1] = str(int(version_parts[-1]) + 1)  # 只增加最后一位
new_version = '.'.join(version_parts)

# 更新版本号到文件
with open(version_file, 'w') as f:
    f.write(f'__version__ = "{new_version}"\n')

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
    ('src', 'src'),
    ('modules/genshin/config', 'module/genshin/config'),
    ('modules/starRail/config', 'module/starRail/config'),
    ('modules/zzz/config', 'module/zzz/config'),
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
    name=f'ratingTools-{new_version}',
)
