import time
from PIL import Image, ImageDraw, ImageFont
from config import W, H, STEP, FPS, SWORD_RADIUS, SWORD_EFFECT_TIME, CUTIN_TIME, BOSS_GAUGE, COLOR_BG, COLOR_TEXT, FONT_PATH
from hw import Display, Buttons
from player import Player
from arrows import ArrowManager
from stage import Stage
from boss import Boss
from ending import Ending
import record
import images

screen = Display()
btns = Buttons()
player = Player()
arrows = ArrowManager()
stage = Stage()
boss = None

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

try:
    big_font = ImageFont.truetype(FONT_PATH, 24)
    small_font = ImageFont.truetype(FONT_PATH, 12)
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


state = "title"   # title / play / pause / ending / over / clear
play_steps = 0
over_wait = 0
ending = None
rec = record.load()
new_record = False
cutin = 0

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
                stage = Stage()
                boss = None
                play_steps = 0
                cutin = 0
                state = "play"

        elif state == "play":
            stage.update()
            player.update(btns)
            arrows.update(player, stage)

            # 밤이 되면 보스 등장
            if stage.phase == "night" and boss is None:
                boss = Boss(stage.day)
            if boss is not None:
                boss.update(arrows)
                if play_steps % 30 == 0:
                    player.add_gauge(BOSS_GAUGE)

            if player.can_be_hit():
                if arrows.check_hit(player):
                    player.hit()
                else:
                    player.add_graze(arrows.check_graze(player))
            if btns.pressed("B") and player.use_sword():
                arrows.clear_near(player.x, player.y, SWORD_RADIUS)
                if boss is not None and boss.in_range(player):
                    boss.hit()
                cutin = CUTIN_TIME

            # 보스를 잡으면 화살 다 없애고 다음 날로
            if boss is not None and boss.is_dead():
                boss = None
                arrows.clear_all()
                stage.boss_defeated()
            play_steps = play_steps + 1
            if player.hp <= 0:
                state = "over"
                over_wait = 60   # 바로 넘어가지 않게 1초 기다림
                new_record = False
                if play_steps / 60 > rec["best_time"]:
                    rec["best_time"] = round(play_steps / 60, 1)
                    record.save(rec)
                    new_record = True
            elif cutin > 0:
                state = "cutin"
            elif stage.finished:
                state = "ending"
                ending = Ending()
            elif btns.pressed("C"):
                state = "pause"

        elif state == "pause":
            if btns.pressed("C"):
                state = "play"

        elif state == "cutin":
            cutin = cutin - 1
            if cutin == 0:
                player.sword_effect = SWORD_EFFECT_TIME
                state = "play"

        elif state == "ending":
            ending.update(btns)
            if ending.done:
                state = "clear"
                over_wait = 60
                new_record = False
                if rec["clear_time"] == 0 or play_steps / 60 < rec["clear_time"]:
                    rec["clear_time"] = round(play_steps / 60, 1)
                    record.save(rec)
                    new_record = True

        elif state == "over" or state == "clear":
            if over_wait > 0:
                over_wait = over_wait - 1
            elif any_pressed():
                state = "title"

        next_update = next_update + STEP

    survive = str(round(play_steps / 60, 1))

    if state == "title":
        d.rectangle((0, 0, W, H), fill=COLOR_BG)
        center_text("무림소녀", 80, big_font)
        center_text("아무 버튼이나 누르세요", 140, small_font)

    elif state == "play" or state == "pause" or state == "cutin":
        d.rectangle((0, 0, W, H), fill=stage.bg_color())
        if boss is not None:
            boss.draw(img)
        player.draw(img, d)
        arrows.draw(d)
        if boss is not None:
            boss.draw_hp(d, small_font)
        player.draw_hp(img)
        player.draw_dash(d)
        player.draw_sword(img, d)
        d.text((4, 4), stage.name(), font=small_font, fill=COLOR_TEXT)
        d.text((4, 20), "시간 " + survive, font=small_font, fill=COLOR_TEXT)
        if stage.banner > 0:
            center_text(stage.banner_text(), 90, big_font)
        if state == "pause":
            d.rectangle((50, 95, 190, 150), fill=(0, 0, 0), outline=COLOR_TEXT)
            center_text("일시정지", 100, big_font)
            center_text("가운데 버튼으로 계속", 130, small_font)
        if state == "cutin":
            passed = CUTIN_TIME - cutin
            x = 0
            if passed < 12:
                x = W - passed * 20
            img.paste(images.CUTIN, (x, 80))
            d.line((x, 79, W, 79), fill=COLOR_TEXT, width=2)
            d.line((x, 160, W, 160), fill=COLOR_TEXT, width=2)

    elif state == "ending":
        ending.draw(img, d, small_font)

    elif state == "over":
        d.rectangle((0, 0, W, H), fill=stage.bg_color())
        center_text("게임 오버", 60, big_font)
        center_text(stage.name(), 100, small_font)
        center_text("버틴 시간 " + survive + "초", 120, small_font)
        center_text("최고 기록 " + str(rec["best_time"]) + "초", 140, small_font)
        if new_record:
            center_text("NEW RECORD!", 160, small_font)
        if over_wait == 0:
            center_text("아무 버튼이나 누르세요", 190, small_font)

    elif state == "clear":
        d.rectangle((0, 0, W, H), fill=COLOR_BG)
        center_text("클리어!", 60, big_font)
        center_text("남은 체력 " + str(player.hp), 100, small_font)
        center_text("클리어 시간 " + survive + "초", 120, small_font)
        center_text("최단 기록 " + str(rec["clear_time"]) + "초", 140, small_font)
        if new_record:
            center_text("NEW RECORD!", 160, small_font)
        if over_wait == 0:
            center_text("아무 버튼이나 누르세요", 190, small_font)

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
