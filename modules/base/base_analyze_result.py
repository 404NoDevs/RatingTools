'''圣遗物推荐方案生成弹窗'''

import os
from itertools import zip_longest

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout
)


class BaseAnalyzeResultWindow(QWidget):

    def __init__(self, params):
        super().__init__()

        self.position = params.get("position", (0, 322))

        self.analyzeResult = []
        self.tips = "提示文本"
        self.labelPool = []
        # 初始化UI
        self.initUI()
        self.updateUI()

    def update(self, params):
        if params:
            self.analyzeResult = params.get("list", [])
            self.tips = params.get("tips", "提示文本")
            self.updateUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../../src/keqing.ico')))
        self.setWindowTitle("适用角色")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(*self.position)

        # 创建界面UI
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("适合角色"), 0, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("有效词条"), 0, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("得分"), 0, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("已装备词条"), 0, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("已装备得分"), 0, 4, 1, 1, Qt.AlignCenter)

        self.tipsLabel = QLabel("提示文本")
        self.tipsLabel.setStyleSheet("color:red;")
        self.layout.addWidget(self.tipsLabel, 100, 0, 1, 5, Qt.AlignCenter)

    def updateUI(self):
        for index, (item, label) in enumerate(zip_longest(self.analyzeResult, self.labelPool, fillvalue=None)):
            if label is None:
                label = self.creatLabelGroup(index)
                self.labelPool.append(label)
                self.setLabelGroup(label, item)
            elif item is None:
                self.setLabelGroupState(label, "hide")
            elif item and label:
                self.setLabelGroupState(label, "show")
                self.setLabelGroup(label, item)

        self.tipsLabel.setText(self.tips)

    def creatLabelGroup(self, index):
        labelGroup = {
            "nameLabel": QLabel(),  # 角色名字
            "entriesLabel1": QLabel(),  # 词条数量
            "scoreLabel1": QLabel(),  # 得分
            "entriesLabel2": QLabel(),  # 已装备词条数量
            "scoreLabel2": QLabel(),  # 已装备得分
        }
        self.layout.addWidget(labelGroup["nameLabel"], 1 + index, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(labelGroup["entriesLabel1"], 1 + index, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(labelGroup["scoreLabel1"], 1 + index, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(labelGroup["entriesLabel2"], 1 + index, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(labelGroup["scoreLabel2"], 1 + index, 4, 1, 1, Qt.AlignCenter)
        return labelGroup

    def setLabelGroup(self, labelGroup, item):
        labelGroup["nameLabel"].setText(item["name"])
        labelGroup["entriesLabel1"].setText(str(item["current_entries"]))
        labelGroup["scoreLabel1"].setText(str(item["current_score"]))
        if "already_entries" in item:
            labelGroup["entriesLabel2"].setText(str(item["already_entries"]))
        else:
            labelGroup["entriesLabel2"].setText("0")
        if "already_score" in item:
            labelGroup["scoreLabel2"].setText(str(item["already_score"]))
        else:
            labelGroup["scoreLabel2"].setText("0")

    def setLabelGroupState(self, labelGroup, type):
        for label in labelGroup.values():
            if type == "show":
                label.show()
            elif type == "hide":
                label.hide()

