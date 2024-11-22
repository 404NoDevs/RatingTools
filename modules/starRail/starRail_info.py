from modules.base.base_info import BaseInfoWindow
from modules.starRail.starRail_data import data
from PySide6.QtGui import QFont, QColor, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt


class InfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__({
            "data": data,
            "position": (305, 0),
            "size": (1230, 425)
        })

    def update(self):
        data = self.data.get_table_data()

        model = QStandardItemModel(len(data), 13)
        headerList = [
            '角色',  # 0
            '外圈一',  # 1
            '外圈二',  # 2
            '内圈',  # 3
            '躯干-主',  # 4
            "脚部-主",  # 5
            "位面球-主",  # 6
            "连结绳-主",  # 7
            "得分权重",  # 8
            "头部",  # 9
            "手部",  # 10
            "躯干",  # 11
            "脚部",  # 12
            "位面球",  # 13
            "连结绳",  # 14
            "总分"  # 15
        ]
        model.setHorizontalHeaderLabels(headerList)
        self.table_view.horizontalHeader().setFont(QFont("Microsoft YaHei", 8, QFont.Bold))

        self.table_view.setModel(model)
        self.table_view.setColumnWidth(0, 70)
        for index in range(1, 3):
            self.table_view.setColumnWidth(index, 105)
        for index in range(9, 15):
            self.table_view.setColumnWidth(index, 40)
        self.table_view.setColumnWidth(15, 40)

        for row, characterItem in enumerate(data):
            nameItem = QStandardItem(characterItem)
            nameItem.setFont(QFont("Microsoft YaHei", 8, QFont.Bold))
            model.setItem(row, 0, nameItem)
            characterData = data[characterItem]
            for col, item in enumerate(characterData):
                if item == "suitA" or item == "suitB" or item == "suitC":
                    suitStr = characterData[item]
                    if suitStr == "选择套装":
                        suitStr = "无"

                    colConfig = {
                        "suitA": 1,
                        "suitB": 2,
                        "suitC": 3
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

                    model.setItem(row, 8, QStandardItem(weightStr))
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
                    sumScoreItem.setBackground(QColor(*self.data.get_evaluate(scoreSum / len(self.data.getPosName()))[1]))
                    model.setItem(row, 15, sumScoreItem)
                else:
                    pass

        model.sort(15, Qt.DescendingOrder)
