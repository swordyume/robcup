from maix import camera, display, image

cam = camera.Camera(224,224)
disp = display.Display()

# thresholds = [[0, 80, 40, 80, 10, 80]]        # red
thresholds = [[60, 90, -10, 10, -35, 0]]  # white
# thresholds = [[0, 80, 30, 100, -120, -60]]    # blue
while 1:
    img = cam.read()
    img = img.rotate(270)
    blobs = img.find_blobs(thresholds, area_threshold = 2500, pixels_threshold = 2500)
    target_blob = None


    # for blob in blobs:

    #     w = blob[2]
    #     h = blob[3]

    #     ratio = w / h


    #     # 正方形过滤
    #     if (
    #         0.85 < ratio < 1.15
    #         and abs(w-h)<15
    #     ):
    #         target_blob = blob
    #         break


    # if target_blob:

    #     roi_x = target_blob[0]
    #     roi_y = target_blob[1]
    #     roi_w = target_blob[2]
    #     roi_h = target_blob[3]
    #     img.draw_rect(roi_x,roi_y,roi_w,roi_h, image.COLOR_GREEN)

    for b in blobs:
        img.draw_rect(b.x(),b.y(),b.w(),b.h(), image.COLOR_GREEN)

    disp.show(img)
