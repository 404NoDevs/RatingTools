'''圣遗物评分界面'''

from modules.base.base_score import BaseScoreWindow
from modules.genshin.genshin_location import location
from modules.genshin.genshin_ocr import ocr
from modules.genshin.genshin_data import data
from modules.genshin.genshin_score_result import ScoreResultWindow
from modules.genshin.genshin_suit import SuitWindow
from modules.genshin.genshin_set import SetWindow
from modules.genshin.genshin_analyze_result import AnalyzeResultWindow


class ScoreWindow(BaseScoreWindow):
    def __init__(self):
        super().__init__({
            "equipmentName": "圣遗物",
            "data": data,
            "location": location,
            "ocr": ocr,
            "ScoreResultWindow": ScoreResultWindow,
            "SuitWindow": SuitWindow,
            "SetWindow": SetWindow,
            "AnalyzeResultWindow": AnalyzeResultWindow
        })
