from modules.base.base_location import BaseLocation


class Location(BaseLocation):
    def __init__(self):
        super().__init__({
            "gameKey": "starRail",
            "1920x1080": {
                # 背包面板
                "bag": {
                    # 第一个贴图位置及每次偏移量
                    "x_initial": 200,
                    "y_initial": 306,
                    "x_offset": 125,
                    "y_offset": 149,
                    # 第一个圣遗物位置
                    "x_left": 126,
                    "x_right": 251,
                    "y_top": 194,
                    "y_bottom": 343,
                    # 截图位置 数组形式以便排除干扰区域
                    "x_grab": [1384, 1384],
                    "y_grab": [113, 377],
                    "w_grab": [400, 481],
                    "h_grab": [264, 229],
                    # 圣遗物行列数
                    "row": 5,
                    "col": 9
                },
                # 角色面板
                "character": {
                    # 第一个贴图位置及每次偏移量
                    "x_initial": 112,
                    "y_initial": 304,
                    "x_offset": 125,
                    "y_offset": 149,
                    # 第一个圣遗物位置
                    "x_left": 37,
                    "x_right": 162,
                    "y_top": 192,
                    "y_bottom": 341,
                    # 截图位置 数组形式以便排除干扰区域
                    "x_grab": [1478, 1478],
                    "y_grab": [160, 288],
                    "w_grab": [360, 424],
                    "h_grab": [128, 203],
                    # 圣遗物行列数
                    "row": 5,
                    "col": 4
                }
            }
        })


location = Location()
