from maix import camera, display, image, nn, app,uart, err, pinmap


model = "/root/models/pp_ocr.mud"
ocr = nn.PP_OCR(model)

# =========================
# UART
# =========================
pin_function = {
    "A19": "UART1_TX",
    "A18": "UART1_RX",
}

device = "/dev/ttyS1"

for pin, func in pin_function.items():
    err.check_raise(
        pinmap.set_pin_function(pin, func),
        f"Failed set pin {pin} function to {func}"
    )

serial_dev = uart.UART(device, 115200)
serial_dev.write_str("Hello MaixPy")

# =========================
# Color mapping
# =========================
color_map = {
    "白": "white",
    "红": "red",
    "黄": "yellow",
    "蓝": "blue",
    "绿": "green",
    "橙": "orange"
}

cam = camera.Camera(224, ocr.input_height(), ocr.input_format())
disp = display.Display()

image.load_font("ppocr", "/maixapp/share/font/ppocr_keys_v1.ttf", size = 20)
image.set_default_font("ppocr")

while not app.need_exit():
    img = cam.read()
    objs = ocr.detect(img)
    for obj in objs:
        text = obj.char_str()

        if text in color_map:

            # 发送识别结果
            serial_dev.write_str(color_map[text])

        points = obj.box.to_list()
        img.draw_keypoints(points, image.COLOR_RED, 4, -1, 1)
        img.draw_string(obj.box.x4, obj.box.y4, obj.char_str(), image.COLOR_RED)
    disp.show(img)
