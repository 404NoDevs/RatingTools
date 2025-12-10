from modules.base.base_info import BaseInfoWindow
from modules.starRail.starRail_data import data
from PySide6.QtGui import QFont, QStandardItemModel, QStandardItem

class EquipmentInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__({
            "data": data,
            "position": (305, 0),
            "size": (770, 990)
        })

    def update(self):
        headerList = ['名称', '穿戴者']
        config = self.data.get_evaluate_config()

        for index, item in enumerate(reversed(config)):
            header = item[2]
            headerList.append(header)

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

        suit_array_out = ["suitA", "suitB"]
        suit_array_in = ["suitC"]
        for character, tableItem in tableData.items():
            for suitName in suit_array_out + suit_array_in:
                if tableItem[suitName] in suitConfig:
                    row = suitConfig.index(tableItem[suitName])
                    standard_item = model.item(row, 1)
                    if standard_item:
                        text = standard_item.text() + "\n" + character
                        standard_item.setText(text)
                    else:
                        model.setItem(row, 1, QStandardItem(character))

                    for pos, posItem in tableItem["equipment"].items():
                        # 只处理对应位置的装备
                        pos_name_out = self.data.getPosName("out")
                        pos_name_in = self.data.getPosName("in")

                        if any((
                                suitName in suit_array_out and pos in pos_name_in,
                                suitName in suit_array_in and pos in pos_name_out
                        )):
                            continue

                        artifactItem = self.data.getArtifactItem(pos, posItem)
                        score = self.data.newScore(artifactItem, character)[1]
                        col = 1
                        for configItem in reversed(config):
                            if score >= configItem[0]:
                                col += 1
                            else:
                                break
                        standard_item = model.item(row, col)
                        if standard_item:
                            text = standard_item.text() + "\n" + character + "-" + pos
                            standard_item.setText(text)
                        else:
                            model.setItem(row, col, QStandardItem(character + "-" + pos))

        self.setColor(model, 2)
