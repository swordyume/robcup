import time
from maix import image
from config import (
    COLOR_THRESHOLDS,
    DEADBAND_U,
    CONTROL_INTERVAL_S,
    K_Y,
    LOST_FRAME_THRESHOLD,
    EDGE_BAND_W,
)


class ColorDetector:
    def __init__(self, screen_width: int):
        self.U0 = screen_width / 2
        self.last_left = 0
        self.last_right = 0
        self.target_lost = True
        self.lost_frame_count = 0
        self.last_control_time = 0.0

    def reset(self):
        self.last_left = 0
        self.last_right = 0
        self.target_lost = True
        self.lost_frame_count = 0
        self.last_control_time = 0.0

    def detect(self, img):
        return img.find_blobs(
            COLOR_THRESHOLDS,
            area_threshold=1000,
            pixels_threshold=1000,
        )

    def update(self, img, send_move_fn) -> list:
        blobs = self.detect(img)
        if blobs:
            self._track_target(img, send_move_fn)
        else:
            self._handle_lost()

        self._draw(img, blobs)
        return blobs

    def _track_target(self, img, send_move_fn):
        self.lost_frame_count = 0
        left_count, right_count = self._edge_counts(img)
        self.last_left = left_count
        self.last_right = right_count
        delta_u = right_count - left_count

        if self.target_lost:
            self.target_lost = False
            return

        now = time.perf_counter()
        if abs(delta_u) > DEADBAND_U and (now - self.last_control_time) >= CONTROL_INTERVAL_S:
            move_y = -K_Y * delta_u
            print("left:", left_count, "right:", right_count, "delta:", delta_u, "move:", move_y)
            send_move_fn(move_y)
            self.last_control_time = now
        elif abs(delta_u) < DEADBAND_U:
            send_move_fn(0)

    @staticmethod
    def _edge_counts(img) -> tuple:
        band = EDGE_BAND_W
        h = img.height()
        counts = []
        for x in (0, img.width() - band):
            strip = img.find_blobs(
                COLOR_THRESHOLDS,
                roi=[x, 0, band, h],
                x_stride=1,
                y_stride=1,
                area_threshold=1,
                pixels_threshold=1,
                merge=True,
            )
            counts.append(sum(b.pixels() for b in strip))
        return counts[0], counts[1]

    def _handle_lost(self):
        self.lost_frame_count += 1
        if self.lost_frame_count >= LOST_FRAME_THRESHOLD:
            self.target_lost = True

    @staticmethod
    def _draw(img, blobs):
        for blob in blobs:
            img.draw_rect(
                blob.x(),
                blob.y(),
                blob.w(),
                blob.h(),
                image.COLOR_GREEN,
            )
