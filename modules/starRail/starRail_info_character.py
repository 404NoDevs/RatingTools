from modules.base.base_info_character import BaseInfoCharacterWindow
from modules.starRail.starRail_data import data
from modules.starRail.starRail_constants import *
from PySide6.QtGui import QFont, QColor, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from utils import *


class CharacterInfoWindow(BaseInfoCharacterWindow):
    def __init__(self):
        super().__init__({
            "data": data,
            "position": (305, 0),
            "size": (1290, 990)
        })

    def update(self):
        data = self.data.get_table_data()
        headerList = [
            '角色',  # 0
            '版本',  # 1
            '外圈一',  # 2
            '外圈二',  # 3
            '内圈',  # 4
            '躯干-主',  # 5
            "脚部-主",  # 6
            "位面球-主",  # 7
            "连结绳-主",  # 8
            "得分权重",  # 9
            "头部",  # 10
            "手部",  # 11
            "躯干",  # 12
            "脚部",  # 13
            "位面球",  # 14
            "连结绳",  # 15
            "总分"  # 16
        ]
        model = QStandardItemModel(len(data), len(headerList))
        model.setHorizontalHeaderLabels(headerList)
        self.table_view.horizontalHeader().setFont(QFont("Microsoft YaHei", 8, QFont.Bold))

        self.table_view.setModel(model)
        self.table_view.setColumnWidth(headerList.index("角色"), 80)
        self.table_view.setColumnWidth(headerList.index("版本"), 50)
        for index in range(headerList.index("外圈一"), headerList.index("内圈") + 1):
            self.table_view.setColumnWidth(index, 105)
        for index in range(headerList.index("躯干-主"), headerList.index("得分权重") + 1):
            self.table_view.setColumnWidth(index, 100)
        for index in range(headerList.index("头部"), headerList.index("连结绳") + 1):
            self.table_view.setColumnWidth(index, 40)
        self.table_view.setColumnWidth(headerList.index("总分"), 50)

        for row, characterItem in enumerate(data):
            nameItem = QStandardItem(characterItem)
            nameItem.setFont(QFont("Microsoft YaHei", 8, QFont.Bold))
            model.setItem(row, headerList.index("角色"), nameItem)
            versionItem = QStandardItem(str(data[characterItem]["version"]))
            # versionItem.setData(data[characterItem]["version"], Qt.DisplayRole)
            model.setItem(row, headerList.index("版本"), versionItem)

            characterData = data[characterItem]
            for col, item in enumerate(characterData):
                if item == "suitA" or item == "suitB" or item == "suitC":
                    suitStr = characterData[item]
                    if suitStr == NO_SELECT_KEY:
                        suitStr = "无"

                    colConfig = {
                        "suitA": headerList.index("外圈一"),
                        "suitB": headerList.index("外圈二"),
                        "suitC": headerList.index("内圈")
                    }
                    model.setItem(row, colConfig[item], QStandardItem(suitStr))
                elif item in self.data.getMainAttrType():
                    mainArrayStr = "错误"
                    if len(characterData[item]) == 0:
                        mainArrayStr = "无"
                    else:
                        mainArrayStr = ""
                        for mainArrayItem in characterData[item]:
                            mainArrayStr += mainArrayItem + "\n"

                    model.setItem(row, headerList.index(item + "-主"), QStandardItem(mainArrayStr))
                elif item == "weight":
                    weightStr = ""
                    for key, value in characterData[item].items():
                        if value > 0:
                            weightStr += key + ":" + str(value) + "\n"

                    model.setItem(row, headerList.index("得分权重"), QStandardItem(weightStr))
                elif item == "equipment":
                    scoreSum = 0
                    for index, posItem in enumerate(self.data.getPosName()):
                        if posItem in characterData[item]:
                            artifactItem = self.data.getArtifactItem(posItem, characterData[item][posItem])

                            score = 0
                            if artifactItem != {}:
                                score = self.data.newScore(artifactItem, characterItem)[1]

                            scoreItem = QStandardItem(str(score))
                            scoreItem.setBackground(QColor(*self.data.get_evaluate(score)[1]))
                            model.setItem(row, headerList.index(posItem), scoreItem)
                            scoreSum += score

                    sumScoreItem = QStandardItem(str(round(scoreSum, 1)))
                    # sumScoreItem.setData(round(float(scoreSum), 1), Qt.DisplayRole)  # 强制转为flot类型用于后续排序
                    sumScoreItem.setBackground(QColor(*self.data.get_evaluate(scoreSum / len(self.data.getPosName()))[1]))
                    model.setItem(row, headerList.index("总分"), sumScoreItem)
                else:
                    pass

        model.sort(headerList.index("版本"), Qt.DescendingOrder)
        setColor(model, 1)
