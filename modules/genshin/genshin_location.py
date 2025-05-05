from modules.base.base_location import BaseLocation


class Location(BaseLocation):
    def __init__(self):
        super().__init__({
            "gameKey": "genshin",
            "1920x1080": {
                # 背包面板
                "bag": {
                    # 第一个贴图位置及每次偏移量
                    "x_initial": 196,
                    "y_initial": 301,
                    "x_offset": 146,
                    "y_offset": 175,
                    # 第一个圣遗物位置
                    "x_left": 106,
                    "x_right": 252,
                    "y_top": 167,
                    "y_bottom": 342,
                    # 截图位置 数组形式以便排除干扰区域
                    "x_grab": [1309, 1309],
                    "y_grab": [119, 403],
                    "w_grab": [287, 367],
                    "h_grab": [284, 227],
                    # 圣遗物行列数
                    "row": 4,
                    "col": 8
                },
                # 角色面板
                "character": {
                    # 第一个贴图位置及每次偏移量
                    "x_initial": 117,
                    "y_initial": 248,
                    "x_offset": 142,
                    "y_offset": 169,
                    # 第一个圣遗物位置
                    "x_left": 28,
                    "x_right": 170,
                    "y_top": 117,
                    "y_bottom": 286,
                    # 截图位置 数组形式以便排除干扰区域
                    "x_grab": [1459, 1459],
                    "y_grab": [112, 207],
                    "w_grab": [327, 413],
                    "h_grab": [95, 279],
                    # 圣遗物行列数
                    "row": 5,
                    "col": 4
                }
            }
        })


location = Location()
