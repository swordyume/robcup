# =========================
# UART 配置（MaixCAM UART1: A19=TX, A18=RX）
# =========================
PIN_FUNCTION_MAP = {
    "A19": "UART1_TX",
    "A18": "UART1_RX",
}
UART_DEVICE = "/dev/ttyS1"
UART_BAUDRATE = 115200

# =========================
# 颜色播报协议：帧头 0x0A | 颜色 | 帧尾 0x0B，共 3 字节
# =========================
FRAME_HEAD = 0x0A
FRAME_TAIL = 0x0B
FRAME_LEN = 3

# =========================
# 颜色字节 -> (语音名称, 语音文件)
# 橙色对应的语音是 no_mail
# =========================
VOICE_DIR = "/root"
COLOR_MAP = {
    0x01: ("white", "white.wav"),
    0x02: ("red", "red.wav"),
    0x03: ("no_mail", "no_mail.wav"),      # 橙色
    0x04: ("yellow", "yellow.wav"),
    0x05: ("green", "green.wav"),
    0x06: ("blue", "blue.wav"),
}

# =========================
# 播放参数
# =========================
SAMPLE_RATE = 48000
VOLUME = 80
# 播放器创建后先写入一段静音启动播放管线，避免非阻塞 play 一直无空闲帧
KICKSTART_SILENCE_BYTES = 4096
