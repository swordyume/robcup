from maix import nn, image
from config import (
    OCR_MODEL_PATH,
    COLOR_MAP,
    PAPER_THRESHOLDS,
    PAPER_AREA_THRESHOLD,
    PAPER_PIXELS_THRESHOLD,
    PAPER_RATIO_MIN,
    PAPER_RATIO_MAX,
    PAPER_SIZE_DIFF_MAX,
    PAPER_MARGIN_RATIO,
)


class CharacterRecognizer:
    def __init__(self):
        self.ocr = nn.PP_OCR(OCR_MODEL_PATH)

    @property
    def input_width(self):
        return self.ocr.input_width()

    @property
    def input_height(self):
        return self.ocr.input_height()

    @property
    def input_format(self):
        return self.ocr.input_format()

    def detect_paper(self, img):
        blobs = img.find_blobs(
            PAPER_THRESHOLDS,
            area_threshold=PAPER_AREA_THRESHOLD,
            pixels_threshold=PAPER_PIXELS_THRESHOLD,
        )
        for blob in blobs:
            img.draw_rect(blob[0], blob[1], blob[2], blob[3], color=image.COLOR_GREEN)
        
        target = None
        for blob in blobs:
            h = blob[3]
            if h == 0:
                # print("无高度")
                continue
            ratio = blob[2] / h
            
            if (PAPER_RATIO_MIN < ratio < PAPER_RATIO_MAX
                    and abs(blob[2] - h) < PAPER_SIZE_DIFF_MAX):
                if target is None or blob[1] > target[1]:
                    target = blob
                    img.draw_rect(target.x(), target.y(), target.w(), target.h(), color=image.COLOR_GREEN)
        return target

    def recognize(self, img, blob) -> str:
        # margin = int(blob[2] * PAPER_MARGIN_RATIO)
        # roi_x = blob[0] + margin
        # roi_y = blob[1] + margin
        # roi_w = blob[2] - 2 * margin
        # roi_h = blob[3] - 2 * margin
        # img.draw_rect(roi_x, roi_y, roi_w, roi_h, color=image.COLOR_BLUE)
        # roi = img.crop(roi_x, roi_y, roi_w, roi_h)
        roi = img.crop(blob[0], blob[1], blob[2], blob[3])
        if roi.format() != self.input_format:
            roi = roi.to_format(self.input_format)
        roi_big = roi.resize(self.input_width, self.input_height)
        obj = self.ocr.recognize(roi_big)
        if obj is None:
            return ""
        return obj.char_str()

    def get_color_cmd(self, text: str) -> int | None:
        return COLOR_MAP.get(text)

    @staticmethod
    def draw_result(img, blob, text):
        img.draw_string(blob[0], blob[1], text, image.COLOR_RED)
