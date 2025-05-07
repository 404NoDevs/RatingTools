@echo off
chcp 65001 > nul
echo 正在创建Python虚拟环境...
python -m venv venv || (
    echo 创建虚拟环境失败，请确保已安装Python
    pause
    exit /b 1
)

echo 激活虚拟环境并安装依赖...
call venv\Scripts\activate && (
    python -m pip install --upgrade ^
    pip ^
    setuptools ^
    wheel ^
    PySide6 ^
    pyperclip ^
    pynput ^
    pywin32 ^
    pyqtdarktheme ^
    rapidocr-onnxruntime ^
    onnxruntime-directml ^
    requests || (
        echo 依赖安装失败
        pause
        exit /b 1
    )
    echo 环境部署完成!
    pause
)