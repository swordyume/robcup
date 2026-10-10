import struct
from maix import uart, pinmap, err
from config import (
    PIN_FUNCTION_MAP,
    UART1_DEVICE,
    UART_BAUDRATE,
    FRAME_HEAD,
    CMD_ARRIVE,
    FRAME_TAIL,
    ARRIVE_FLAG_START,
    ARRIVE_FLAG_STOP,
    ARRIVE_FRAME_LEN,
)


class UARTManager:
    def __init__(self):
        self._init_pins()
        self.uart1 = uart.UART(UART1_DEVICE, UART_BAUDRATE)
        # self.uart2 = uart.UART(UART2_DEVICE, UART_BAUDRATE)
        self.detect_enabled = False
        self._rx_buf = bytearray()

    def _init_pins(self):
        for pin, func in PIN_FUNCTION_MAP.items():
            err.check_raise(
                pinmap.set_pin_function(pin, func),
                f"Failed set pin {pin} function to {func}",
            )

    def poll(self):
        data = self.uart1.read()
        if data:
            print(data)
            self._rx_buf += data
            self._parse_arrive()

    def _parse_arrive(self):
        buf = self._rx_buf
        while len(buf) >= ARRIVE_FRAME_LEN:
            if buf[0] != FRAME_HEAD:
                head = buf.find(FRAME_HEAD)
                if head < 0:
                    buf.clear()
                    return
                del buf[:head]
                continue
            if buf[1] != CMD_ARRIVE or buf[3] != FRAME_TAIL:
                del buf[0]
                continue
            flag = buf[2]
            del buf[:ARRIVE_FRAME_LEN]
            if flag == ARRIVE_FLAG_START:
                if not self.detect_enabled:
                    print("arrive flag 0x01 -> enter detect")
                self.detect_enabled = True
            elif flag == ARRIVE_FLAG_STOP:
                if self.detect_enabled:
                    print("arrive flag 0x00 -> exit detect")
                self.detect_enabled = False

    def send_color(self, cmd: int):
        if cmd==7:
            return
        packet = bytes([0x1C, 0x02, cmd, 0x28])
        print(cmd)                          #右边颜色id0x78
        self.uart1.write(packet)

    # def send_direct(self):
    #     packet = bytes([0x1C, 0x12, 0x01, 0x28])
    #     self.uart1.write(packet)

    def send_move(self, distance: float):
        if not self.detect_enabled:
            return
        packet = bytes([0x1C, 0xAD]) + struct.pack("<f", distance) + bytes([0x02, 0x28])              #右边相机id0x02
        self.uart1.write(packet)
