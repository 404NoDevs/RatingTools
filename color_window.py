import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter


class ColorWindow(QWidget):
    def __init__(self):
        super().__init__()

        # self.setWindowTitle("纯色窗口")
        # self.setGeometry(1000, 100, 100, 100)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # self.setAttribute(Qt.WA_TranslucentBackground)  # 允许背景透明
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.setWindowOpacity(0.5)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.color = QColor("lightblue")
        # self.setGeometry(1000, 100, 100, 100)


    def init_window(self, mark, x, y, w, h):
        # print(index, x, y, w, h)
        if mark % 2 == 0:
            self.color = QColor("lightblue")
        else:
            self.color = QColor("lightgreen")
        self.setGeometry(x, y, w, h)
        # self.setGeometry(0, 100, 100, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.color)  # 填充背景颜色
