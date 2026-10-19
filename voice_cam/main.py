from maix import app, time
from uart_manager import UARTManager
from voice_player import VoicePlayer


class VoiceCamApp:
    def __init__(self):
        self.voice = VoicePlayer()
        self.uart = UARTManager(on_color=self.voice.notify_color)

    def run(self):
        while not app.need_exit():
            self.uart.poll()
            self.voice.tick()
            time.sleep_ms(1)


if __name__ == "__main__":
    VoiceCamApp().run()
