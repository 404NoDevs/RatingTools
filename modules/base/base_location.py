import win32gui

from PySide6.QtGui import QGuiApplication


class BaseLocation():
    def __init__(self, params):
        self.window_type = params.get('window_type', 'UnityWndClass')
        self.window_name = params.get('window_name', '原神')
        self.SCALE = QGuiApplication.instance().devicePixelRatio()

        # 游戏窗口信息获取
        self.window = win32gui.FindWindow(self.window_type, self.window_name)
        # self.window_start = win32gui.FindWindow('START Cloud Game', 'START云游戏-Game')
        # self.window = self.window_sc or self.window_start
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.window)

        self.w_left = self.left
        self.w_top = self.top
        self.w_width = self.right - self.left - 3 * self.SCALE
        self.w_hight = self.bottom - self.top - 26 * self.SCALE

        if self.w_hight != 0:
            self.ratio = self.w_width / self.w_hight
        else:
            self.ratio = 1

