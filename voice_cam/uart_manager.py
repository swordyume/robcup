from maix import uart, pinmap, err
from config import (
    PIN_FUNCTION_MAP,
    UART_DEVICE,
    UART_BAUDRATE,
    FRAME_HEAD,
    FRAME_TAIL,
    FRAME_LEN,
    COLOR_MAP,
)


class UARTManager:
    def __init__(self, on_color):
        self._on_color = on_color
        self._init_pins()
        self.uart = uart.UART(UART_DEVICE, UART_BAUDRATE)
        self._rx_buf = bytearray()

    def _init_pins(self):
        for pin, func in PIN_FUNCTION_MAP.items():
            err.check_raise(
                pinmap.set_pin_function(pin, func),
                f"Failed set pin {pin} function to {func}",
            )

    def poll(self):
        data = self.uart.read()
        if data:
            print(data)
            self._rx_buf += data
            self._parse()

    def _parse(self):
        buf = self._rx_buf
        while len(buf) >= FRAME_LEN:
            if buf[0] != FRAME_HEAD:
                head = buf.find(FRAME_HEAD)
                if head < 0:
                    buf.clear()
                    return
                del buf[:head]
                continue
            if buf[1] not in COLOR_MAP or buf[2] != FRAME_TAIL:
                del buf[0]
                continue
            color = buf[1]
            del buf[:FRAME_LEN]
            self._on_color(color)
