import time
from PIL import Image, ImageDraw
from config import W, H, STEP, FPS, COLOR_BG, COLOR_TEXT
from hw import Display, Buttons
from player import Player

screen = Display()
btns = Buttons()
player = Player()

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

next_update = time.monotonic()
fps = 0
frame_count = 0
fps_timer = time.monotonic()

while True:
    now = time.monotonic()

    # 너무 많이 밀렸으면 따라잡지 않고 지금부터 다시
    if now - next_update > 0.25:
        next_update = now

    # 게임 계산은 1/60초마다 한 번
    while next_update <= now:
        btns.update()
        player.update(btns)
        next_update = next_update + STEP

    d.rectangle((0, 0, W, H), fill=COLOR_BG)
    player.draw(d)

    frame_count = frame_count + 1
    if now - fps_timer >= 1:
        fps = frame_count
        frame_count = 0
        fps_timer = now
    d.text((4, 4), "FPS " + str(fps), fill=COLOR_TEXT)

    screen.show(img)

    # 화면은 1초에 20번만
    spent = time.monotonic() - now
    if spent < 1 / FPS:
        time.sleep(1 / FPS - spent)
