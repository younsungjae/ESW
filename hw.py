import board
import digitalio
from adafruit_rgb_display import st7789
from config import W, H


class Display:
    def __init__(self):
        cs = digitalio.DigitalInOut(board.CE0)
        dc = digitalio.DigitalInOut(board.D25)
        rst = digitalio.DigitalInOut(board.D24)

        self.backlight = digitalio.DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True

        self.disp = st7789.ST7789(
            board.SPI(), width=W, height=H,
            rotation=180, y_offset=80,
            cs=cs, dc=dc, rst=rst,
            baudrate=24000000,
        )

    def show(self, img):
        self.disp.image(img)


class Buttons:
    PINS = {
        "U": board.D17, "D": board.D22,
        "L": board.D27, "R": board.D23,
        "C": board.D4,
        "A": board.D5, "B": board.D6,
    }

    def __init__(self):
        self.pins = {}
        for name, pin in self.PINS.items():
            p = digitalio.DigitalInOut(pin)
            p.direction = digitalio.Direction.INPUT
            p.pull = digitalio.Pull.UP
            self.pins[name] = p
        self.now = {n: False for n in self.PINS}
        self.prev = {n: False for n in self.PINS}

    def update(self):
        self.prev = self.now
        self.now = {n: not p.value for n, p in self.pins.items()}  # active low

    def held(self, name):
        return self.now[name]

    def pressed(self, name):
        return self.now[name] and not self.prev[name]
