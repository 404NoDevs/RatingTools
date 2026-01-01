import os
from PySide6.QtCore import Qt
from PySide6.QtGui import (QFont, QIcon, QColor, QStandardItem, QStandardItemModel)
from PySide6.QtWidgets import (QWidget, QGridLayout, QTableView)
from modules.base.base_constants import *
from utils import *


class BaseInfoEquipmentWindow(QWidget):
    def __init__(self, params):
        super().__init__()
        # 初始化子类参数
        self.data = params.get("data")
        self.position = params.get("position", (0, 0))
        self.size = params.get("size", (0, 0))
        self.suitArray = params.get("suitArray", [])
        self.widthList = params.get("widthList", [0, 0, 0])

        # 初始化参数
        self.table_view = None

        # 初始化UI
        self.initUI()
        self.update()

    def initUI(self):
        self.setWindowFlags(Qt.Window)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../../src/keqing.ico')))
        self.setWindowTitle("装备角色信息")
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
        headerList = ['名称', '穿戴者']
        config = self.data.get_evaluate_config()
        for index, item in enumerate(reversed(config)):
            header = item[2]
            headerList.append(header)
        suitConfig = [key for key in self.data.getSuitConfig().keys()]
        print(suitConfig)
        suitConfigNoTwo = [suitName for suitName in suitConfig if TWO_PIECE_SET_KEY not in suitName]
        tableData = self.data.get_table_data()
        model = QStandardItemModel(len(suitConfigNoTwo), len(headerList))
        model.setHorizontalHeaderLabels(headerList)
        self.table_view.horizontalHeader().setFont(QFont("Microsoft YaHei", 8, QFont.Bold))
        self.table_view.setModel(model)
        self.table_view.setColumnWidth(headerList.index("名称"), self.widthList[0])
        self.table_view.setColumnWidth(headerList.index("穿戴者"), self.widthList[1])
        for index in range(2, len(headerList) - 1):
            self.table_view.setColumnWidth(index, self.widthList[2])
        for row, suitName in enumerate(suitConfigNoTwo):
            nameItem = QStandardItem(suitName)
            nameItem.setFont(QFont("Microsoft YaHei", 8, QFont.Bold))
            model.setItem(row, headerList.index("名称"), nameItem)
            # 创建所有子Item
            for index in range(1, len(headerList)):
                standardItem = QStandardItem("")
                model.setItem(row, index, standardItem)

        for character, tableItem in tableData.items():
            for suitName in self.suitArray:
                if tableItem[suitName] in suitConfig:
                    if TWO_PIECE_SET_KEY in tableItem[suitName]:
                        suit_list = self.data.getSuitListByKey(tableItem[suitName])
                    else:
                        suit_list = [tableItem[suitName]]

                    for suitNameItem in suit_list:
                        row = suitConfigNoTwo.index(suitNameItem)
                        standard_item = model.item(row, headerList.index("穿戴者"))
                        text = standard_item.text()
                        if character in text:
                            continue  # 避免重复添加
                        standard_item.setText(dealTableText(text, character, "人"))

                        for pos, posItem in tableItem["equipment"].items():
                            artifactItem = self.data.getArtifactItem(pos, posItem)
                            score = self.data.newScore(artifactItem, character)[1]
                            colCounter = 1
                            for configItem in reversed(config):
                                if score >= configItem[0]:
                                    colCounter += 1
                                else:
                                    break
                            standardItem = model.item(row, colCounter)
                            standardItem.setText(dealTableText(standardItem.text(), character + "-" + pos))
        setColor(model, 2)
