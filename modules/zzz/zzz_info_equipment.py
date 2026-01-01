from modules.base.base_info_equipment import BaseInfoEquipmentWindow
from modules.zzz.zzz_data import data


class EquipmentInfoWindow(BaseInfoEquipmentWindow):
    def __init__(self):
        super().__init__({
            "data": data,
            "position": (310, 0),
            "size": (770, 990),
            "suitArray": ["suitA", "suitB"],
            "widthList": [90, 70, 110]
        })
