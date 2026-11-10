import time
from PIL import Image, ImageDraw, ImageFont
from config import W, H, STEP, FPS, COLOR_BG, COLOR_TEXT, FONT_PATH
from hw import Display, Buttons
from player import Player
from arrows import ArrowManager

screen = Display()
btns = Buttons()
player = Player()
arrows = ArrowManager()

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

try:
    big_font = ImageFont.truetype(FONT_PATH, 24)
    small_font = ImageFont.truetype(FONT_PATH, 13)
except OSError:
    big_font = ImageFont.load_default()
    small_font = ImageFont.load_default()


def center_text(text, y, font):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=COLOR_TEXT)


def any_pressed():
    if btns.pressed("A") or btns.pressed("B") or btns.pressed("C"):
        return True
    return False


state = "title"   # title / play / over
play_steps = 0
over_wait = 0

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

        if state == "title":
            if any_pressed():
                player = Player()
                arrows = ArrowManager()
                play_steps = 0
                state = "play"

        elif state == "play":
            player.update(btns)
            arrows.update(player)
            if player.can_be_hit() and arrows.check_hit(player):
                player.hit()
            play_steps = play_steps + 1
            if player.hp <= 0:
                state = "over"
                over_wait = 60   # 바로 넘어가지 않게 1초 기다림

        elif state == "over":
            if over_wait > 0:
                over_wait = over_wait - 1
            elif any_pressed():
                state = "title"

        next_update = next_update + STEP

    d.rectangle((0, 0, W, H), fill=COLOR_BG)
    survive = str(round(play_steps / 60, 1))

    if state == "title":
        center_text("MURIM GIRL", 80, big_font)
        center_text("PRESS ANY BUTTON", 140, small_font)

    elif state == "play":
        player.draw(d)
        arrows.draw(d)
        player.draw_hp(d)
        player.draw_dash(d)
        d.text((4, 4), "TIME " + survive, font=small_font, fill=COLOR_TEXT)

    elif state == "over":
        center_text("GAME OVER", 80, big_font)
        center_text("TIME " + survive + "s", 120, small_font)
        if over_wait == 0:
            center_text("PRESS ANY BUTTON", 160, small_font)

    frame_count = frame_count + 1
    if now - fps_timer >= 1:
        fps = frame_count
        frame_count = 0
        fps_timer = now
    d.text((4, H - 14), "FPS " + str(fps), fill=COLOR_TEXT)

    screen.show(img)

    # 화면은 1초에 20번만
    spent = time.monotonic() - now
    if spent < 1 / FPS:
        time.sleep(1 / FPS - spent)
