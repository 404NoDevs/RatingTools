'''图像识别、文字处理，考虑多种ocr方式'''

import re, time
from PIL import ImageGrab
from rapidocr_onnxruntime import RapidOCR
from utils import markPrint, strReplace


class OCR:
    def __init__(self):
        self.data_length = 14
        self.replace_dict_name = {
            '【': '[',
            '】': ']',
            '咳木鸟': '啄木鸟'
        }
        self.replace_dict_parts = {
        }
        self.ocr = RapidOCR()
        self.start_time = 0

    def orcImage(self, index, x, y, w, h):
        print(f"图像{index}识别开始...{time.time() - self.start_time}")
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        img_name = f"src/grab{index}.png"
        img.save(img_name)
        result, elapse = self.ocr(img_name, use_det=True, use_cls=False, use_rec=True, text_score=0.35)
        print(f"图像{index}识别完成...{time.time() - self.start_time}")
        return [item[1] for item in result]

    def process_result(self, result):
        # 移除异常文本
        errorText = ["+","S","s"]
        result = [item for item in result if item not in errorText]


        # 存在个位数识别困难情况 进行数据矫正
        # i = 5
        # is_corrected = False
        # s = r'^\d+(\.\d+)?%?$|^%$'
        # while i < len(result):
        #     if i % 2 == 0 and re.match(s, result[i]) is None:
        #         result.insert(i, "0")
        #         is_corrected = True
        #         i += 1  # 跳过插入的元素
        #     i += 1  # 继续下一个元素


        # 校验数据长度
        if len(result) != self.data_length:
            markPrint("数据长度不符合要求", result)
            return False

        # 千位符（含误识别的.）兼容
        pattern_thou = '\d\.\d{3}|\d\,\d{3}'
        txt = [re.sub(pattern_thou, item.replace(',', '').replace('.', ''), item) for item in result]
        temp_name = strReplace(txt[0], self.replace_dict_name)
        name = temp_name.split("[")[0]
        parts = "分区" + temp_name.split("[")[1][0]
        main_name = txt[3]
        main_digit = txt[4]
        lvl = re.findall(r'\d+', txt[1])[0]
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
        for index in range(6, len(txt), 2):
            item = txt[index].split("+")[0] + txt[index + 1]
            try:
                # 词条名称
                name = re.findall(pattern_chinese, item)[0]
                # 数值 兼容千位符被识别为小数点情况
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
                elif name in '异常精通':
                    normalTags['异常精通'] = digit
                elif name in '穿透值':
                    normalTags['穿透值'] = digit
                else:
                    normalTags[item] = 0
            except:
                normalTags[item] = 0
        result["normalTags"] = normalTags

        markPrint(result)
        return result

    def rapidocr(self, x, y, w, h):
        self.start_time = time.time()
        temp_result = [self.orcImage(index, x[index], y[index], w[index], h[index]) for index in range(len(x))]
        result = [item for sublist in temp_result for item in sublist]
        return self.process_result(result)

ocr = OCR()
