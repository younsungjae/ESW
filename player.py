from config import (W, H, PLAYER_SPEED, PLAYER_DRAW_R, PLAYER_HIT_R, PLAYER_HP,
                    INVINCIBLE_TIME, COLOR_PLAYER, COLOR_HITBOX, COLOR_HP)


class Player:
    def __init__(self):
        self.x = W / 2
        self.y = H / 2
        self.hp = PLAYER_HP
        self.invincible = 0   # 남은 무적 시간 (0이면 무적 아님)

    def update(self, btns):
        if self.invincible > 0:
            self.invincible = self.invincible - 1

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

        speed = PLAYER_SPEED
        # 대각선은 그냥 두면 더 빨라져서 0.7배
        if dx != 0 and dy != 0:
            speed = PLAYER_SPEED * 0.7

        self.x = self.x + dx * speed
        self.y = self.y + dy * speed

        r = PLAYER_DRAW_R
        if self.x < r:
            self.x = r
        if self.x > W - r:
            self.x = W - r
        if self.y < r:
            self.y = r
        if self.y > H - r:
            self.y = H - r

    def hit(self):
        self.hp = self.hp - 1
        self.invincible = INVINCIBLE_TIME

    def draw(self, d):
        # 무적일 때 깜빡이기
        if self.invincible > 0 and (self.invincible // 6) % 2 == 1:
            return

        x = self.x
        y = self.y
        r = PLAYER_DRAW_R
        h = PLAYER_HIT_R
        d.ellipse((x - r, y - r, x + r, y + r), fill=COLOR_PLAYER)
        d.ellipse((x - h, y - h, x + h, y + h), fill=COLOR_HITBOX)

    def draw_hp(self, d):
        for i in range(PLAYER_HP):
            x = W - 42 + i * 14
            y = 10
            if i < self.hp:
                d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=COLOR_HP)
            else:
                d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=COLOR_HP)
