import PyInstaller.__main__
from pathlib import Path
import shutil
import os

new_version = "0.0.0"
# 读取当前版本
version_file = "globalsData.py"
with open(version_file, encoding='utf-8') as f:
    version_content = f.readlines()
# 版本号增加
new_version_content = []
for line in version_content:
    if line.startswith('version ='):
        version = line.split('=')[1].strip().strip('"')  # 获取当前版本号
        version_parts = version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)  # 增加最后一位
        new_version = '.'.join(version_parts)
        new_version_content.append(f'version = "{new_version}"\n')  # 更新版本号
    else:
        new_version_content.append(line)  # 保持其他行不变
# 写回文件
with open(version_file, 'w', encoding='utf-8') as f:
    f.writelines(new_version_content)

new_name = f'ratingTools-{new_version}'
# 将新版本号写入build.spec
config_file = "build.spec"
with open(config_file, 'r', encoding='utf-8') as f:
    config_content = f.readlines()
new_config_content = []
for line in config_content:
    if "name='ratingTools" in line:
        new_config_content.append(f"    name='{new_name}'\n")
    else:
        new_config_content.append(line)  # 保持其他行不变
with open(config_file, 'w', encoding='utf-8') as f:
    f.writelines(new_config_content)


def copy_file(src: str, dst: str):
    # 将文件或目录拷贝到指定位置
    src_path = Path(src)
    dst_path = Path(dst)

    # 如果目标是目录，保留原文件名/目录名
    if dst_path.is_dir():
        dst_path = dst_path / src_path.name

    # 执行拷贝
    if src_path.is_file():
        shutil.copy(src_path, dst_path)
    elif src_path.is_dir():
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
    print(f"已拷贝到: {dst_path}")

def build_success_callback():
    # 在这里添加你的回调逻辑
    path = Path.cwd() / "dist" / new_name
    src_path = path / "_internal" / "src"
    copy_file(src_path, path)

try:
    PyInstaller.__main__.run([
        'build.spec'
    ])
    build_success_callback()
except Exception as e:
    print(f"构建失败: {e}")