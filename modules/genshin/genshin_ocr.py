'''图像识别、文字处理，考虑多种ocr方式'''

import re
from modules.base.base_ocr import BaseOCR
from utils import markPrint, strReplace


class OCR(BaseOCR):
    def __init__(self):
        self.data_length = 9
        self.replace_dict_name = {
            '明威之': '明威之镡',
            '无边醋乐之笼': '无边酣乐之筵',
            '无边醋乐之筵': '无边酣乐之筵',
            '浮溯之玉': '浮溯之珏',
            '阳之遗': '阳辔之遗',
            '遮雷之姿': '虺雷之姿',
            '他雷之姿': '虺雷之姿',
            '海祗之冠': '海祇之冠',
            '海低之冠': '海祇之冠',
            '海张之冠': '海祇之冠',
            '蛋笑之面': '嗤笑之面',
            '金铜时唇': '金铜时晷',
            '将帅兜': '将帅兜鍪',
            '雷灾的子遗': '雷灾的孑遗',
            '星罗圭璧之唇': '星罗圭璧之晷',
            '魔岩琢塑之樽': '巉岩琢塑之樽',
            '宗室银瓷': '宗室银瓮'
        }

        super().__init__()

    def process_result(self, result):
        result = super().process_result(result)

        # 原神数据不进行矫正
        is_corrected = False

        # 校验数据长度
        if len(result) != self.data_length:
            markPrint("数据长度不符合要求", result)
            return False

        # 千位符（含误识别的.）兼容
        pattern_thou = '\d\.\d{3}|\d\,\d{3}'
        txt = [re.sub(pattern_thou, item.replace(',', '').replace('.', ''), item) for item in result]

        name = strReplace(txt[0], self.replace_dict_name)
        parts = txt[1]
        main_name = txt[2]
        main_digit = txt[3]
        lvl = re.findall(r'\d+', txt[4])[0]
        result = {
            'name': name,
            'parts': parts,
            'mainTag': main_name,
            'mainDigit': main_digit,
            'lvl': lvl,
            "isCorrected": is_corrected
        }

        # 中文和数字正则
        pattern_chinese = '[\u4e00-\u9fa5]+'
        pattern_digit = '\d+(\.\d+)?'

        normalTags = {}
        for item in txt[-4:]:
            try:
                # 词条名称
                name = re.findall(pattern_chinese, item)[0]
                # 数值 兼容千位符被识别为小数点的情况
                digit = float(re.search(pattern_digit, item).group())
                if digit < 2: digit *= 1000

                if name in '暴击率':
                    normalTags['暴击率'] = digit
                elif name in '暴击伤害':
                    normalTags['暴击伤害'] = digit
                elif name in '攻击力' and '%' in item:
                    normalTags['攻击力百分比'] = digit
                elif name in '攻击力':
                    normalTags['攻击力'] = digit
                elif name in '生命值' and '%' in item:
                    normalTags['生命值百分比'] = digit
                elif name in '生命值':
                    normalTags['生命值'] = digit
                elif name in '防御力' and '%' in item:
                    normalTags['防御力百分比'] = digit
                elif name in '防御力':
                    normalTags['防御力'] = digit
                elif name in '元素精通':
                    normalTags['元素精通'] = digit
                elif name in '元素充能效率':
                    normalTags['元素充能效率'] = digit
                else:
                    normalTags[item] = 0
            except:
                normalTags[item] = 0
        result["normalTags"] = normalTags

        markPrint(result)
        return result


ocr = OCR()
