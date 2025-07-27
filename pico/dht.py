import time
from machine import Pin

class DHTBase:
    def __init__(self, pin):
        self.pin = pin
        self.buf = bytearray(5)

    def measure(self):
        buf = self.buf
        buf[:] = b'\x00\x00\x00\x00\x00'    # <‑‑ clear previous bits

        self._send_init_signal()
        self._collect_input()
        for i in range(40):
            while self.pin.value() == 0:
                pass
            t = time.ticks_us()
            while self.pin.value() == 1:
                pass
            if time.ticks_diff(time.ticks_us(), t) > 50:
                buf[i // 8] |= 1 << (7 - i % 8)

    # checksum
        if buf[4] != ((buf[0] + buf[1] + buf[2] + buf[3]) & 0xFF):
            raise Exception("checksum error")


    def _send_init_signal(self):
        self.pin.init(Pin.OUT)
        self.pin.value(0)
        time.sleep_ms(20)
        self.pin.value(1)
        time.sleep_us(40)
        self.pin.init(Pin.IN)

    def _collect_input(self):
        for i in range(2):
            count = 0
            while self.pin.value() == i:
                count += 1
                if count > 100:
                    raise Exception("DHT timeout")

class DHT11(DHTBase):
    def temperature(self):
        return self.buf[2]

    def humidity(self):
        return self.buf[0]