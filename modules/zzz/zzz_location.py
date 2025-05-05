from modules.base.base_location import BaseLocation


class Location(BaseLocation):
    def __init__(self):
        super().__init__({
            "gameKey": "zzz",
            "1920x1080": {
                # 背包面板
                "bag": {
                    # 第一个贴图位置及每次偏移量
                    "x_initial": 275,
                    "y_initial": 321,
                    "x_offset": 142,
                    "y_offset": 181,
                    # 第一个圣遗物位置
                    "x_left": 192,
                    "x_right": 334,
                    "y_top": 220,
                    "y_bottom": 401,
                    # 截图位置 数组形式以便排除干扰区域
                    "x_grab": [1396, 1396],
                    "y_grab": [194, 387],
                    "w_grab": [259, 448],
                    "h_grab": [193, 321],
                    # 圣遗物行列数
                    "row": 4,
                    "col": 8
                },
                # 角色面板
                "character": {
                    # 第一个贴图位置及每次偏移量
                    "x_initial": 148,
                    "y_initial": 205,
                    "x_offset": 130,
                    "y_offset": 171,
                    # 第一个圣遗物位置
                    "x_left": 74,
                    "x_right": 204,
                    "y_top": 114,
                    "y_bottom": 285,
                    # 截图位置 数组形式以便排除干扰区域
                    "x_grab": [600],
                    "y_grab": [102],
                    "w_grab": [394],
                    "h_grab": [485],
                    # 圣遗物行列数
                    "row": 5,
                    "col": 4
                }
            }
        })


location = Location()
