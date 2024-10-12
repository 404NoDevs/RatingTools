'''圣遗物推荐方案生成弹窗'''

import os
from itertools import zip_longest

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QGridLayout
)


class BaseAnalyzeResultWindow(QWidget):

    def __init__(self, params):
        super().__init__()

        self.position = params.get("position", (0, 322))
        self.analyzeResult = params.get("analyzeResult", {})

        self.labelPool = []
        # 初始化UI
        self.initUI()
        self.updateUI()

    def update(self):
        pass

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../../src/keqing.ico')))
        self.setWindowTitle("分析结果")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(*self.position)

        # 创建界面UI
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("适用方向"), 0, 0, 1, 1)
        layout.addWidget(QLabel("适合角色"), 0, 1, 1, 1)
        layout.addWidget(QLabel("有效词条"), 0, 2, 1, 1)
        layout.addWidget(QLabel("得分"), 0, 3, 1, 1)


    def updateUI(self):
        for item, label in zip_longest(self.analyzeResult, self.labelPool, fillvalue=None):
            if label is None:
                
                pass


