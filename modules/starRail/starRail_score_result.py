'''贴图窗口，显示单独的评分结果'''

from modules.base.base_score_result import BaseScoreResultWindow
from modules.starRail import starRail_location as location

class ScoreResultWindow(BaseScoreResultWindow):
    def __init__(self):
        super().__init__({
            "location":location
        })
