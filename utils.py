'''工具方法文件'''
import json
import inspect
import win32gui
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


# 纠错工具
class SpellCorrector:
    def __init__(self, dictionary, max_distance=2):
        self.dictionary = dictionary
        self.max_distance = max_distance

    def correct_word(self, word):
        # 如果单词正确，直接返回
        if word in self.dictionary:
            return word

        # 寻找最佳候选
        best_candidate = word
        min_distance = float('inf')

        for correct_word in self.dictionary:
            distance = self.levenshtein_distance(word, correct_word)
            if distance < min_distance and distance <= self.max_distance:
                min_distance = distance
                best_candidate = correct_word

        return best_candidate if min_distance <= self.max_distance else word

    def levenshtein_distance(self, s1, s2):
        # 使用上面的DP实现
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
                    dp[i - 1][j] + 1,  # 删除
                    dp[i][j - 1] + 1,  # 插入
                    dp[i - 1][j - 1] + cost  # 替换
                )
        return dp[m][n]

    def correct_text(self, text):
        """纠正整个文本"""
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

