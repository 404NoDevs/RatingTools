import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTableView
)


class BaseInfoWindow(QWidget):

    def __init__(self, params):
        super().__init__()
        # 子类参数
        self.data = params.get("data")
        self.position = params.get("position", (0, 0))
        self.size = params.get("size", (0, 0))

        # 初始化UI
        self.initUI()
        self.update()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../../src/keqing.ico')))
        self.setWindowTitle("装备信息")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(*self.position)
        self.resize(*self.size)

        layout = QGridLayout()
        self.setLayout(layout)
        self.table_view = QTableView()
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        self.table_view.resizeRowsToContents()  # 根据内容调整行高
        self.table_view.resizeColumnsToContents()  # 根据内容调整列宽
        self.table_view.setSortingEnabled(True)
        layout.addWidget(self.table_view)

    def update(self):
        pass
