import images
from config import (W, H, PLAYER_SPEED, PLAYER_DRAW_R, PLAYER_HIT_R, PLAYER_HP,
                    INVINCIBLE_TIME, DASH_SPEED, DASH_TIME, DASH_COOLDOWN,
                    GAUGE_PER_GRAZE, GAUGE_MAX, SWORD_MAX, SWORD_RADIUS, SWORD_EFFECT_TIME,
                    COLOR_HITBOX, COLOR_DASH, COLOR_GRAY, COLOR_SWORD)


class Player:
    def __init__(self):
        self.x = W / 2
        self.y = H / 2
        self.hp = PLAYER_HP
        self.invincible = 0   # 남은 무적 시간 (0이면 무적 아님)

        self.face_x = 0       # 마지막으로 움직인 방향 (처음엔 위쪽)
        self.face_y = -1
        self.dash_left = 0    # 남은 대시 시간
        self.dash_cool = 0    # 남은 쿨타임
        self.dash_x = 0
        self.dash_y = 0

        self.gauge = 0         # 검기 게이지 (0 ~ 100)
        self.swords = 0        # 모아둔 검기 개수
        self.graze_flash = 0   # 스쳤을 때 잠깐 표시
        self.sword_effect = 0  # 검기 이펙트 남은 시간

    def update(self, btns):
        if self.invincible > 0:
            self.invincible = self.invincible - 1
        if self.dash_cool > 0:
            self.dash_cool = self.dash_cool - 1
        if self.graze_flash > 0:
            self.graze_flash = self.graze_flash - 1
        if self.sword_effect > 0:
            self.sword_effect = self.sword_effect - 1

        dx = 0
        dy = 0
        if btns.held("L"):
            dx = -1
        if btns.held("R"):
            dx = 1
        if btns.held("U"):
            dy = -1
        if btns.held("D"):
            dy = 1

        if dx != 0 or dy != 0:
            self.face_x = dx
            self.face_y = dy

        # 대시 시작
        if btns.pressed("A") and self.dash_cool == 0 and self.dash_left == 0:
            self.dash_left = DASH_TIME
            self.dash_cool = DASH_COOLDOWN
            self.dash_x = self.face_x
            self.dash_y = self.face_y

        if self.dash_left > 0:
            self.dash_left = self.dash_left - 1
            move_x = self.dash_x
            move_y = self.dash_y
            speed = DASH_SPEED
        else:
            move_x = dx
            move_y = dy
            speed = PLAYER_SPEED

        # 대각선은 그냥 두면 더 빨라져서 0.7배
        if move_x != 0 and move_y != 0:
            speed = speed * 0.7

        self.x = self.x + move_x * speed
        self.y = self.y + move_y * speed

        r = PLAYER_DRAW_R
        if self.x < r:
            self.x = r
        if self.x > W - r:
            self.x = W - r
        if self.y < r:
            self.y = r
        if self.y > H - r:
            self.y = H - r

    def can_be_hit(self):
        # 맞은 뒤 무적이거나 대시 중이면 안 맞음
        if self.invincible > 0 or self.dash_left > 0:
            return False
        return True

    def hit(self):
        self.hp = self.hp - 1
        self.invincible = INVINCIBLE_TIME

    def add_graze(self, count):
        if count == 0:
            return
        self.graze_flash = 4
        self.add_gauge(count * GAUGE_PER_GRAZE)

    def add_gauge(self, amount):
        if self.swords == SWORD_MAX:
            return
        self.gauge = self.gauge + amount
        if self.gauge >= GAUGE_MAX:
            self.gauge = self.gauge - GAUGE_MAX
            self.swords = self.swords + 1
            if self.swords == SWORD_MAX:
                self.gauge = 0

    def use_sword(self):
        if self.swords == 0:
            return False
        self.swords = self.swords - 1
        return True

    def draw(self, img, d):
        # 검기 이펙트: 원이 점점 커짐
        if self.sword_effect > 0:
            done = 1 - self.sword_effect / SWORD_EFFECT_TIME
            rr = 10 + (SWORD_RADIUS - 10) * done
            d.ellipse((self.x - rr, self.y - rr, self.x + rr, self.y + rr), outline=COLOR_SWORD, width=3)
            images.draw(img, images.SLASH, self.x, self.y)

        # 무적일 때 깜빡이기
        if self.invincible > 0 and (self.invincible // 6) % 2 == 1:
            return

        x = self.x
        y = self.y
        # 대시 중이면 뒤에 하늘색 원
        if self.dash_left > 0:
            d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=COLOR_DASH)

        images.draw(img, images.PLAYER, x, y)

        h = PLAYER_HIT_R
        d.ellipse((x - h, y - h, x + h, y + h), fill=COLOR_HITBOX)

        # 스쳤을 때 테두리 반짝
        if self.graze_flash > 0:
            d.ellipse((x - 13, y - 13, x + 13, y + 13), outline=COLOR_SWORD)

    def draw_hp(self, img):
        for i in range(PLAYER_HP):
            x = W - 42 + i * 16
            if i < self.hp:
                images.draw(img, images.HEART, x, 10)
            else:
                images.draw(img, images.HEART_EMPTY, x, 10)

    def draw_dash(self, d):
        # 체력 아래에 대시 쿨타임 막대
        left = W - 50
        right = W - 2
        top = 20
        bottom = 23
        if self.dash_cool == 0:
            d.rectangle((left, top, right, bottom), fill=COLOR_DASH)
        else:
            ready = 1 - self.dash_cool / DASH_COOLDOWN
            d.rectangle((left, top, right, bottom), outline=COLOR_GRAY)
            d.rectangle((left, top, left + (right - left) * ready, bottom), fill=COLOR_GRAY)

    def draw_sword(self, img, d):
        # 대시 막대 아래에 검기 개수와 게이지
        for i in range(SWORD_MAX):
            x = W - 42 + i * 16
            if i < self.swords:
                images.draw(img, images.SWORD, x, 33)
            else:
                images.draw(img, images.SWORD_EMPTY, x, 33)

        left = W - 50
        right = W - 2
        d.rectangle((left, 43, right, 45), outline=COLOR_GRAY)
        if self.gauge > 0:
            d.rectangle((left, 43, left + (right - left) * self.gauge / GAUGE_MAX, 45), fill=COLOR_SWORD)
