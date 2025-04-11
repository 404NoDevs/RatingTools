from modules.base.base_info import BaseInfoWindow
from modules.genshin.genshin_data import data
from PySide6.QtGui import QFont, QColor, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt


class CharacterInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__({
            "data": data,
            "position": (300, 0),
            "size": (955, 375)
        })

    def update(self):
        tableData = self.data.get_table_data()
        headerList = [
            '角色',  # 0
            '套装一',  # 1
            '套装二',  # 2
            '沙-主',  # 3
            "杯-主",  # 4
            "冠-主",  # 5
            "得分权重",  # 6
            "花",  # 7
            "羽",  # 8
            "沙",  # 9
            "杯",  # 10
            "冠",  # 11
            "总分"  # 12
        ]
        model = QStandardItemModel(len(tableData), len(headerList))
        model.setHorizontalHeaderLabels(headerList)
        self.table_view.horizontalHeader().setFont(QFont("Microsoft YaHei", 8, QFont.Bold))

        self.table_view.setModel(model)
        self.table_view.setColumnWidth(0, 70)
        for index in range(7, 12):
            self.table_view.setColumnWidth(index, 35)
        self.table_view.setColumnWidth(12, 40)

        for row, characterItem in enumerate(tableData):
            nameItem = QStandardItem(characterItem)
            nameItem.setFont(QFont("Microsoft YaHei", 8, QFont.Bold))
            model.setItem(row, 0, nameItem)
            characterData = tableData[characterItem]
            for col, item in enumerate(characterData):
                if item == "suitA" or item == "suitB":
                    suitStr = characterData[item]
                    if suitStr == "选择套装":
                        suitStr = "无"

                    colConfig = {
                        "suitA": 1,
                        "suitB": 2
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

                    model.setItem(row, headerList.index(item[2] + "-主"), QStandardItem(mainArrayStr))
                elif item == "weight":
                    weightStr = ""
                    for key, value in characterData[item].items():
                        if value > 0:
                            weightStr += key + ":" + str(value) + "\n"

                    model.setItem(row, 6, QStandardItem(weightStr))
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
                            model.setItem(row, headerList.index(posItem[2]), scoreItem)
                            scoreSum += score
                        else:
                            model.setItem(row, headerList.index(posItem[2]), QStandardItem("无"))
                    sumScoreItem = QStandardItem(str(round(scoreSum, 1)))
                    sumScoreItem.setData(round(float(scoreSum), 1), Qt.DisplayRole)  # 强制转为flot类型用于后续排序
                    sumScoreItem.setBackground(QColor(*self.data.get_evaluate(scoreSum / len(self.data.getPosName()))[1]))
                    model.setItem(row, 12, sumScoreItem)
                else:
                    pass

        model.sort(12, Qt.DescendingOrder)
