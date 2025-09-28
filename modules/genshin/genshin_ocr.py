'''图像识别、文字处理，考虑多种ocr方式'''

import re
from collections import OrderedDict
from modules.base.base_ocr import BaseOCR
from modules.genshin.genshin_data import data
from utils import markPrint, SpellCorrector


class OCR(BaseOCR):
    def __init__(self):
        super().__init__({
            "error_text": []
        })

        self.data_length = 9
        self.nameSpellCorrector = SpellCorrector(data.getArtifactNameDict())
        self.partsSpellCorrector = SpellCorrector(data.getArtifactPosDict())
        self.mainAttrSpellCorrector = SpellCorrector(data.getMainAttrDict())

    def process_result(self, result):
        # 公共处理
        result = super().process_result(result)

        new_result = {}
        is_corrected = False
        new_result["isCorrected"] = is_corrected

        # 校验数据长度
        if len(result) != self.data_length:
            markPrint("数据长度不符合要求", result)
            return False

        new_result["name"] = self.nameSpellCorrector.correct_word(result[0])
        new_result["parts"] = self.partsSpellCorrector.correct_word(result[1])
        new_result["mainAttr"] = self.mainAttrSpellCorrector.correct_word(result[2])
        new_result["mainDigit"] = result[3]
        new_result["lvl"] = re.findall(r'\d+', result[4])[0]

        # 中文和数字正则
        subAttr = {}
        for item in result[-4:]:
            try:
                # 词条名称
                name = re.findall('[\u4e00-\u9fa5]+', item)[0]
                # 数值
                digit = float(re.search(r'\d+(\.\d+)?', item).group())

                if name in '暴击率':
                    subAttr['暴击率'] = digit
                elif name in '暴击伤害':
                    subAttr['暴击伤害'] = digit
                elif name in '攻击力' and '%' in item:
                    subAttr['攻击力百分比'] = digit
                elif name in '攻击力':
                    subAttr['攻击力'] = digit
                elif name in '生命值' and '%' in item:
                    subAttr['生命值百分比'] = digit
                elif name in '生命值':
                    subAttr['生命值'] = digit
                elif name in '防御力' and '%' in item:
                    subAttr['防御力百分比'] = digit
                elif name in '防御力':
                    subAttr['防御力'] = digit
                elif name in '元素精通':
                    subAttr['元素精通'] = digit
                elif name in '元素充能效率':
                    subAttr['元素充能效率'] = digit
                else:
                    subAttr[item] = 0
            except:
                subAttr[item] = 0
        new_result["subAttr"] = OrderedDict(subAttr)

        markPrint(new_result)
        return new_result


ocr = OCR()
