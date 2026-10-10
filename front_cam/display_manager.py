from maix import display, touchscreen, image, app
from maix._maix.err import check_bool_raise


class DisplayManager:
    def __init__(self):
        self.dis = display.Display()
        self.ts = touchscreen.TouchScreen()

        size = image.string_size("< Exit")
        self.exit_btn_pos = [0, 0, 8*2 + size.width(), 12 * 2 + size.height()]

    def draw_exit_button(self, img):
        img.draw_string(8, 12, "< Exit", image.COLOR_WHITE)
        img.draw_rect(
            self.exit_btn_pos[0], self.exit_btn_pos[1],
            self.exit_btn_pos[2], self.exit_btn_pos[3],
            image.COLOR_WHITE, 2,
        )

    def check_exit(self):
        x, y, pressed = self.ts.read()
        if (
            x > self.exit_btn_pos[0]
            and x < self.exit_btn_pos[0] + self.exit_btn_pos[2]
            and y > self.exit_btn_pos[1]
            and y < self.exit_btn_pos[1] + self.exit_btn_pos[3]
        ):
            app.set_exit_flag(True)

    def show(self, img):
        self.draw_exit_button(img)
        self.check_exit()
        self.dis.show(img)