import time
from maix import image
from config import (
    PAPER_THRESHOLDS,
    PAPER_AREA_THRESHOLD,
    PAPER_PIXELS_THRESHOLD,
    PAPER_RATIO_MIN,
    PAPER_RATIO_MAX,
    PAPER_SIZE_DIFF_MAX,
    ALPHA,
    DEADBAND_U,
    MAX_JUMP_PIXEL,
    CONTROL_INTERVAL_S,
    K_Y,
    LOST_FRAME_THRESHOLD,
)


class BoxDetector:
    def __init__(self, screen_weight: int):
        self.U0 = screen_weight / 2
        self.last_u_filtered = self.U0
        self.target_lost = True
        self.target_blob = None
        self.lost_frame_count = 0
        self.last_control_time = 0.0

    def reset(self):
        self.last_u_filtered = self.U0
        self.target_lost = True
        self.target_blob = None
        self.lost_frame_count = 0
        self.last_control_time = 0.0

    def detect(self, img):
        return img.find_blobs(
            PAPER_THRESHOLDS,
            area_threshold=PAPER_AREA_THRESHOLD,
            pixels_threshold=PAPER_PIXELS_THRESHOLD,
        )

    @staticmethod
    def _filter_square_blobs(blobs) -> list:
        squares = []
        for blob in blobs:
            h = blob[3]
            if h == 0:
                continue
            ratio = blob[2] / h
            if (PAPER_RATIO_MIN < ratio < PAPER_RATIO_MAX
                    and abs(blob[2] - h) < PAPER_SIZE_DIFF_MAX):
                squares.append(blob)
        return squares

    def update(self, img, send_move_fn) -> list:
        blobs = self._filter_square_blobs(self.detect(img))
        if blobs:
            self.target_blob = max(blobs, key=lambda b: b[1])
            self._track_target(self.target_blob, send_move_fn)
        else:
            self.target_blob = None
            self._handle_lost()
        self._draw(img, blobs)
        return blobs

    def _track_target(self, blob, send_move_fn):
        u_raw = blob[0] + blob[2] / 2
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
    def _draw(img, blobs):
        for blob in blobs:
            img.draw_rect(blob[0], blob[1], blob[2], blob[3], color=image.COLOR_GREEN)
