from modules.base.base_suit_result import BaseSuitResultWindow
from modules.starRail.starRail_data import data


class SuitResultWindow(BaseSuitResultWindow):
    def __init__(self):
        super().__init__({
            "data": data,
            "position": [0, 450]
        })
