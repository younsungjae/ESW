from config import W, H, PLAYER_SPEED, PLAYER_DRAW_R, PLAYER_HIT_R, COLOR_PLAYER, COLOR_HITBOX


class Player:
    def __init__(self):
        self.x = W / 2
        self.y = H / 2

    def update(self, btns):
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

    def draw(self, d):
        x = self.x
        y = self.y
        r = PLAYER_DRAW_R
        h = PLAYER_HIT_R
        d.ellipse((x - r, y - r, x + r, y + r), fill=COLOR_PLAYER)
        d.ellipse((x - h, y - h, x + h, y + h), fill=COLOR_HITBOX)
