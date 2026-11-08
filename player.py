from config import W, H, PLAYER_SPEED, PLAYER_DRAW_R, PLAYER_HIT_R, COLOR_PLAYER, COLOR_HITBOX

DIAG = 0.7071  # 1/sqrt(2)


class Player:
    def __init__(self):
        self.x = W / 2
        self.y = H / 2

    def update(self, btns):
        dx = btns.held("R") - btns.held("L")
        dy = btns.held("D") - btns.held("U")
        if dx != 0 and dy != 0:
            dx *= DIAG
            dy *= DIAG
        self.x += dx * PLAYER_SPEED
        self.y += dy * PLAYER_SPEED

        r = PLAYER_DRAW_R
        self.x = max(r, min(W - r, self.x))
        self.y = max(r, min(H - r, self.y))

    def draw(self, d):
        r = PLAYER_DRAW_R
        d.ellipse((self.x - r, self.y - r, self.x + r, self.y + r), fill=COLOR_PLAYER)
        h = PLAYER_HIT_R
        d.ellipse((self.x - h, self.y - h, self.x + h, self.y + h), fill=COLOR_HITBOX)
