from maix import nn, image
from config import OCR_MODEL_PATH, COLOR_MAP


class CharacterRecognizer:
    def __init__(self):
        self.ocr = nn.PP_OCR(OCR_MODEL_PATH)

    def detect(self, img):
        ocr_img = img.to_format(image.Format.FMT_BGR888)
        return self.ocr.detect(ocr_img)

    def get_color_cmd(self, text: str) -> int | None:
        return COLOR_MAP.get(text)

    @staticmethod
    def draw_results(img, results):
        for obj in results:
            points = obj.box.to_list()
            img.draw_keypoints(points, image.COLOR_RED, 4, -1, 1)
            img.draw_string(obj.box.x4, obj.box.y4, obj.char_str(), image.COLOR_RED)
