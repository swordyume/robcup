from maix import camera, app
from uart_manager import UARTManager
from character_recognizer import CharacterRecognizer
from box_detector import BoxDetector
from display_manager import DisplayManager


class RightCamApp:
    def __init__(self):
        self.uart = UARTManager()
        self.recognizer = CharacterRecognizer()
        self.detector = BoxDetector(screen_weight=224)
        self.display = DisplayManager()
        self.cam = camera.Camera(224, 224)

    def run(self):
        while not app.need_exit():
            self.uart.poll()
            img_raw = self.cam.read()
            img = img_raw.rotate(270)
            if self.uart.detect_enabled:
                self.detector.update(img, self.uart.send_move)
            else:
                self.detector.reset()
            self._process_ocr(img)
            self.display.show(img)

    def _process_ocr(self, img):
        blob = self.recognizer.detect_paper(img)
        cmd = None
        if blob is not None:
            text = self.recognizer.recognize(img, blob)
            if text:
                print(text)
                cmd = self.recognizer.get_color_cmd(text)
                CharacterRecognizer.draw_result(img, blob, text)
        self._update_color_cmd(cmd)

    def _update_color_cmd(self, cmd):
        # 识别到有效汉字：直接采用该颜色
        if cmd is not None:
            self.uart.send_color(cmd)


if __name__ == "__main__":
    RightCamApp().run()
