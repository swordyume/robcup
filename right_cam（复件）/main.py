import time
from maix import camera, app
from config import COLOR_MAP, WHITE_FALLBACK_DELAY_S
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
        self.cam = camera.Camera(
            self.detector.input_width,
            self.detector.input_height,
            self.detector.input_format,
        )
        self._timer_since = None
        self._box_prev = False
        self._decided_cmd = None
        self._is_timing=False

    def run(self):
        while not app.need_exit():
            self.uart.poll()
            img_raw = self.cam.read()
            img = img_raw.rotate(270)
            if self.uart.detect_enabled:
                self.detector.update(img, self.uart.send_move)
                box_present = not self.detector.target_lost
            else:
                self.detector.reset()
                box_present = False
            self._process_ocr(img, box_present)
            self.display.show(img)

    def _process_ocr(self, img, box_present):
        results = self.recognizer.detect(img)
        cmd = None
        for obj in results:
            cmd = self.recognizer.get_color_cmd(obj.char_str()) 
            print(obj.char_str())
            if cmd is not None:
                break
        self._update_color_cmd(cmd, box_present)
        CharacterRecognizer.draw_results(img, results)

    def _update_color_cmd(self, cmd, box_present):
        now = time.perf_counter()
        rising = box_present and not self._box_prev
        self._box_prev = box_present

        # 看到货站（上升沿）：上一轮已判定完则开始新一轮并重新计时
        if rising and self._decided_cmd is not None:
            self._decided_cmd = None
            self._timer_since = now
            self._is_timing=True
        elif box_present and self._timer_since is None:
            self._timer_since = now
            self._is_timing=True

        # 识别到有效汉字：本轮计时终止，采用该颜色；“白”兜底可被覆盖
        # if cmd is not None and self._decided_cmd in (None, COLOR_MAP["白"]):
        if cmd is not None:
            self._decided_cmd = cmd
            self.uart.send_color(self._decided_cmd)
            self._is_timing=False

        # 计时满阈值仍无有效汉字：按“白”处理；计时不会因货站消失/detect 变 false 而终止
        # if (self._decided_cmd is None and self._timer_since is not None
        #         and now - self._timer_since >= WHITE_FALLBACK_DELAY_S):
        if (self._decided_cmd is None and self._is_timing==True and self._timer_since is not None
                and now - self._timer_since >= WHITE_FALLBACK_DELAY_S):
            self._decided_cmd = COLOR_MAP["白"]
            self.uart.send_color(self._decided_cmd)
            print("白")
            self._is_timing=False
            

        # if self._decided_cmd is not None:
        #     self.uart.send_color(self._decided_cmd)
        #     self._decided_cmd = 7


if __name__ == "__main__":
    RightCamApp().run()
