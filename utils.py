'''工具方法文件'''
# 导入系统文件
import json
import inspect
import win32gui
# 导入PySide6文件
from PySide6.QtGui import QColor, QStandardItem
# 导入自定义文件
import globalsData


def getKeyByValue(dict, val):
    for key, value in dict.items():
        if value == val:
            return key
    return None


def checkWinowState(gameKey):
    """
    检查指定游戏窗口的状态。

    参数:
    gameKey (str): 用于从全局数据中获取窗口参数的键。

    返回:
    int:
        0 - 窗口存在且宽高比正常。
        1 - 窗口不存在。
        2 - 窗口没有适配
    """
    windowParams = globalsData.gamesWindowParams[gameKey]
    window = win32gui.FindWindow(*windowParams)
    if window == 0:
        return 1
    client_rect = win32gui.GetClientRect(window)
    client_size = (client_rect[2], client_rect[3])
    adaptedSizes = globalsData.adaptedSizes
    if client_size not in adaptedSizes:
        return 2
    return 0


def markPrint(*str, mark="*", title="未命名"):
    markStr = mark * 40 + title + mark * 40
    print(markStr)
    for item in str:
        if isinstance(item, (dict, list)):
            item = json.dumps(item, indent=4, ensure_ascii=False)
        print(item)
    print(markStr)


def debugPrint(*str):
    # 获取当前栈帧
    frame = inspect.currentframe()
    # 获取调用的上一层栈帧
    caller_frame = frame.f_back.f_back
    # 获取文件名、行号和函数名
    filename = caller_frame.f_code.co_filename
    line_number = caller_frame.f_lineno
    function_name = caller_frame.f_code.co_name

    markPrint(filename, line_number, function_name, *str, mark="--debug")


# 字典纠错工具
class SpellCorrector:
    def __init__(self, dictionary, max_distance=3):
        self.dictionary = dictionary
        self.max_distance = max_distance
        self.length_groups = {}
        for word in dictionary:
            length = len(word)
            if length not in self.length_groups:
                self.length_groups[length] = []
            self.length_groups[length].append(word)

    def __get_candidate_words(self, word):
        """获取候选词，限制搜索范围提高效率"""
        word_len = len(word)
        candidates = []

        # 搜索长度相近的单词
        for length in range(max(1, word_len - 2), word_len + 3):
            if length in self.length_groups:
                candidates.extend(self.length_groups[length])

        return candidates

    @staticmethod
    def __character_overlap(s1, s2):
        """计算字符重叠度，对丢字情况更敏感"""
        set1, set2 = set(s1), set(s2)
        intersection = set1 & set2
        union = set1 | set2
        return len(intersection) / len(union) if union else 0

    @staticmethod
    def __length_similarity(s1, s2):
        """计算长度相似度"""
        len1, len2 = len(s1), len(s2)
        return 1 - abs(len1 - len2) / max(len1, len2)

    @staticmethod
    def __levenshtein_distance(s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost
                )
        return dp[m][n]

    # 对单词进行字典纠错
    def correct_word(self, word):
        if word in self.dictionary:
            return word

        candidates = self.__get_candidate_words(word)

        if not candidates:
            return word

        # 使用多种策略选择最佳候选词
        scored_candidates = []

        for candidate in candidates:
            # 策略1: 编辑距离
            edit_distance = self.__levenshtein_distance(word, candidate)

            # 策略2: 字符重叠度（对丢字情况更敏感）
            overlap_score = self.__character_overlap(word, candidate)

            # 策略3: 长度相似度
            length_similarity = self.__length_similarity(word, candidate)

            # 综合评分（可根据需要调整权重）
            combined_score = (
                    0.6 * (1 - edit_distance / max(len(word), len(candidate))) +
                    0.3 * overlap_score +
                    0.1 * length_similarity
            )

            scored_candidates.append((candidate, combined_score, edit_distance))

        # 选择综合评分最高的候选词
        scored_candidates.sort(key=lambda x: (x[1], -x[2]), reverse=True)

        best_candidate, best_score, best_distance = scored_candidates[0]

        return best_candidate if best_distance <= self.max_distance else word

    # 对文本进行字典纠错
    def correct_text(self, text):
        words = text.split()
        corrected_words = [self.correct_word(word) for word in words]
        return ' '.join(corrected_words)


# 事件管理器
class EventManager:
    # 事件名称
    MOVE_MOUSE = "move_Mouse",

    def __init__(self):
        self._listeners = {}

    def register(self, event_type, listener):
        """注册事件监听器"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unregister(self, event_type, listener=None):
        """取消注册事件监听器"""
        if event_type in self._listeners:
            if listener:
                self._listeners[event_type].remove(listener)
            else:
                del self._listeners[event_type]

    def emit(self, event_type, *args, **kwargs):
        """触发事件"""
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(*args, **kwargs)


event_manager = EventManager()


# 设置交替行颜色
def setColor(model, divisor):
    for row in range(model.rowCount()):
        color = QColor(240, 240, 240) if (row // divisor) % 2 == 0 else QColor(255, 255, 255)
        for col in range(model.columnCount()):
            standardItem = model.item(row, col)
            if not standardItem:
                standardItem = QStandardItem()
                model.setItem(row, col, standardItem)

            if standardItem.background().color() == QColor(0, 0, 0, 255):
                standardItem.setBackground(color)


# 设置表格文本
def dealTableText(text, item, unit="个"):
    textList = text.split("\n")[1:]
    textList.append(item)
    textList.insert(0, str(len(textList)) + unit)
    return "\n".join(textList)
