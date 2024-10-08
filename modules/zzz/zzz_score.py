'''圣遗物评分界面'''
from modules.base.base_score import BaseScoreWindow
from modules.zzz import zzz_location as location
from modules.zzz.zzz_ocr import ocr
from modules.zzz.zzz_data import data
from modules.zzz.zzz_score_result import ScoreResultWindow
from modules.zzz.zzz_suit import SuitWindow
from modules.zzz.zzz_set import SetWindow


class ScoreWindow(BaseScoreWindow):
    def __init__(self):
        super().__init__({
            "equipmentName": "光驱",
            "data": data,
            "location": location,
            "ocr": ocr,
            "ScoreResultWindow": ScoreResultWindow,
            "SuitWindow": SuitWindow,
            "SetWindow": SetWindow
        })
