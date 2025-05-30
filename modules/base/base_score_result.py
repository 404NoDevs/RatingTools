'''贴图窗口，显示单独的评分结果'''

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget


class BaseScoreResultWindow(QWidget):
    def __init__(self, params):
        super().__init__()

        # 获取子类参数
        self.location = params.get('location', {})

        # 初始化参数
        self.scale = self.location.getFitterScale()

        self.initUI()

    def initUI(self):
        # 设置贴图窗口属性：透明、无边框透明、置顶
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        # 贴图窗口内容
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel('Er!')
        # 字体大小
        font = self.label.font()
        font.setPointSize(9 * self.scale)
        self.label.setFont(font)
        self.label.setFixedSize(30 * self.scale, 20 * self.scale)
        self.label.setAlignment(Qt.AlignCenter)
        # qss = 'border-image: url(paste.png);'
        qss = 'background-color: rgb(255, 255, 255)'
        self.label.setStyleSheet(qss)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 快捷键Ctrl+Z关闭贴图窗口，需焦点在主窗口
        # self.shortcut = QShortcut(QKeySequence('Ctrl+Z'), self)
        # self.shortcut.activated.connect(self.close)

    def setLabel(self, text):
        self.label.setStyleSheet('background-color: rgb(255, 255, 255)')
        try:
            num = float(text)
            if num < 0:
                text = 'Er!'
                self.label.setStyleSheet('background-color: rgb(235, 85, 37)')
        except:
            pass
        self.label.setText(str(text))

    # 按键关闭/重置对应贴图窗口
    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Z:
    #         print('freshed')
    #         self.hide()

    # Ctrl+Z关闭窗口
    def close(self):
        self.hide()
