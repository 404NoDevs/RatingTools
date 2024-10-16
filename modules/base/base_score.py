'''圣遗物评分界面'''

import os
from pynput import keyboard
from extention import OutsideMouseManager
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QRadioButton,
    QPushButton,
    QWidget,
    QGridLayout,
    QComboBox
)


class BaseScoreWindow(QWidget):

    def __init__(self, params):
        super().__init__()

        # 获取子类参数
        self.equipment_name = params.get('equipmentName', "圣遗物")
        self.data = params.get('data')
        self.location = params.get('location')
        self.ocr = params.get('ocr')
        self.ScoreResultWindow = params.get('ScoreResultWindow')
        self.SuitWindow = params.get('SuitWindow')
        self.SetWindow = params.get('SetWindow')
        self.AnalyzeResultWindow = params.get('AnalyzeResultWindow')

        self.initData()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../../src/keqing.ico')))
        self.setWindowTitle(f"{self.equipment_name}评分工具")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(0, 0)

        # 背包/角色面板选择（Radio）
        self.radiobtn1 = QRadioButton('角色')
        self.radiobtn1.setChecked(True)
        self.radiobtn2 = QRadioButton('背包')
        self.type = '角色'
        self.suitButton = QPushButton('套装推荐→')
        # 角色选择框
        self.combobox = QComboBox()
        # 添加角色
        self.characters = self.data.getCharacters()
        for key in self.characters:
            self.combobox.addItem(key)
        # 设置按钮
        self.setButton = QPushButton('设置→')
        # 识别结果显示，初始配置
        self.name = []
        self.digit = []
        self.strengthen = []
        self.score = []
        for i in range(4):
            self.name.append(QLabel(''))
            text = QLineEdit("0")
            # text.setFixedWidth(50)
            text.setAlignment(Qt.AlignRight)
            self.digit.append(text)
            self.score.append(QLabel("0"))
            self.strengthen.append(QLabel("+0"))
            self.name[i].setText('副词条' + str(i + 1))
        self.modifyButton = QPushButton('确认修改')
        self.entries = QLabel('0')
        self.score_total = QLabel('0')
        # 提示文本
        self.tipsLabel = QLabel(f'请选择{self.equipment_name}，然后点击右键')
        self.tipsLabel.setStyleSheet("color:red;")
        # 分析按钮
        self.analyzeButton = QPushButton(f'{self.equipment_name}分析↓')
        # self.analyzeText

        # 弹窗内容
        layout = QGridLayout()
        layout.addWidget(self.radiobtn1, 0, 0)
        layout.addWidget(self.radiobtn2, 0, 1)
        layout.addWidget(self.suitButton, 0, 2, 1, 2)
        # 角色选择
        layout.addWidget(self.combobox, 1, 0, 1, 3)
        layout.addWidget(self.setButton, 1, 3, 1, 1)
        # 识别结果展示
        for i in range(4):
            layout.addWidget(self.name[i], i + 3, 0)
            layout.addWidget(self.digit[i], i + 3, 1)
            layout.addWidget(self.strengthen[i], i + 3, 2, Qt.AlignRight)
            layout.addWidget(self.score[i], i + 3, 3, Qt.AlignRight)
        # 修改按钮
        layout.addWidget(self.modifyButton, 10, 0, 1, 2)
        # 总分计算结果
        layout.addWidget(self.entries, 10, 2, 1, 1, Qt.AlignRight)
        layout.addWidget(self.score_total, 10, 3, 1, 1, Qt.AlignRight)
        # 提示文本
        layout.addWidget(self.tipsLabel, 11, 0, 1, 4, Qt.AlignCenter)
        # 分析按钮
        # layout.addWidget(self.analyzeButton, 12, 0, 1, 4, Qt.AlignCenter)

        self.setLayout(layout)

        ''' 事件链接 '''
        # 背包、角色单选
        self.radiobtn1.toggled.connect(lambda: self.radiobtn_state(self.radiobtn1))
        self.radiobtn2.toggled.connect(lambda: self.radiobtn_state(self.radiobtn2))
        # 套装推荐
        self.suitButton.clicked.connect(self.swich_suit_window)
        # 角色下拉框选择
        self.combobox.currentIndexChanged.connect(self.current_index_changed)
        # 设置弹窗
        self.setButton.clicked.connect(self.open_set_window)
        # 修改按钮
        self.modifyButton.clicked.connect(self.button_clicked)
        # 分析按钮
        self.analyzeButton.clicked.connect(self.analyzeButton_clicked)
        # 外部鼠标事件启动识别和贴图弹窗
        self.mouseManager = OutsideMouseManager()
        self.mouseManager.right_click.connect(self.open_new_window)
        self.mouseManager.left_click.connect(self.left_click_artifact)
        # 全局热键
        self.hotkey()

    def initData(self):
        self.character = '全属性'

        # 子窗口
        self.setWindow = None
        self.analyzeWindow = None

        # 默认坐标信息-角色B
        self.position = self.location.position_B
        self.row, self.col = self.location.row_B, self.location.col_B
        self.xarray, self.yarray = self.location.xarray_B, self.location.yarray_B
        self.x_grab, self.y_grab, self.w_grab, self.h_grab = self.location.x_grab_B, self.location.y_grab_B, self.location.w_grab_B, self.location.h_grab_B
        self.SCALE = self.location.SCALE

        # 预先设定好贴图窗口组&每一个窗口的圣遗物数据
        self.pastes = []
        self.id = -1
        # 当前屏幕中圣遗物坐标及副词条dict，{'0': {'暴击率': 2.0}, '2': {'暴击伤害': 4.0}}
        self.artifact = {}
        self.score_result = [[0, 0, 0, 0], 0, [0, 0, 0, 0], 0]
        for i in range(self.row * self.col):
            window = self.ScoreResultWindow()
            self.pastes.append(window)
            self.pastes[i].move(self.position[i][0] / self.SCALE, self.position[i][1] / self.SCALE)

    def closeEvent(self, event):
        # print("关闭窗口")
        pass

    def initParams(self):
        # print("初始化参数")
        pass

    # 单选框面板选择事件
    def radiobtn_state(self, btn):
        if btn.text() == '背包':
            if btn.isChecked() == True:
                self.type = '背包'
                # 重置坐标信息
                self.position = self.location.position_A
                self.row, self.col = self.location.row_A, self.location.col_A
                self.xarray, self.yarray = self.location.xarray_A, self.location.yarray_A
                self.x_grab, self.y_grab, self.w_grab, self.h_grab = self.location.x_grab_A, self.location.y_grab_A, self.location.w_grab_A, self.location.h_grab_A
                self.reset()

        if btn.text() == '角色':
            if btn.isChecked() == True:
                self.type = '角色'
                # 重置坐标信息
                self.position = self.location.position_B
                self.row, self.col = self.location.row_B, self.location.col_B
                self.xarray, self.yarray = self.location.xarray_B, self.location.yarray_B
                self.x_grab, self.y_grab, self.w_grab, self.h_grab = self.location.x_grab_B, self.location.y_grab_B, self.location.w_grab_B, self.location.h_grab_B
                self.reset()

    # 选择框选择角色事件
    def current_index_changed(self, index):
        self.character = self.combobox.currentText()

        # 更新评分贴图
        for i in range(len(self.pastes)):
            if self.pastes[i].isVisible() == True:
                self.score_result = self.data.newScore(self.artifact[str(i)], self.character)
                self.pastes[i].setLabel(self.score_result[1])

        # 更新主程序评分详情
        if self.artifact != {}:
            self.fresh_main_window()

        if self.setWindow:
            self.setWindow.update(self.character)

    # 修改识别结果按钮
    def button_clicked(self):
        if str(self.id) in self.artifact:
            self.artifact[str(self.id)]["subAttr"] = {}
            for i in range(4):
                self.artifact[str(self.id)]["subAttr"][self.name[i].text()] = float(self.digit[i].text())
            # 修改完成移除矫正标识
            self.artifact[str(self.id)]["isCorrected"] = False
            # 刷新界面
            self.fresh_main_window()
            self.fresh_paste_window()
        else:
            self.tipsLabel.setText("请先选择一个遗器")

    # 启动贴图弹窗
    def open_new_window(self, x, y):
        # 根据鼠标事件定位贴图
        for i in range(self.col):
            if x >= self.xarray[i][0] and x <= self.xarray[i][1]:
                for j in range(self.row):
                    if y >= self.yarray[j][0] and y <= self.yarray[j][1]:
                        print(self.character + 'detected')
                        # 插入模式后移数据
                        self.id = j * self.col + i
                        # ocr识别与结果返回并刷新主面板、贴图
                        self.id = j * self.col + i

                        ocrResult = self.ocr.rapidocr(self.x_grab, self.y_grab, self.w_grab, self.h_grab)
                        if ocrResult:
                            self.artifact[str(self.id)] = ocrResult
                            self.fresh_main_window()
                            self.fresh_paste_window()
                        else:
                            self.tipsLabel.setText("识别失败，请重试")
                        break
                break

    # 切换为套装推荐
    def swich_suit_window(self):
        global mainWindow
        mainWindow = self.SuitWindow({
            "character": self.character
        })
        mainWindow.show()
        self.close()

    # 根据鼠标左键选择的圣遗物刷新主窗口圣遗物副属性和评分
    def left_click_artifact(self, x, y):
        for i in range(self.col):
            if x >= self.xarray[i][0] and x <= self.xarray[i][1]:
                for j in range(self.row):
                    if y >= self.yarray[j][0] and y <= self.yarray[j][1]:
                        id_temp = j * self.col + i
                        if self.pastes[id_temp].isVisible() == True:
                            self.id = id_temp
                            self.fresh_main_window()
                            break
                break

    # 刷新主程序（识别、选择、切换角色、修改后确认、加载本地数据）
    def fresh_main_window(self):
        # 计算评分（计算很快就不另外储存了）
        self.score_result = self.data.newScore(self.artifact[str(self.id)], self.character)

        # 主窗口更新详细评分
        self.score_total.setText(str(self.score_result[1]))
        self.entries.setText(str(self.score_result[3]))
        for i in range(4):
            if i < len(self.artifact[str(self.id)]["subAttr"]):
                if list(self.artifact[str(self.id)]["subAttr"].keys())[i] in self.data.getCoefficient().keys():
                    self.name[i].setText(list(self.artifact[str(self.id)]["subAttr"].keys())[i])
                    self.digit[i].setText(str(list(self.artifact[str(self.id)]["subAttr"].values())[i]))
                    self.score[i].setText(str(self.score_result[0][i]))
                    self.strengthen[i].setText("+" + str(self.score_result[2][i]))
                else:
                    self.name[i].setText('识别错误')
                    self.digit[i].setText(list(self.artifact[str(self.id)]["subAttr"].keys())[i])
                    self.score[i].setText('0')
                    self.strengthen[i].setText("+0")
            else:
                self.name[i].setText('识别错误')
                self.digit[i].setText('0')
                self.score[i].setText('0')
                self.strengthen[i].setText("+0")

        if "isCorrected" in self.artifact[str(self.id)] and self.artifact[str(self.id)]["isCorrected"]:
            self.tipsLabel.setText("识别失败，请手动修改")
            print("识别异常，停止保存")
        else:
            self.tipsLabel.setText("评分成功")
            # 自动保存遗器
            self.data.saveArtifactList(self.artifact[str(self.id)])

    # 刷新圣遗物贴图（识别、修改后确认、加载本地数据,后于主面板更新）
    def fresh_paste_window(self):
        self.pastes[self.id].setLabel(self.score_result[1])
        self.pastes[self.id].show()

    # 重置圣遗物数据&贴图窗口&主程序窗口
    def reset(self):
        # 主程序重置
        self.id = -1

        for i in range(4):
            self.name[i].setText('副词条' + str(i + 1))
            self.digit[i].setText('0')
            self.score[i].setText('0')
            self.strengthen[i].setText("+0")
        self.score_total.setText('0')
        self.entries.setText('0')

        self.tipsLabel.setText(f'请选择{self.equipment_name}，然后点击右键')

        # 数据重置
        self.pastes = []
        self.artifact = {}
        for i in range(self.row * self.col):
            window = self.ScoreResultWindow()
            self.pastes.append(window)
            self.pastes[i].move(self.position[i][0] / self.SCALE, self.position[i][1] / self.SCALE)

    # 主窗口关闭则所有贴图窗口也关闭
    def closeEvent(self, event):
        for item in self.pastes:
            item.close()

        if self.setWindow:
            self.setWindow.close()
        if self.analyzeWindow:
            self.analyzeWindow.close()

        self.mouseManager.stop()
        self.hotKeyManager.stop()

    # 全局快捷键Ctrl+Shift+Z重置贴图窗口
    def hotkey(self):
        def on_activate():
            print('reset!')
            # self.reset() # 为啥这里调用就闪退
            self.id = -1
            self.artifact = {}

            for i in range(4):
                self.name[i].setText('副词条' + str(i + 1))
                # self.digit[i].setText('0')  # 不明原因引起闪退，reset()里也是因为这个
                self.score[i].setText('0')
                self.strengthen[i].setText("+0")
            self.score_total.setText('0')
            self.entries.setText('0')
            for item in self.pastes:
                item.hide()

            self.tipsLabel.setText(f'请选择{self.equipment_name}，然后点击右键')

        self.hotKeyManager = keyboard.GlobalHotKeys({'<ctrl>+<shift>+z': on_activate})
        self.hotKeyManager.start()

    def open_set_window(self):
        if not self.setWindow or not self.setWindow.isVisible():
            self.setWindow = self.SetWindow()
            self.setWindow.update(self.character)
            self.setWindow.show()
        else:
            self.setWindow.close()
            self.setWindow = None

    def initCombobox(self, character):
        index = self.data.getCharacterIndex(character)
        self.combobox.setCurrentIndex(index)

    def analyzeButton_clicked(self):
        if not self.analyzeWindow or not self.analyzeWindow.isVisible():
            self.analyzeWindow = self.AnalyzeResultWindow()
            self.analyzeWindow.update()
            self.analyzeWindow.show()
        else:
            self.analyzeWindow.close()
            self.analyzeWindow = None