'''圣遗物推荐参数选择弹窗'''
import copy
from extention import XCombobox
from PySide6.QtWidgets import QLabel, QComboBox

from modules.base.base_suit import BaseSuitWindow
from modules.zzz.zzz_data import data
from modules.zzz.zzz_set import SetWindow
from modules.zzz.zzz_suit_result import SuitResultWindow


class SuitWindow(BaseSuitWindow):
    def __init__(self, params):
        super().__init__({
            "enterParam": params.get("enterParam", 0),
            "character": params.get("character", "全属性"),
            "equipmentName": "光驱",
            "data": data,
            "SuitResultWindow": SuitResultWindow,
            "SetWindow": SetWindow
        })

    def initUI(self):
        super().initUI()

        self.layout.addWidget(QLabel('套装类型:'), 10, 0, 1, 1)
        self.layout.addWidget(QLabel('四件套'), 11, 1, 1, 1)
        self.layout.addWidget(QLabel('二件套'), 12, 1, 1, 1)
        self.suitCombobox1 = QComboBox()
        self.suitCombobox2 = QComboBox()
        self.suitCombobox1.addItem("选择套装")
        self.suitCombobox2.addItem("选择套装")
        for key in data.getSuitConfig():
            self.suitCombobox1.addItem(key)
            self.suitCombobox2.addItem(key)
        self.layout.addWidget(self.suitCombobox1, 11, 2, 1, 2)
        self.layout.addWidget(self.suitCombobox2, 12, 2, 1, 2)

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

        # 根据创建参数调整页面
        self.heroNameCombobox.setCurrentIndex(self.data.getCharacterIndex(self.character))
    # 推荐方案
    def startRating(self):
        params = {}
        params["suitA"] = self.suitCombobox1.currentText()
        params["suitB"] = self.suitCombobox2.currentText()
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
        result, tipsText = data.recommend(params)
        if result:
            self.suitResultWindow = self.SuitResultWindow()
            self.suitResultWindow.update(self.character, result)
            self.suitResultWindow.show()
        else:
            pass
        self.tipsLabel.setText(tipsText)

    def updateUI(self):
        indexObj = data.getIndexByCharacter(self.character)
        for key in indexObj:
            if key == "suitA":
                self.suitCombobox1.setCurrentIndex(indexObj[key])
            elif key == "suitB":
                self.suitCombobox2.setCurrentIndex(indexObj[key])
            else:
                if key in self.mainTagCombobox:
                    self.mainTagCombobox[key].set_selected(indexObj[key])

    def swichMainWindow(self):
        from modules.zzz.zzz_score import ScoreWindow
        super().swichMainWindow(ScoreWindow)
