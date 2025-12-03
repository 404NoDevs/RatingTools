'''设置窗口，自定义词条收益权重'''

import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QGridLayout,
    QDoubleSpinBox,
    QCheckBox
)

class BaseSetWindow(QWidget):
    def __init__(self, params):
        super().__init__()

        # 获取子类参数
        self.parent = params.get("parent", None)
        self.data = params.get("data", {})
        self.position = params.get("position", (0, 0))

        # 初始化数值
        self.character = "全属性"
        self.config = {}

        # 初始化UI
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../../src/keqing.ico')))
        self.setWindowTitle("得分权重设置")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(*self.position)

        self.openFileButton = QPushButton('打开文件')
        self.dataUpdateButton = QPushButton('更新数据')
        # 显示当前角色
        self.heroNameLabel = QLabel("")
        # 显示得分权重
        self.entryChild = {}
        for keyName in self.data.getEntryArray():
            numText = QDoubleSpinBox()
            numText.setMinimum(-1)
            numText.setMaximum(2)
            numText.setSingleStep(0.1)
            numText.setValue(0)
            numText.setAlignment(Qt.AlignRight)
            self.entryChild[keyName] = {}
            self.entryChild[keyName]["entryNum"] = numText
            self.entryChild[keyName]["checkBtn"] = QCheckBox("")
        # 添加保存按钮
        self.saveButton = QPushButton('确认修改')

        # 注意事项
        self.tipsLabel1 = QLabel('注意事项：')
        self.tipsLabel1.setStyleSheet("color:red;")
        self.tipsLabel2 = QLabel('1.小词条（固定值）得分为大词条（百分比）的一半')
        self.tipsLabel2.setStyleSheet("color:red;")

        # 弹窗内容
        layout = QGridLayout()
        layout.addWidget(self.openFileButton, 0, 0, 1, 1)
        layout.addWidget(self.dataUpdateButton, 0, 1, 1, 1)
        layout.addWidget(QLabel('当前角色：'), 1, 0, Qt.AlignRight)
        layout.addWidget(self.heroNameLabel, 1, 1)
        # layout.addWidget(QLabel('核心词条'), 1, 2, Qt.AlignCenter)
        counter = 2
        for keyName in self.entryChild:
            layout.addWidget(QLabel(keyName + "："), counter, 0, Qt.AlignRight)
            layout.addWidget(self.entryChild[keyName]["entryNum"], counter, 1, Qt.AlignLeft)
            # layout.addWidget(self.entryChild[keyName]["checkBtn"], counter, 2, Qt.AlignCenter)
            counter += 1
        layout.addWidget(self.saveButton, 100, 0, 1, 2)
        layout.addWidget(self.tipsLabel1, 101, 0, 1, 2)
        layout.addWidget(self.tipsLabel2, 102, 0, 1, 2)
        self.setLayout(layout)

        # 注册按钮事件
        self.openFileButton.clicked.connect(self.openFile)
        self.dataUpdateButton.clicked.connect(self.updateData)
        self.saveButton.clicked.connect(self.btn_save)

    def updateUI(self):
        herConfig = self.data.getCharacters()
        # 兼容数据异常情况
        if self.character in herConfig and herConfig[self.character] != {}:
            self.heroNameLabel.setText(self.character)
            for keyName in self.entryChild:
                self.entryChild[keyName]["entryNum"].setValue(herConfig[self.character]["weight"][keyName])
                self.entryChild[keyName]["checkBtn"].setChecked(keyName in herConfig[self.character].get("core", []))
        else:
            self.heroNameLabel.setText("请正确的选择角色")
            for keyName in self.entryChild:
                self.entryChild[keyName]["entryNum"].setValue(0)
                self.entryChild[keyName]["checkBtn"].setChecked(False)

    def update(self, character):
        self.character = character
        self.updateUI()

    def btn_save(self):
        tempConfig = {}
        tempConfig["weight"] = {}
        for keyName in self.entryChild:
            tempConfig["weight"][keyName] = round(self.entryChild[keyName]["entryNum"].value(), 2)

        # tempConfig["core"] = [keyName for keyName in self.entryChild if self.entryChild[keyName]["checkBtn"].isChecked()]

        self.data.setCharacters(self.character, tempConfig)

        if self.parent and self.parent.fresh_main_and_paste_window:
            self.parent.fresh_main_and_paste_window()

        self.close()

    # 数据更新
    def updateData(self):
        self.data.loadData()

    # 打开文件夹
    def openFile(self):
        os.startfile(self.data.getUserDataPath())
