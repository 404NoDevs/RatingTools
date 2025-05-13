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


def strReplace(old_str, replacements):
    new_str = old_str
    for wrong, right in replacements.items():
        new_str = new_str.replace(wrong, right)
    return new_str


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
