from modules.base.base_info import BaseInfoWindow
from modules.genshin.genshin_data import data
from PySide6.QtGui import QFont, QColor, QStandardItemModel, QStandardItem

class EquipmentInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__({
            "data": data,
            "position": (300, 0),
            "size": (770, 370)
        })

    def update(self):
        headerList = ['名称', '穿戴者']
        config = self.data.get_evaluate_config()
        for index, item in enumerate(reversed(config)):
            lastIndex = index - 1

            if lastIndex >= 0:
                header = "[" + str(config[-lastIndex - 1][0]) + ',' + str(item[0]) + ")"
                headerList.append(header)
        headerList.append(str(config[0][0]) + '以上')

        suitConfig = list(self.data.getSuitConfig().keys())
        tableData = self.data.get_table_data()

        model = QStandardItemModel(len(suitConfig), len(headerList))
        model.setHorizontalHeaderLabels(headerList)
        self.table_view.horizontalHeader().setFont(QFont("Microsoft YaHei", 8, QFont.Bold))

        self.table_view.setModel(model)
        self.table_view.setColumnWidth(0, 90)
        self.table_view.setColumnWidth(1, 70)
        for index in range(2, 6):
            self.table_view.setColumnWidth(index, 110)

        for row, suitName in enumerate(suitConfig):
            nameItem = QStandardItem(suitName)
            nameItem.setFont(QFont("Microsoft YaHei", 8, QFont.Bold))
            model.setItem(row, 0, nameItem)

        suitArray = ["suitA", "suitB"]
        for character, tableItem in tableData.items():
            for suitName in suitArray:
                if tableItem[suitName] in suitConfig:
                    row = suitConfig.index(tableItem[suitName])
                    standard_item = model.item(row, 1)
                    if standard_item:
                        text = standard_item.text() + "\n" + character
                        standard_item.setText(text)
                    else:
                        model.setItem(row, 1, QStandardItem(character))

                    for pos, posItem in tableItem["equipment"].items():
                        artifactItem = self.data.getArtifactItem(pos, posItem)
                        score = self.data.newScore(artifactItem, character)[1]
                        col = 1
                        for configItem in reversed(config):
                            if score >= configItem[0]:
                                col += 1
                            else:
                                break
                        standardItem = model.item(row, col)
                        if standardItem:
                            text = standardItem.text() + "\n" + character + "-" + pos
                            standardItem.setText(text)
                        else:
                            model.setItem(row, col, QStandardItem(character + "-" + pos))

        # 设置交替行颜色
        for row in range(model.rowCount()):
            color = QColor(240, 240, 240) if (row // 2) % 2 == 0 else QColor(255, 255, 255)
            for col in range(model.columnCount()):
                standardItem = model.item(row, col)
                if not standardItem:
                    standardItem = QStandardItem()
                    model.setItem(row, col, standardItem)
                standardItem.setBackground(color)
