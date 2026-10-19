from maix import audio, err
from config import (
    VOICE_DIR,
    COLOR_MAP,
    SAMPLE_RATE,
    VOLUME,
    KICKSTART_SILENCE_BYTES,
)


class VoicePlayer:
    def __init__(self):
        self._data = {}
        for color, (name, filename) in COLOR_MAP.items():
            path = f"{VOICE_DIR}/{filename}"
            f = audio.File()
            err.check_raise(f.load(path), f"Failed to load {path}")
            self._data[color] = bytes(f.get_pcm())
            print(f"[voice] loaded {name}: {path} sample_rate={f.sample_rate()} channel={f.channels()}")
        self._player = audio.Player(sample_rate=SAMPLE_RATE, channel=1, block=False)
        self._player.volume(VOLUME)
        self._player.play(bytes(KICKSTART_SILENCE_BYTES))
        self._pcm = None
        self._offset = 0
        self._last_cmd = None

    def notify_color(self, color: int):
        if color == self._last_cmd:
            return
        self._last_cmd = color
        print(f"[voice] play {COLOR_MAP[color][0]} (0x{color:02x})")
        self._pcm = self._data[color]
        self._offset = 0

    def tick(self):
        if self._pcm is None or self._offset >= len(self._pcm):
            return
        idle_frames = self._player.get_remaining_frames()
        if idle_frames <= 0:
            return
        feed_frames = min(idle_frames, self._player.period_size())
        if feed_frames <= 0:
            return
        feed_bytes = self._player.frame_size(feed_frames)
        chunk = self._pcm[self._offset:self._offset + feed_bytes]
        self._player.play(chunk)
        self._offset += len(chunk)
