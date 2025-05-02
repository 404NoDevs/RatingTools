'''遗器评分界面'''

from modules.base.base_score import BaseScoreWindow
from modules.starRail.starRail_location import location
from modules.starRail.starRail_ocr import ocr
from modules.starRail.starRail_data import data
from modules.starRail.starRail_score_result import ScoreResultWindow
from modules.starRail.starRail_suit import SuitWindow
from modules.starRail.starRail_set import SetWindow
from modules.starRail.starRail_analyze_result import AnalyzeResultWindow


class ScoreWindow(BaseScoreWindow):
    def __init__(self):
        super().__init__({
            "equipmentName": "遗器",
            "data": data,
            "location": location,
            "ocr": ocr,
            "ScoreResultWindow": ScoreResultWindow,
            "SuitWindow": SuitWindow,
            "SetWindow": SetWindow,
            "AnalyzeResultWindow": AnalyzeResultWindow
        })
