import time
from PIL import Image, ImageDraw
from config import W, H, STEP, FPS, COLOR_BG, COLOR_TEXT
from hw import Display, Buttons
from player import Player


def main():
    screen = Display()
    btns = Buttons()
    player = Player()

    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    prev = time.monotonic()
    acc = 0.0
    fps = 0.0
    frames = 0
    fps_t = prev

    while True:
        now = time.monotonic()
        acc += now - prev
        prev = now
        if acc > 0.25:
            acc = 0.0

        # 로직은 60Hz 고정
        while acc >= STEP:
            btns.update()
            player.update(btns)
            acc -= STEP

        d.rectangle((0, 0, W, H), fill=COLOR_BG)
        player.draw(d)

        frames += 1
        if now - fps_t >= 1.0:
            fps = frames / (now - fps_t)
            frames = 0
            fps_t = now
        d.text((4, 4), f"FPS {fps:4.1f}", fill=COLOR_TEXT)
        screen.show(img)

        spent = time.monotonic() - now
        time.sleep(max(0, 1 / FPS - spent))


if __name__ == "__main__":
    main()
