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

        spi = board.SPI()
        self.disp = st7789.ST7789(spi, width=W, height=H, rotation=180, y_offset=80,
                                  cs=cs, dc=dc, rst=rst, baudrate=24000000)

    def show(self, img):
        self.disp.image(img)


def make_button(pin):
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    return btn


class Buttons:
    def __init__(self):
        self.pins = {
            "U": make_button(board.D17),
            "D": make_button(board.D22),
            "L": make_button(board.D27),
            "R": make_button(board.D23),
            "C": make_button(board.D4),
            "A": make_button(board.D5),
            "B": make_button(board.D6),
        }
        self.now = {}
        self.before = {}
        for name in self.pins:
            self.now[name] = False
            self.before[name] = False

    def update(self):
        for name in self.pins:
            self.before[name] = self.now[name]
            # 누르면 LOW(False)가 되니까 반대로 저장
            self.now[name] = not self.pins[name].value

    def held(self, name):
        return self.now[name]

    def pressed(self, name):
        if self.now[name] and not self.before[name]:
            return True
        return False
