'''贴图窗口，显示单独的评分结果'''

from modules.base.base_score_result import BaseScoreResultWindow
from modules.starRail.starRail_location import location


class ScoreResultWindow(BaseScoreResultWindow):
    def __init__(self):
        super().__init__({
            "location": location
        })
