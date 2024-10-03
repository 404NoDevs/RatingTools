'''工具方法文件'''
import win32gui
import globalsData

def getKeyByValue(dict, val):
    for key, value in dict.items():
        if value == val:
            return key
    return None

def checkWinow(gameKey):
    windowParams = globalsData.gamesWindowParams[gameKey]
    window_sc = win32gui.FindWindow(windowParams[0], windowParams[1])
    return window_sc != 0

def strReplace(str, replacements):
    for old, new in replacements.items():
        str = str.replace(old, new)
    return str

def markPrint(*str,mark="*"):
    markStr = mark * 100
    print(markStr)
    for item in str:
        print(item)
    print(markStr)