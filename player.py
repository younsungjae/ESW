from config import (W, H, PLAYER_SPEED, PLAYER_DRAW_R, PLAYER_HIT_R, PLAYER_HP,
                    INVINCIBLE_TIME, DASH_SPEED, DASH_TIME, DASH_COOLDOWN,
                    COLOR_PLAYER, COLOR_HITBOX, COLOR_HP, COLOR_DASH, COLOR_GRAY)


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

    def update(self, btns):
        if self.invincible > 0:
            self.invincible = self.invincible - 1
        if self.dash_cool > 0:
            self.dash_cool = self.dash_cool - 1

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

    def draw(self, d):
        # 무적일 때 깜빡이기
        if self.invincible > 0 and (self.invincible // 6) % 2 == 1:
            return

        color = COLOR_PLAYER
        if self.dash_left > 0:
            color = COLOR_DASH

        x = self.x
        y = self.y
        r = PLAYER_DRAW_R
        h = PLAYER_HIT_R
        d.ellipse((x - r, y - r, x + r, y + r), fill=color)
        d.ellipse((x - h, y - h, x + h, y + h), fill=COLOR_HITBOX)

    def draw_hp(self, d):
        for i in range(PLAYER_HP):
            x = W - 42 + i * 14
            y = 10
            if i < self.hp:
                d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=COLOR_HP)
            else:
                d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=COLOR_HP)

    def draw_dash(self, d):
        # 체력 아래에 대시 쿨타임 막대
        left = W - 47
        right = W - 9
        top = 20
        bottom = 23
        if self.dash_cool == 0:
            d.rectangle((left, top, right, bottom), fill=COLOR_DASH)
        else:
            ready = 1 - self.dash_cool / DASH_COOLDOWN
            d.rectangle((left, top, right, bottom), outline=COLOR_GRAY)
            d.rectangle((left, top, left + (right - left) * ready, bottom), fill=COLOR_GRAY)
