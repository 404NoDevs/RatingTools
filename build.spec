# -*- mode: python ; coding: utf-8 -*-


from PyInstaller.utils.hooks import collect_dynamic_libs
import glob
import os

new_content = []
new_version = "0.0.0"
# 读取当前版本
version_file = "globalsData.py"
with open(version_file, encoding='utf-8') as f:
    content = f.readlines()

# 版本号增加
for line in content:
    if line.startswith('version ='):
        version = line.split('=')[1].strip().strip('"')  # 获取当前版本号
        version_parts = version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)  # 增加最后一位
        new_version = '.'.join(version_parts)
        new_content.append(f'version = "{new_version}"\n')  # 更新版本号
    else:
        new_content.append(line)  # 保持其他行不变

# 写回文件
with open(version_file, 'w', encoding='utf-8') as f:
    f.writelines(new_content)

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
    name='ratingTools-0.0.54'
)
