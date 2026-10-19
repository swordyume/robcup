from maix import display, image


class DisplayManager:
    def __init__(self):
        self.dis = display.Display()
        image.load_font("ppocr", "/maixapp/share/font/ppocr_keys_v1.ttf", size=20)
        image.set_default_font("ppocr")

    def show(self, img):
        self.dis.show(img)
