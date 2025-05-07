'''设置窗口，自定义词条收益权重'''

from modules.base.base_set import BaseSetWindow
from modules.genshin.genshin_data import data


class SetWindow(BaseSetWindow):
    def __init__(self, parent=None):
        super().__init__({
            "parent": parent,
            "data": data,
            "position": [340, 0]
        })
