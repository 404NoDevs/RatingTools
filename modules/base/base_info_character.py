import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QColor, QStandardItem
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTableView
)


class BaseInfoCharacterWindow(QWidget):
    def __init__(self, params):
        super().__init__()
        # 初始化子类参数
        self.data = params.get("data")
        self.position = params.get("position", (0, 0))
        self.size = params.get("size", (0, 0))

        # 初始化参数
        self.table_view = None

        # 初始化UI
        self.initUI()
        self.update()

    def initUI(self):
        self.setWindowFlags(Qt.Window)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../../src/keqing.ico')))
        self.setWindowTitle("角色装备信息")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(*self.position)
        self.resize(*self.size)

        layout = QGridLayout()
        self.setLayout(layout)
        self.table_view = QTableView()
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        self.table_view.setSortingEnabled(True)
        layout.addWidget(self.table_view)

    def update(self):
        pass

