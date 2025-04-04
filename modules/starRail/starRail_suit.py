'''圣遗物推荐参数选择弹窗'''
import copy
from extention import XCombobox
from PySide6.QtWidgets import QLabel, QComboBox

from modules.base.base_suit import BaseSuitWindow
from modules.starRail.starRail_data import data
from modules.starRail.starRail_set import SetWindow
from modules.starRail.starRail_suit_result import SuitResultWindow
from modules.starRail.starRail_info_character import CharacterInfoWindow
from modules.starRail.starRail_info_equipment import EquipmentInfoWindow

class SuitWindow(BaseSuitWindow):

    def __init__(self, params):
        super().__init__({
            "enterParam": params.get("enterParam", 0),
            "character": params.get("character", "全属性"),
            "equipmentName": "遗器",
            "data": data,
            "SuitResultWindow": SuitResultWindow,
            "SetWindow": SetWindow,
            "CharacterInfoWindow": CharacterInfoWindow,
            "EquipmentInfoWindow": EquipmentInfoWindow
        })

    def initUI(self):
        super().initUI()

        self.layout.addWidget(QLabel('套装类型:'), 10, 0, 1, 1)
        self.layout.addWidget(QLabel('外圈A'), 11, 1, 1, 1)
        self.layout.addWidget(QLabel('外圈B'), 12, 1, 1, 1)
        self.suitComboboxA = QComboBox()
        self.suitComboboxB = QComboBox()
        self.suitComboboxA.addItem("选择套装")
        self.suitComboboxB.addItem("选择套装")
        for key in data.getSuitConfig("外圈"):
            self.suitComboboxA.addItem(key)
            self.suitComboboxB.addItem(key)
        self.layout.addWidget(self.suitComboboxA, 11, 2, 1, 2)
        self.layout.addWidget(self.suitComboboxB, 12, 2, 1, 2)
        self.layout.addWidget(QLabel('内圈C'), 13, 1, 1, 1)
        self.suitComboboxC = QComboBox()
        self.suitComboboxC.addItem("选择套装")
        for key in data.getSuitConfig("内圈"):
            self.suitComboboxC.addItem(key)
        self.layout.addWidget(self.suitComboboxC, 13, 2, 1, 2)

        self.layout.addWidget(QLabel('主要属性:'), 15, 0, 1, 1)
        self.layout.addWidget(QLabel('(不选默认不限制主词条)'), 15, 1, 1, 4)
        self.mainAttrCombobox = {}
        MainAttrType = data.getMainAttrType()
        for index, (key, values) in enumerate(MainAttrType.items()):
            self.layout.addWidget(QLabel(key), 16 + index, 1, 1, 2)
            mainAttrCombobox = XCombobox("任意属性")
            mainAttrCombobox.add_items(values)
            self.layout.addWidget(mainAttrCombobox, 16 + index, 2, 1, 2)
            self.mainAttrCombobox[key] = mainAttrCombobox

        # 根据创建参数调整页面
        self.heroNameCombobox.setCurrentIndex(self.data.getCharacterIndex(self.character))

    # 推荐方案
    def startRating(self):
        params = {}
        params["suitA"] = self.suitComboboxA.currentText()
        params["suitB"] = self.suitComboboxB.currentText()
        params["suitC"] = self.suitComboboxC.currentText()
        needMainAttr = {}
        for key in self.mainAttrCombobox:
            mainAttr = self.mainAttrCombobox[key].get_selected()
            needMainAttr[key] = mainAttr
            params[key] = mainAttr

        # 保存方案
        saveParams = copy.deepcopy(params)
        data.setCharacters(self.character, saveParams)

        params["needMainAttr"] = needMainAttr
        params["character"] = self.character
        params["selectType"] = self.selectType

        # 获取推荐数据
        result, tipsText = data.recommend(params)
        if result:
            self.suitResultWindow = SuitResultWindow()
            self.suitResultWindow.update(self.character, result)
            self.suitResultWindow.show()
        else:
            pass
        self.tipsLabel.setText(tipsText)

    def updateUI(self):
        indexObj = data.getIndexByCharacter(self.character)
        for key in indexObj:
            if key == "suitA":
                self.suitComboboxA.setCurrentIndex(indexObj[key])
            elif key == "suitB":
                self.suitComboboxB.setCurrentIndex(indexObj[key])
            elif key == "suitC":
                self.suitComboboxC.setCurrentIndex(indexObj[key])
            else:
                if key in self.mainAttrCombobox:
                    self.mainAttrCombobox[key].set_selected(indexObj[key])

    # 切换为评分
    def swichMainWindow(self):
        from modules.starRail.starRail_score import ScoreWindow
        super().swichMainWindow(ScoreWindow)
