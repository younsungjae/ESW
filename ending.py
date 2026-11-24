import images
from config import W, COLOR_TEXT

PAGES = [
    (images.ENDING1, "천마가 쓰러지자", "봉인의 진법이 다시 빛났다."),
    (images.ENDING2, "사흘 밤낮의 싸움 끝에", "죽림에 아침이 밝아온다."),
    (images.ENDING2, "죽림문의 마지막 후예,", "무림소녀의 이야기는 계속된다."),
]


class Ending:
    def __init__(self):
        self.page = 0
        self.wait = 60
        self.done = False

    def update(self, btns):
        if self.wait > 0:
            self.wait = self.wait - 1
            return
        if btns.pressed("A") or btns.pressed("B") or btns.pressed("C"):
            self.page = self.page + 1
            self.wait = 60
            if self.page >= len(PAGES):
                self.done = True

    def draw(self, img, d, font):
        picture, line1, line2 = PAGES[self.page]
        img.paste(picture, (0, 0))
        d.rectangle((0, 160, W, 240), fill=(0, 0, 0))
        d.text((10, 172), line1, font=font, fill=COLOR_TEXT)
        d.text((10, 192), line2, font=font, fill=COLOR_TEXT)
        if self.wait == 0:
            d.text((W - 20, 220), "▶", font=font, fill=COLOR_TEXT)
