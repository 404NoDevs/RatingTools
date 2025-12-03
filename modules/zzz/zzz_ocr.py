'''图像识别、文字处理，考虑多种ocr方式'''

import re
from collections import OrderedDict
from modules.base.base_ocr import BaseOCR
from modules.zzz.zzz_data import data
from utils import markPrint, SpellCorrector


class OCR(BaseOCR):
    def __init__(self):
        super().__init__({
            "error_text": ["S", "s", "A", "a", "主属性", "副属性", "?",
                           "1", "2", "3", "4", "5", "6",
                           "+1", "+2", "+3", "+4", "+5",
                           "1+1", "1+2", "1+3", "1+4", "1+5",
                           "直+1", "直+2", "直+3", "直+4", "直+5"
                           ]
        })

        self.data_length = 12
        self.nameSpellCorrector = SpellCorrector(data.getArtifactNameDict())
        self.mainAttrSpellCorrector = SpellCorrector(data.getMainAttrDict())

    def process_result(self, result):
        # 公共处理
        result = super().process_result(result)

        new_result = {}
        is_corrected = False
        # 矫正规则一 属性识别失败进行补9(只有9无需手动补齐)
        i = 5
        s = r'^\d+(\.\d+)?%?$|^%$'
        while i < len(result):
            if i % 2 == 1 and re.match(s, result[i]) is None:
                result.insert(i, "9")
                is_corrected = False
                i += 1  # 跳过插入的元素
            i += 1  # 继续下一个元素
        # 防止丢失元素在最后一位
        if re.match(s, result[-1]) is None:
            result.append("9")
            is_corrected = False
        new_result["isCorrected"] = is_corrected

        # 校验数据长度
        if len(result) != self.data_length:
            markPrint("数据长度不符合要求", result)
            return False

        markPrint("数据整理前检查", result)
        temp_list = result[0].replace("【", "[").split("[")
        new_result["name"] = self.nameSpellCorrector.correct_word(temp_list[0])
        new_result["parts"] = "分区" + temp_list[1][0]
        new_result["mainAttr"] = self.mainAttrSpellCorrector.correct_word(result[2])
        new_result["mainDigit"] = result[3]
        if new_result["mainAttr"] in ["攻击力", "生命值", "防御力"] and "%" in new_result["mainDigit"]:
            new_result["mainAttr"] += "百分比"
        new_result["lvl"] = re.findall(r'\d+', result[1])[0]

        # 中文和数字正则
        subAttr = {}
        pattern_chinese = '[\u4e00-\u9fa5]+'
        pattern_digit = r'\d+(\.\d+)?'
        for index in range(4, len(result), 2):
            item = result[index] + result[index + 1]
            temp_name = result[index]
            temp_digit = result[index + 1]
            try:
                # 词条名称
                name = re.findall(pattern_chinese, temp_name)[0]
                # 数值 兼容千位符被识别为小数点的情况
                digit = float(re.search(pattern_digit, temp_digit).group())

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
                elif name in '异常精通':
                    subAttr['异常精通'] = digit
                elif name in '穿透值':
                    subAttr['穿透值'] = digit
                else:
                    subAttr[item] = 0
            except:
                subAttr[item] = 0
        new_result["subAttr"] = OrderedDict(subAttr)

        markPrint(new_result)
        return new_result


ocr = OCR()
