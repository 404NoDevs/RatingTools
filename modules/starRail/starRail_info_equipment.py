from modules.base.base_info_equipment import BaseInfoEquipmentWindow
from modules.starRail.starRail_data import data


class EquipmentInfoWindow(BaseInfoEquipmentWindow):
    def __init__(self):
        super().__init__({
            "data": data,
            "position": (310, 0),
            "size": (865, 990),
            "suitArray": ["suitA", "suitB", "suitC"],
            "widthList": [110, 85, 125]
        })
