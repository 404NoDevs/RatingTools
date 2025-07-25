'''图像识别、文字处理，考虑多种ocr方式'''

import re
from modules.base.base_ocr import BaseOCR
from utils import markPrint, strReplace


class OCR(BaseOCR):
    def __init__(self):
        super().__init__({
            "error_text": ["孩", "软"]
        })

        self.data_length = 13
        self.replace_dict_name = {
            '者的复明义眼': '莳者的复明义眼',
            '者的机巧木手': '莳者的机巧木手',
            '者的承露羽衣': '莳者的承露羽衣',
            '者的天人丝履': '莳者的天人丝履',
            '蔚者的机巧木手': '莳者的机巧木手',
            '勇烈的飞翎瓷申': '勇烈的飞翎瓷甲',
            '铁骑的银影装申': '铁骑的银影装甲',
            "哀地里亚的名祭碑": "哀地里亚的殁名祭碑",
            "诗人的萝花冠": "诗人的莳萝花冠",
            "神悟树庭的沉思巨根": "神悟树庭的沉思巨桹",

            '臂罐': '臂鞲',
            '臂購': '臂鞲',
            '臂講': '臂鞲',
            '绝足锁': '绝足锁桎',
            '黑塔，': '黑塔',
            '黑塔」': '黑塔',
            '圳裂缆索': '坼裂缆索',
            '系因': '系囚',
            '铅石桔': '铅石梏铐',
            '铅石枱': '铅石梏铐',
            '护腔': '护胫',
            '玄号': '玄枵',
            "器兽缰": "器兽缰辔",
            "司锋的": "司铎的"
        }
        self.replace_dict_parts = {
            '躯于': '躯干'
        }

    def process_result(self, result):
        # 公共处理
        result = super().process_result(result)

        new_result = {}
        is_corrected = False
        # 矫正规则一 属性识别失败进行补0
        i = 5
        s = r'^\d+(\.\d+)?%?$|^%$'
        while i < len(result):
            if i % 2 == 0 and re.match(s, result[i]) is None:
                result.insert(i, "0")
                is_corrected = True
                i += 1  # 跳过插入的元素
            i += 1  # 继续下一个元素
        # 防止丢失元素在最后一位
        if re.match(s, result[-1]) is None:
            result.append("0")
            is_corrected = True
        new_result["isCorrected"] = is_corrected

        # 校验数据长度
        if len(result) != self.data_length:
            markPrint("数据长度不符合要求", result)
            return False

        # print("11111111")
        # print(result)
        new_result["name"] = strReplace(result[0], self.replace_dict_name)
        new_result["parts"] = strReplace(result[1], self.replace_dict_parts)
        new_result["mainAttr"] = result[3]
        new_result["mainDigit"] = result[4]
        new_result["lvl"] = re.findall(r'\d+', result[2])[0]

        # 中文和数字正则
        subAttr = {}
        pattern_chinese = '[\u4e00-\u9fa5]+'
        pattern_digit = r'\d+(\.\d+)?'
        for index in range(5, len(result), 2):
            item = result[index] + result[index + 1]
            try:
                # 词条名称
                name = re.findall(pattern_chinese, item)[0]
                # 数值
                digit = float(re.search(pattern_digit, item).group())

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
                elif name in '速度':
                    subAttr['速度'] = digit
                elif name in '击破特攻':
                    subAttr['击破特攻'] = digit
                elif name in '效果命中':
                    subAttr['效果命中'] = digit
                elif name in '效果抵抗':
                    subAttr['效果抵抗'] = digit
                else:
                    subAttr[item] = 0
            except:
                subAttr[item] = 0
        new_result["subAttr"] = subAttr

        markPrint(new_result)
        return new_result


ocr = OCR()
