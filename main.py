import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QApplication
)

from globalsData import *
from utils import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'src/keqing.ico')))
        self.setWindowTitle(appName)
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(0, 0)

        self.initUI()

    def initUI(self):

        # 初始化UI
        maxWidth = 20
        layout = QGridLayout()
        # 标题
        title = QLabel(appName)
        title.setFont(QFont('微软雅黑', 30, QFont.Bold))
        title.setStyleSheet("qproperty-alignment: 'AlignCenter';")
        layout.addWidget(title, 0, 0, 1, maxWidth)
        # 游戏按钮
        counter = 1
        gameBtns = {}
        for gamekey, gameName in gamesMap.items():
            btnItem = QPushButton(gameName)
            btnItem.clicked.connect(self.onClickGameBtn)
            layout.addWidget(btnItem, counter, 0, 1, maxWidth)
            gameBtns[gamekey] = btnItem
            counter += 1

        # 提示文本
        self.tipsLabel = QLabel('请选择游戏')
        self.tipsLabel.setStyleSheet("qproperty-alignment: 'AlignCenter';color:red;")
        layout.addWidget(self.tipsLabel, 100, 0, 1, maxWidth)

        # layout载入widget中
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def onClickGameBtn(self):
        sender_button = self.sender()  # 获取发送信号的按钮对象
        gameName = sender_button.text()
        gameKey = getKeyByValue(gamesMap, gameName)

        global mainWindow
        window_state = checkWinowState(gameKey)
        if window_state == 0:
            ScoreWindow = None
            if gameKey == "genshin":
                from modules.genshin.genshin_score import ScoreWindow
            elif gameKey == "starRail":
                from modules.starRail.starRail_score import ScoreWindow
            elif gameKey == "zzz":
                from modules.zzz.zzz_score import ScoreWindow
            else:
                self.tipsLabel.setText(f"{gameName} 模块正在施工")

            if ScoreWindow:
                mainWindow = ScoreWindow()
                mainWindow.initParams()
                mainWindow.show()
                self.close()
        elif window_state == 1:
            SuitWindow = None
            if gameKey == "genshin":
                from modules.genshin.genshin_suit import SuitWindow
            elif gameKey == "starRail":
                from modules.starRail.starRail_suit import SuitWindow
            elif gameKey == "zzz":
                from modules.zzz.zzz_suit import SuitWindow
            else:
                self.tipsLabel.setText(f"{gameName} 模块正在施工")

            if SuitWindow:
                mainWindow = SuitWindow({
                    "enterParam": 1
                })
                mainWindow.show()
                self.close()
        elif window_state == 2:
            self.tipsLabel.setText("请将游戏窗口调整为1920*1080")

def main():
    # 任务栏图标问题
    try:
        from ctypes import windll  # Only exists on Windows.
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(version)
    except ImportError:
        pass

    app = QApplication(sys.argv)
    # 设置样式
    app.setStyle("WindowsVista")
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
