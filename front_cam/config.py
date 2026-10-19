# =========================
# UART 配置
# =========================
PIN_FUNCTION_MAP = {
    "A19": "UART1_TX",
    "A18": "UART1_RX",
}
UART_DEVICE = "/dev/ttyS1"
UART_BAUDRATE = 115200

# =========================
# 到位协议：帧头 0x1C | 命令 0xA0 | arrive flag | 帧尾 0x28
# flag = 0x01 进入 detect 矫正状态，flag = 0x00 退出 detect 矫正状态
# =========================
FRAME_HEAD = 0x1C
CMD_ARRIVE = 0xA0
FRAME_TAIL = 0x28
ARRIVE_FLAG_START = 0x01
ARRIVE_FLAG_STOP = 0x00
ARRIVE_FRAME_LEN = 4

# =========================
# 颜色阈值
# =========================
COLOR_THRESHOLDS = [
    [0, 80, 0, 80, 10, 80],       # 红色
    [0, 60, 0, 127, -128, -35],      # 蓝色
]

# =========================
# 视觉控制参数
# =========================
ALPHA = 0.3
DEADBAND_U = 6
MAX_JUMP_PIXEL = 30
CONTROL_INTERVAL_S = 0.1
K_Y = 0.62
LOST_FRAME_THRESHOLD = 3

# =========================
# 左右边缘像素统计
# =========================
EDGE_BAND_W = 1            # 左右边缘统计带的宽度(像素)，1 表示只统计最左/最右一列