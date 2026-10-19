# =========================
# 模型路径
# =========================
OCR_MODEL_PATH = "/root/models/pp_ocr.mud"

# =========================
# 白纸色块识别（代替货站模型，用于矫正和 OCR 区域）
# =========================
PAPER_THRESHOLDS = [[70, 90, -10, 5, -10, 5]]  # 白色 LAB 阈值
PAPER_AREA_THRESHOLD = 2500
PAPER_PIXELS_THRESHOLD = 2500
PAPER_RATIO_MIN = 0.5
PAPER_RATIO_MAX = 1.15
PAPER_SIZE_DIFF_MAX = 30
PAPER_MARGIN_RATIO = 0.1  # 裁剪掉白纸边缘的比例（和 nn_pp_ocr 一致）

# =========================
# UART 配置
# =========================
PIN_FUNCTION_MAP = {
    "A19": "UART1_TX",
    "A18": "UART1_RX",
    # "A29": "UART2_RX",
    # "A28": "UART2_TX",
}
UART1_DEVICE = "/dev/ttyS1"
# UART2_DEVICE = "/dev/ttyS2"
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
# 颜色映射
# =========================
COLOR_MAP = {
    "白": 0x01,
    "红": 0x02,
    "橙": 0x03,
    "黄": 0x04,
    "绿": 0x05,
    "蓝": 0x06,
    "盗": 0x06,
    "益": 0x06,
    "蓄": 0x06
}

# =========================
# 视觉控制参数
# =========================
ALPHA = 0.3
DEADBAND_U = 6
MAX_JUMP_PIXEL = 30
CONTROL_INTERVAL_S = 0.1
K_Y = 1
LOST_FRAME_THRESHOLD = 3
