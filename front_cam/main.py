from maix import camera, app
from uart_manager import UARTManager
from color_detector import ColorDetector
from display_manager import DisplayManager


class FrontCamApp:
    def __init__(self):
        self.uart = UARTManager()
        self.detector = ColorDetector(screen_width=320)
        self.display = DisplayManager()
        self.cam = camera.Camera(320, 240)

    def run(self):
        while not app.need_exit():
            self.uart.poll()
            img = self.cam.read()
            if self.uart.detect_enabled:
                self.detector.update(img, self.uart.send_move)
            else:
                self.detector.reset()
            self.display.show(img)


if __name__ == "__main__":
    FrontCamApp().run()