import win32gui
import globalsData
from PySide6.QtGui import QGuiApplication


class BaseLocation:
    def __init__(self, params):
        self.window_type = params.get('window_type', 'UnityWndClass')
        self.window_name = params.get('window_name', '原神')
        self.config_1920x1080 = params.get('1920x1080', {})

        self.SCALE = 0
        self.client_x = 0
        self.client_y = 0
        self.client_w = 0
        self.client_h = 0
        self.config = {}

        self.initData()

    def initData(self):
        self.SCALE = QGuiApplication.instance().devicePixelRatio()

        # 游戏窗口信息获取
        window = win32gui.FindWindow(self.window_type, self.window_name)
        # self.window_start = win32gui.FindWindow('START Cloud Game', 'START云游戏-Game')
        # self.window = self.window_sc or self.window_start

        if window:
            # 将客户区左上角转换为屏幕坐标
            self.client_x, self.client_y = win32gui.ClientToScreen(window, (0, 0))
            print(f"Client area top-left in screen coordinates: ({self.client_x}, {self.client_y})")

            # 获取客户区大小（不含标题栏，但仅返回宽高，左上角是0,0）
            client_rect = win32gui.GetClientRect(window)
            self.client_w, self.client_h = client_rect[2], client_rect[3]
            client_size = f"{self.client_w}x{self.client_h}"
            if client_size == "1920x1080":
                print("1920x1080")
                self.config = self.config_1920x1080
            else:
                print(client_size + " 未适配")
        else:
            print("窗口未找到")

    def countData(self, config):

        # 第一个贴图位置及每次偏移量
        x_initial = self.client_x + config["x_initial"]
        y_initial = self.client_y + config["y_initial"]
        x_offset = config["x_offset"]
        y_offset = config["y_offset"]

        # print("x_initial", x_initial)
        # print("y_initial", y_initial)
        # print("x_offset", x_offset)
        # print("y_offset", y_offset)

        # 第一个圣遗物位置
        x_left = self.client_x + config["x_left"]
        x_right = self.client_x + config["x_right"]
        y_top = self.client_y + config["y_top"]
        y_bottom = self.client_y + config["y_bottom"]

        x_grab = []
        y_grab = []
        w_grab = []
        h_grab = []
        for index in range(len(config["x_grab"])):
            x_grab.append(self.client_x + config["x_grab"][index])
            y_grab.append(self.client_y + config["y_grab"][index])
            w_grab.append(config["w_grab"][index])
            h_grab.append(config["h_grab"][index])

        # print("x_grab", x_grab)
        # print("y_grab", y_grab)
        # print("w_grab", w_grab)
        # print("h_grab", h_grab)

        row = config["row"]
        col = config["col"]

        # print("row", row)
        # print("col", col)

        # 贴图坐标组
        position = []
        for i in range(row):
            for j in range(col):
                item = x_initial + j * x_offset, y_initial + i * y_offset
                position.append(item)
        # print("position", position)

        # 鼠标事件有效坐标区间
        xarray = []
        for i in range(col):
            item = (x_left + i * x_offset) / self.SCALE, (x_right + i * x_offset) / self.SCALE
            xarray.append(item)
        # print("xarray", xarray)

        yarray = []
        for i in range(row):
            item = (y_top + i * y_offset) / self.SCALE, (y_bottom + i * y_offset) / self.SCALE
            yarray.append(item)
        # print("yarray", yarray)

        return {
            # 贴图坐标组
            "position": position,

            # 鼠标事件有效坐标区间
            "xarray": xarray,
            "yarray": yarray,

            # 截图坐标
            "x_grab": x_grab,
            "y_grab": y_grab,
            "w_grab": w_grab,
            "h_grab": h_grab,

            # 行列数
            "row": row,
            "col": col
        }

    def getData(self, data_type='bag'):
        result = {}
        if data_type in self.config:
            result = self.countData(self.config[data_type])
        else:
            print("未适配 " + data_type + " 界面")
        return result

    def getScale(self):
        return self.SCALE

    def getFitterScale(self):
        scale = min(
            self.client_w / globalsData.REF_WIDTH,
            self.client_h / globalsData.REF_HEIGHT
        )
        return scale
