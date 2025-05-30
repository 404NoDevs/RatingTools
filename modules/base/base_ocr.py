'''图像识别、文字处理，考虑多种ocr方式'''

import re
import time
from PIL import ImageGrab
from rapidocr_onnxruntime import RapidOCR


class BaseOCR:
    def __init__(self, params):
        # 获取子类参数
        sub_error_text = params.get("error_text", [])

        self.ocr = RapidOCR()
        self.start_time = 0
        self.error_text = ["", "+", "×", "X"] + sub_error_text

    def orcImage(self, index, x, y, w, h):
        print(f"图像{index}识别开始...{time.time() - self.start_time}")
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        img_name = f"src/grab{index}.png"
        img.save(img_name)
        result, elapse = self.ocr(img_name, use_det=True, use_cls=False, use_rec=True, text_score=0.35)
        print(f"图像{index}识别完成...{time.time() - self.start_time}")
        if not result:
            return []
        return [item[1] for item in result]

    def rapidocr(self, x, y, w, h):
        self.start_time = time.time()
        temp_result = [self.orcImage(index, x[index], y[index], w[index], h[index]) for index in range(len(x))]
        result = [item for sublist in temp_result for item in sublist]
        return self.process_result(result)

    # 子类方法
    def process_result(self, result):
        # 移除异常文本
        result = [item for item in result if item not in self.error_text]
        # 千位符（含误识别的.）兼容
        result = [re.sub(r'(?<=\d)[.,](\d{3})', r'\1', item) for item in result]
        # 将所有：替换为 .
        result = [item.replace("：", ".").replace(":", ".") for item in result]
        # 去空格
        result = [item.replace(" ", "") for item in result]

        # 识别多个小数点兼容
        def simple_replace(match):
            parts = match.group(0).split('.')
            first_part = ''.join(parts[:-1])
            last_part = parts[-1]
            return first_part + ('.' + last_part if last_part else '')
        result = [re.sub(r'(\d+\.)*\d+\.\d+', simple_replace, item) for item in result]
        return result
