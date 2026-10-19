from maix import camera, display, image, nn, app, uart, err, pinmap
from maix._maix.image import COLOR_BLUE

# =========================
# OCR
# =========================
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
# Camera
# =========================
ocr_w = ocr.input_width()
ocr_h = ocr.input_height()

cam = camera.Camera(
    224,224,
)

# cam.exposure(50000)
# cam.gain(0)
# cam.exp_mode(camera.AeMode.Auto)

disp = display.Display()

# =========================
# Font
# =========================
image.load_font(
    "ppocr",
    "/maixapp/share/font/ppocr_keys_v1.ttf",
    size=20
)
image.set_default_font("ppocr")

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

#字体白色背景区域

area_threshold = 2500
pixels_threshold = 2500
thresholds = [[60, 90, -10, 10, -35, -5]]  # white


while not app.need_exit():

    # 原始图像
    # print(ocr_h,ocr_w)
    img = cam.read()
    img = img.rotate(270)

    #字体背景做ROI

    blobs = img.find_blobs(thresholds,area_threshold=2500,pixels_threshold=2500)
    #for blob in blobs:
    #     img.draw_rect(blob[0], blob[1], blob[2], blob[3], image.COLOR_GREEN)
    target_blob = None


    for blob in blobs:
        img.draw_rect(blob.x(),blob.y(),blob.w(),blob.h(), image.COLOR_GREEN)

        w = blob[2]
        h = blob[3]

        ratio = w / h


        # 正方形过滤
        if (
            0.85 < ratio < 1.15
            and abs(w-h)<15
        ):
            target_blob = blob
            break

    ocr_img = img.to_format(image.Format.FMT_BGR888)
    if target_blob:
        print(1)
        roi_x = target_blob[0]
        roi_y = target_blob[1]
        roi_w = target_blob[2]
        roi_h = target_blob[3]
        img.draw_rect(roi_x,roi_y,roi_w,roi_h, image.COLOR_GREEN)

    else:

        roi_x=0
        roi_y=0
        roi_w = img.width()
        roi_h = img.height()
        # for blob in blobs:
        #     img.draw_rect(blob[0], blob[1], blob[2], blob[3], image.COLOR_GREEN)
        # # ---------------------------------
        # # 1. 裁剪中央区域
        # # ---------------------------------
        # roi_w = blod[2]
        # roi_h = blod[3]

        # roi_x = blod[0]
        # roi_y = blod[1]
    # else:
    #     roi_x=0
    #     roi_y=0
    #     roi_w=ocr_w
    #     roi_h=ocr_h

    # 去掉边缘
    margin = int(roi_w*0.05)


    roi = ocr_img.crop(
        roi_x+margin,
        roi_y+margin,
        roi_w-2*margin,
        roi_h-2*margin
    )
    img.draw_rect(
        roi_x+margin,
        roi_y+margin,
        roi_w-2*margin,
        roi_h-2*margin,COLOR_BLUE
    )

    # roi = img.crop(
    #     roi_x,
    #     roi_y,
    #     roi_w,
    #     roi_h
    # )

    # ---------------------------------
    # 2. 放大回 OCR 输入尺寸
    # ---------------------------------
    roi_big = roi.resize(
        ocr_w,
        ocr_h
    )

    # ---------------------------------
    # 3. OCR
    # ---------------------------------
    # obj = ocr.detect(roi_big)
    obj = ocr.recognize(roi_big)

    # if len(objs) > 0:

    #     obj = objs[0]
    # obj=obj[0]
    text = obj.char_str()

    if text in color_map:

        # 发送识别结果
        serial_dev.write_str(color_map[text])

        # ---------------------------------
        # 将 ROI 中的坐标映射回原图
        # ---------------------------------
        scale_x = roi_w / ocr_w
        scale_y = roi_h / ocr_h

        points = obj.box.to_list()

        # OCR 框坐标转换回原图
        points_original = []

        for i in range(0, len(points), 2):
            x = int(points[i] * scale_x + roi_x)
            y = int(points[i + 1] * scale_y + roi_y)

            points_original.append(x)
            points_original.append(y)

        # ---------------------------------
        # 在原图上画框
        # ---------------------------------
        img.draw_keypoints(
            points_original,
            image.COLOR_RED,
            4,
            -1,
            1
        )

        # 文字
        img.draw_string(
            roi_x,
            roi_y,
            text,
            image.COLOR_RED
        )

    # 显示
    disp.show(img)