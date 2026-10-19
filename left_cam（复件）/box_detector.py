import time
from maix import nn, image
from config import (
    BOX_MODEL_PATH,
    ALPHA,
    DEADBAND_U,
    MAX_JUMP_PIXEL,
    CONTROL_INTERVAL_S,
    K_Y,
    LOST_FRAME_THRESHOLD,
)


class BoxDetector:
    def __init__(self, screen_weight: int):
        self.detector = nn.YOLOv5(model=BOX_MODEL_PATH)
        self.U0 = screen_weight / 2
        self.last_u_filtered = self.U0
        self.target_lost = True
        self.lost_frame_count = 0
        self.last_control_time = 0.0

    @property
    def input_width(self):
        return self.detector.input_width()

    @property
    def input_height(self):
        return self.detector.input_height()

    @property
    def input_format(self):
        return self.detector.input_format()

    def reset(self):
        self.last_u_filtered = self.U0
        self.target_lost = True
        self.lost_frame_count = 0
        self.last_control_time = 0.0

    def detect(self, img):
        return self.detector.detect(img, conf_th=0.5, iou_th=0.45)

    def update(self, img, send_move_fn) -> list:
        objs = self.detect(img)
        if objs:
            self._track_target(objs, send_move_fn)
        else:
            self._handle_lost()
        self._draw(img, objs)
        return objs

    def _track_target(self, objs, send_move_fn):
        obj = max(objs, key=lambda x: x.score)
        u_raw = obj.x + obj.w / 2
        self.lost_frame_count = 0

        if self.target_lost:
            self.last_u_filtered = u_raw
            self.target_lost = False
        else:
            # if abs(u_raw - self.last_u_filtered) <= MAX_JUMP_PIXEL:                          #防跳变，也许可删
            self.last_u_filtered = ALPHA * u_raw + (1 - ALPHA) * self.last_u_filtered

            delta_u = self.last_u_filtered - self.U0                                         
            now = time.perf_counter()
            if abs(delta_u) > DEADBAND_U and (now - self.last_control_time) >= CONTROL_INTERVAL_S:
                move_y = K_Y * delta_u                                                       #左正右负
                print("move:", move_y)
                send_move_fn(move_y)
                self.last_control_time = now
            elif abs(delta_u) < DEADBAND_U:
                send_move_fn(0)

    def _handle_lost(self):
        self.lost_frame_count += 1
        if self.lost_frame_count >= LOST_FRAME_THRESHOLD:
            self.target_lost = True

    @staticmethod
    def _draw(img, objs):
        for obj in objs:
            img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_RED)
            msg = f"{obj.class_id}: {obj.score:.2f}"
            img.draw_string(obj.x, obj.y, msg, color=image.COLOR_RED)
