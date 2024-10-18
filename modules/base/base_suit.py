'''圣遗物推荐参数选择弹窗'''

import os
from extention import ExtendedComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QRadioButton,
    QPushButton,
    QWidget,
    QGridLayout,
    QComboBox
)


class BaseSuitWindow(QWidget):

    def __init__(self, params):
        super().__init__()

        # 子类参数
        self.enter_params = params.get("enterParam", 0)
        self.character = params.get("character", "全属性")
        self.equipment_name = params.get('equipmentName', "圣遗物")
        self.data = params.get("data")
        self.SuitResultWindow = params.get("SuitResultWindow")
        self.SetWindow = params.get("SetWindow")

        # 初始化变量
        self.setWindow = None
        self.suitResultWindow = None
        self.selectType = 1

        self.initUI()
        self.updateUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../../src/keqing.ico')))
        self.setWindowTitle(f"{self.equipment_name}套装推荐")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(0, 0)

        # 创建界面UI
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # 上半部分
        self.checkButton = QPushButton('检查更新')
        self.layout.addWidget(self.checkButton, 0, 0, 1, 2)
        self.scoreButton = QPushButton(f'{self.equipment_name}评分→')
        self.layout.addWidget(self.scoreButton, 0, 2, 1, 2)
        self.layout.addWidget(QLabel('当前角色：'), 1, 0, 1, 1)
        self.heroNameCombobox = ExtendedComboBox()
        for herName in self.data.getCharacters():
            self.heroNameCombobox.addItem(herName)
        self.layout.addWidget(self.heroNameCombobox, 1, 1, 1, 2)
        self.setButton = QPushButton('设置>')
        self.layout.addWidget(self.setButton, 1, 3, 1, 1)
        # 下半部分
        self.layout.addWidget(QLabel('其他选择:'), 20, 0, 1, 1)
        self.radiobtn1 = QRadioButton('仅未装备')
        self.radiobtn2 = QRadioButton('全部')
        self.radiobtn1.setChecked(True)
        self.layout.addWidget(self.radiobtn1, 21, 1, 1, 1)
        self.layout.addWidget(self.radiobtn2, 21, 2, 1, 1)
        self.startButton = QPushButton('生成方案')
        self.layout.addWidget(self.startButton, 22, 0, 1, 4)
        self.tipsLabel = QLabel('提示文本')
        self.tipsLabel.setStyleSheet("qproperty-alignment: 'AlignCenter';color:red;")
        self.layout.addWidget(self.tipsLabel, 23, 0, 1, 4)

        # 注册事件
        self.scoreButton.clicked.connect(self.swichMainWindow)
        self.heroNameCombobox.currentIndexChanged.connect(self.heroNameCurrentIndexChanged)
        self.radiobtn1.toggled.connect(lambda: self.radiobtn_state(self.radiobtn1))
        self.radiobtn2.toggled.connect(lambda: self.radiobtn_state(self.radiobtn2))
        self.startButton.clicked.connect(self.startRating)
        self.setButton.clicked.connect(self.openSetWindow)
        self.checkButton.clicked.connect(self.checkButtonClicked)

        # 根据创建参数调整页面
        self.scoreButton.setEnabled(self.enter_params != 1)

    def closeEvent(self, event):
        if self.setWindow:
            self.setWindow.close()
        if self.suitResultWindow:
            self.suitResultWindow.close()

    # 单选框按钮
    def radiobtn_state(self, btn):
        if btn.text() == '仅未装备' and btn.isChecked() == True:
            self.selectType = 1
        elif btn.text() == '全部' and btn.isChecked() == True:
            self.selectType = 2

    # 英雄名称
    def heroNameCurrentIndexChanged(self):
        self.character = self.heroNameCombobox.currentText()
        if self.setWindow:
            self.setWindow.update(self.character)
        self.updateUI()

    # 切换为评分
    def swichMainWindow(self, window):
        global mainWindow
        mainWindow = window()
        mainWindow.initCombobox(self.character)
        mainWindow.show()
        self.close()

    def openSetWindow(self):
        self.setWindow = self.SetWindow()
        self.setWindow.update(self.character)
        self.setWindow.show()

    def checkButtonClicked(self):
        updateArray = self.data.checkUpdate()
        if len(updateArray) > 0:
            tipsStr = "、".join(updateArray) + " 需要更新"
        else:
            tipsStr = "没有需要更新的套装"
        self.tipsLabel.setText(tipsStr)

    def startRating(self):
        pass

    def updateUI(self):
        pass
