'''圣遗物推荐方案生成弹窗'''

import os, pyperclip
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QGridLayout,
    QComboBox
)


class BaseSuitResultWindow(QWidget):

    def __init__(self, params):
        super().__init__()

        # 获取子类参数
        self.data = params.get("data", {})
        self.position = params.get("position", (0, 0))

        # 初始化变量
        self.character = "全属性"
        self.score_array = []
        self.resultArray = []

        # 初始化UI
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../../src/keqing.ico')))
        self.setWindowTitle("推荐方案")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(*self.position)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("当前方案："), 0, 0, 1, 1)
        self.programmeCombobox = QComboBox()
        layout.addWidget(self.programmeCombobox, 0, 1, 1, 5)
        self.copyButton = QPushButton('复制得分')
        layout.addWidget(self.copyButton, 0, 6, 1, 1)

        self.artifactNameLabel1 = {}
        self.artifactScoreLabel1 = {}
        self.artifactOwnerLabel1 = {}
        self.artifactNameLabel2 = {}
        self.artifactScoreLabel2 = {}
        self.artifactOwnerLabel2 = {}
        self.artifactScoreSubLabel = {}
        for index, posItem in enumerate(self.data.getPosName()):
            layout.addWidget(QLabel(posItem), 1 + 3 * index + 1, 0, 2, 1)
            layout.addWidget(QLabel("当前："), 1 + 3 * index + 1, 1, 1, 1)
            self.artifactNameLabel1[posItem] = QLabel("无装备")
            layout.addWidget(self.artifactNameLabel1[posItem], 1 + 3 * index + 1, 2, 1, 1)
            self.artifactOwnerLabel1[posItem] = QLabel("0")
            layout.addWidget(self.artifactOwnerLabel1[posItem], 1 + 3 * index + 1, 3, 1, 1)
            self.artifactScoreLabel1[posItem] = QLabel("0")
            layout.addWidget(self.artifactScoreLabel1[posItem], 1 + 3 * index + 1, 4, 1, 1)
            layout.addWidget(QLabel("推荐："), 2 + 3 * index + 1, 1, 1, 1)
            self.artifactNameLabel2[posItem] = QLabel("无装备")
            layout.addWidget(self.artifactNameLabel2[posItem], 2 + 3 * index + 1, 2, 1, 1)
            self.artifactOwnerLabel2[posItem] = QLabel("无人装备")
            layout.addWidget(self.artifactOwnerLabel2[posItem], 2 + 3 * index + 1, 3, 1, 1)
            self.artifactScoreLabel2[posItem] = QLabel("0")
            layout.addWidget(self.artifactScoreLabel2[posItem], 2 + 3 * index + 1, 4, 1, 1)
            self.artifactScoreSubLabel[posItem] = QLabel("0")
            layout.addWidget(self.artifactScoreSubLabel[posItem], 1 + 3 * index + 1, 5, 2, 1)
            button = QPushButton('替换')
            button.setObjectName(posItem)
            button.clicked.connect(self.equip)
            layout.addWidget(button, 1 + 3 * index + 1, 6, 2, 1)

            layout.addWidget(QLabel(" "), 4 + 3 * index, 0, 1, 6)  # 占位符

        self.equipTipsLabel = QLabel("将推荐装备全部标记")
        self.equipTipsLabel.setStyleSheet("color:red;qproperty-alignment: 'AlignCenter';")
        layout.addWidget(self.equipTipsLabel, 100, 0, 1, 6)
        self.equipButton = QPushButton('全部装备')
        layout.addWidget(self.equipButton, 101, 0, 1, 6)

        # 注册事件
        self.programmeCombobox.currentIndexChanged.connect(self.programmeCurrentIndexChanged)
        self.equipButton.clicked.connect(self.allEquip)
        self.copyButton.clicked.connect(self.copyScore)

    def updateUI(self):
        oldArtifactsData = self.data.getArtifactOwner(self.character)
        newArtifactsData = self.resultArray[self.programmeCombobox.currentIndex()]["combinationName"]
        self.score_array = [] # 重置得分数组
        for posItem in self.data.getPosName():
            oldScore = 0
            if posItem in oldArtifactsData:
                self.artifactNameLabel1[posItem].setText(oldArtifactsData[posItem])

                oldArtifactItem = self.data.getArtifactItem(posItem, oldArtifactsData[posItem])
                if "subAttr" in oldArtifactItem:
                    oldScore = self.data.newScore(oldArtifactItem, self.character)[1]
                self.artifactScoreLabel1[posItem].setText(str(oldScore))

            if posItem in newArtifactsData:
                self.artifactNameLabel2[posItem].setText(newArtifactsData[posItem])
                newArtifactItem = self.data.getArtifactItem(posItem, newArtifactsData[posItem])
                newScore = self.data.newScore(newArtifactItem, self.character)[1]
                self.score_array.append(newScore)
                self.artifactScoreLabel2[posItem].setText(str(newScore))

                ownerCharacter = self.data.getOwnerCharacterByArtifactId(posItem, newArtifactsData[posItem])
                if ownerCharacter:
                    newOwnerStr = ownerCharacter
                else:
                    newOwnerStr = "无人装备"
                self.artifactOwnerLabel2[posItem].setText(newOwnerStr)

            if newOwnerStr != "无人装备" and newOwnerStr != self.character:
                newOwnerScore = self.data.newScore(newArtifactItem, newOwnerStr)[1]
                self.artifactOwnerLabel1[posItem].setText(str(newOwnerScore))
            else:
                self.artifactOwnerLabel1[posItem].setText("")

            scoreSub = round(newScore - oldScore, 1)
            if scoreSub > 0:
                scoreSub = "+" + str(scoreSub)
                scoreStyle = "color:green;"
            elif scoreSub < 0:
                scoreStyle = "color:red;"
            else:
                scoreStyle = "color:black;"
            self.artifactScoreSubLabel[posItem].setText(str(scoreSub))
            self.artifactScoreSubLabel[posItem].setStyleSheet(scoreStyle)

    def update(self, character, array):
        self.character = character
        self.resultArray = array
        # 添加下拉框item
        self.programmeCombobox.clear()
        for item in self.resultArray:
            tempKey = item["combinationType"] + "_" + str(item["scoreSum"])
            self.programmeCombobox.addItem(tempKey)

    # 英雄名称
    def programmeCurrentIndexChanged(self):
        self.updateUI()


    def equip(self):
        posItem = self.sender().objectName()
        self.equipTipsLabel.setText(self.character + " 已装备 " + posItem)
        newArtifactsData = self.resultArray[self.programmeCombobox.currentIndex()]["combinationName"]
        newArtifactsItem = {posItem: newArtifactsData[posItem]}
        self.data.setArtifactOwner(self.character, newArtifactsItem)
        self.updateUI()

    # 全部装备
    def allEquip(self):
        # print("全部装备")
        self.equipTipsLabel.setText(self.character + "已全部装备")
        newArtifactsData = self.resultArray[self.programmeCombobox.currentIndex()]["combinationName"]
        self.data.setArtifactOwner(self.character, newArtifactsData)
        self.updateUI()

    # 复制得分到剪切板
    def copyScore(self):
        # 复制文本到剪贴板
        text_to_copy = "	".join(str(score) for score in self.score_array)
        pyperclip.copy(text_to_copy)
        self.equipTipsLabel.setText("得分已复制到剪切板")
