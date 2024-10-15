'''工具方法文件'''
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
        2 - 窗口不是1920*1080
    """
    windowParams = globalsData.gamesWindowParams[gameKey]
    window = win32gui.FindWindow(*windowParams)
    if window == 0:
        return 1
    left, top, right, bottom = win32gui.GetWindowRect(window)
    ratio = (right - left) / (bottom - top)
    if ratio < 1.7 or ratio > 1.8:
        return 2
    return 0


def strReplace(str, replacements):
    for wrong, right in replacements.items():
        str = str.replace(wrong, right)
    return str


def markPrint(*str, mark="*"):
    markStr = mark * 100
    print(markStr)
    for item in str:
        print(item)
    print(markStr)
