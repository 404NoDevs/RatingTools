'''图像识别、文字处理，考虑多种ocr方式'''

import re
from modules.base.base_ocr import BaseOCR
from utils import markPrint, strReplace


class OCR(BaseOCR):
    def __init__(self):
        super().__init__({
            "error_text": []
        })

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

    def process_result(self, result):
        # 公共处理
        result = super().process_result(result)

        new_result = {}
        # 原神数据不进行矫正
        is_corrected = False
        new_result["isCorrected"] = is_corrected

        # 校验数据长度
        if len(result) != self.data_length:
            markPrint("数据长度不符合要求", result)
            return False

        new_result["name"] = strReplace(result[0], self.replace_dict_name)
        new_result["parts"] = result[1]
        new_result["mainTag"] = result[2]
        new_result["mainDigit"] = result[3]
        new_result["lvl"] = re.findall(r'\d+', result[4])[0]

        # 中文和数字正则
        normalTags = {}
        pattern_chinese = '[\u4e00-\u9fa5]+'
        pattern_digit = '\d+(\.\d+)?'
        for item in result[-4:]:
            try:
                # 词条名称
                name = re.findall(pattern_chinese, item)[0]
                # 数值 兼容千位符被识别为小数点的情况
                digit = float(re.search(pattern_digit, item).group())

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
        new_result["normalTags"] = normalTags

        markPrint(new_result)
        return new_result

ocr = OCR()
