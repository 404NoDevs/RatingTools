from modules.base.base_info_character import BaseInfoCharacterWindow
from modules.zzz.zzz_data import data
from modules.zzz.zzz_constants import *
from PySide6.QtGui import QFont, QColor, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from utils import *


class CharacterInfoWindow(BaseInfoCharacterWindow):
    def __init__(self):
        super().__init__({
            "data": data,
            "position": (300, 0),
            "size": (1035, 990)
        })

    def update(self):
        data = self.data.get_table_data()
        headerList = [
            '角色',  # 0
            '版本',  # 1
            '四件套',  # 2
            '二件套',  # 3
            '分区4-主',  # 4
            "分区5-主",  # 5
            "分区6-主",  # 6
            "得分权重",  # 7
            "分区1",  # 8
            "分区2",  # 9
            "分区3",  # 10
            "分区4",  # 11
            "分区5",  # 12
            "分区6",  # 13
            "总分"  # 14
        ]
        model = QStandardItemModel(len(data), len(headerList))
        model.setHorizontalHeaderLabels(headerList)
        self.table_view.horizontalHeader().setFont(QFont("Microsoft YaHei", 8, QFont.Bold))

        self.table_view.setModel(model)
        self.table_view.setColumnWidth(headerList.index("角色"), 70)
        self.table_view.setColumnWidth(headerList.index("版本"), 50)
        for index in range(headerList.index("四件套"), headerList.index("得分权重")+1):
            self.table_view.setColumnWidth(index, 100)
        for index in range(headerList.index("分区1"), headerList.index("分区6")+1):
            self.table_view.setColumnWidth(index, 35)
        self.table_view.setColumnWidth(headerList.index("总分"), 40)

        for row, characterItem in enumerate(data):
            nameItem = QStandardItem(characterItem)
            nameItem.setFont(QFont("Microsoft YaHei", 8, QFont.Bold))
            model.setItem(row, headerList.index("角色"), nameItem)
            versionItem = QStandardItem(str(data[characterItem]["version"]))
            model.setItem(row, headerList.index("版本"), versionItem)

            characterData = data[characterItem]
            for col, item in enumerate(characterData):
                if item == "suitA" or item == "suitB":
                    suitStr = characterData[item]
                    if suitStr == NO_SELECT_KEY:
                        suitStr = "无"

                    colConfig = {
                        "suitA": headerList.index("四件套"),
                        "suitB": headerList.index("二件套")
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
                        else:
                            scoreItem = QStandardItem(str("无"))
                            model.setItem(row, headerList.index(posItem), scoreItem)

                    sumScoreItem = QStandardItem(str(round(scoreSum, 1)))
                    sumScoreItem.setBackground(QColor(*self.data.get_evaluate(scoreSum / len(self.data.getPosName()))[1]))
                    model.setItem(row, headerList.index("总分"), sumScoreItem)
                else:
                    pass

        model.sort(headerList.index("版本"), Qt.DescendingOrder)
        setColor(model, 1)
