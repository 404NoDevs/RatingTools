'''圣遗物推荐参数选择弹窗'''
import copy
from extention import ExtendedComboBox, XCombobox
from PySide6.QtWidgets import QLabel

from modules.base.base_suit import BaseSuitWindow
from modules.starRail.starRail_data import data
from modules.starRail.starRail_set import SetWindow
from modules.starRail.starRail_suit_result import SuitResultWindow


class SuitWindow(BaseSuitWindow):

    def __init__(self, params):
        super().__init__({
            "enterParam": params.get("enterParam", 0),
            "character": params.get("character", "全属性"),
            "equipmentName": "遗器",
            "data": data,
            "SuitResultWindow": SuitResultWindow,
            "SetWindow": SetWindow
        })

    def initUI(self):
        super().initUI()

        self.layout.addWidget(QLabel('套装类型:'), 10, 0, 1, 1)
        self.layout.addWidget(QLabel('外圈A'), 11, 1, 1, 1)
        self.layout.addWidget(QLabel('外圈B'), 12, 1, 1, 1)
        self.suitComboboxA = ExtendedComboBox()
        self.suitComboboxB = ExtendedComboBox()
        self.suitComboboxA.addItem("选择套装")
        self.suitComboboxB.addItem("选择套装")
        for key in data.getSuitConfig("外圈"):
            self.suitComboboxA.addItem(key)
            self.suitComboboxB.addItem(key)
        self.layout.addWidget(self.suitComboboxA, 11, 2, 1, 2)
        self.layout.addWidget(self.suitComboboxB, 12, 2, 1, 2)
        self.layout.addWidget(QLabel('内圈C'), 13, 1, 1, 1)
        self.suitComboboxC = ExtendedComboBox()
        self.suitComboboxC.addItem("选择套装")
        for key in data.getSuitConfig("内圈"):
            self.suitComboboxC.addItem(key)
        self.layout.addWidget(self.suitComboboxC, 13, 2, 1, 2)

        self.layout.addWidget(QLabel('主要属性:'), 15, 0, 1, 1)
        self.layout.addWidget(QLabel('(不选默认不限制主词条)'), 15, 1, 1, 4)
        self.mainTagCombobox = {}
        MainTagType = data.getMainTagType()
        for index, (key, values) in enumerate(MainTagType.items()):
            self.layout.addWidget(QLabel(key), 16 + index, 1, 1, 2)
            mainTagCombobox = XCombobox("任意属性")
            mainTagCombobox.add_items(values)
            self.layout.addWidget(mainTagCombobox, 16 + index, 2, 1, 2)
            self.mainTagCombobox[key] = mainTagCombobox

    # 推荐方案
    def startRating(self):
        params = {}
        params["suitA"] = self.suitComboboxA.currentText()
        params["suitB"] = self.suitComboboxB.currentText()
        params["suitC"] = self.suitComboboxC.currentText()
        needMainTag = {}
        for key in self.mainTagCombobox:
            mainTag = self.mainTagCombobox[key].get_selected()
            needMainTag[key] = mainTag
            params[key] = mainTag

        # 保存方案
        saveParams = copy.deepcopy(params)
        data.setArtifactScheme(self.character, saveParams)

        params["needMainTag"] = needMainTag
        params["character"] = self.character
        params["selectType"] = self.selectType

        # 获取推荐数据
        result = data.recommend(params)
        if result:
            self.suitResultWindow = SuitResultWindow()
            self.suitResultWindow.update(self.character, result)
            self.suitResultWindow.show()
        else:
            print("无可用方案")

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
                if key in self.mainTagCombobox:
                    self.mainTagCombobox[key].set_selected(indexObj[key])

    # 切换为评分
    def swichMainWindow(self):
        from modules.starRail.starRail_score import ScoreWindow
        super().initUI(ScoreWindow)
