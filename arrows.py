import math
import random
from config import (W, H, ARROW_SPEED, ARROW_LEN, ARROW_HIT_R, ARROW_START_GAP, ARROW_MIN_GAP,
                    MAX_ARROWS, PLAYER_HIT_R, COLOR_ARROW)


class Arrow:
    def __init__(self, x, y, target_x, target_y, speed):
        self.x = x
        self.y = y
        angle = math.atan2(target_y - y, target_x - x)
        self.dir_x = math.cos(angle)
        self.dir_y = math.sin(angle)
        self.speed = speed

    def update(self):
        self.x = self.x + self.dir_x * self.speed
        self.y = self.y + self.dir_y * self.speed

    def is_out(self):
        if self.x < -10 or self.x > W + 10:
            return True
        if self.y < -10 or self.y > H + 10:
            return True
        return False

    def draw(self, d):
        # 날아가는 반대 방향으로 꼬리
        tail_x = self.x - self.dir_x * ARROW_LEN
        tail_y = self.y - self.dir_y * ARROW_LEN
        d.line((tail_x, tail_y, self.x, self.y), fill=COLOR_ARROW, width=2)


def random_edge():
    side = random.randint(0, 3)
    if side == 0:
        return random.randint(0, W), -5
    if side == 1:
        return random.randint(0, W), H + 5
    if side == 2:
        return -5, random.randint(0, H)
    return W + 5, random.randint(0, H)


class ArrowManager:
    def __init__(self):
        self.arrows = []
        self.timer = 0
        self.time = 0

    def spawn(self, player):
        x, y = random_edge()
        # 플레이어 근처를 노리게 (정확히 노리면 너무 어려움)
        target_x = player.x + random.randint(-30, 30)
        target_y = player.y + random.randint(-30, 30)
        speed = ARROW_SPEED + (self.time // 600) * 0.1   # 10초마다 조금씩 빨라짐
        self.arrows.append(Arrow(x, y, target_x, target_y, speed))

    def update(self, player):
        self.time = self.time + 1
        self.timer = self.timer + 1

        gap = ARROW_START_GAP - (self.time // 300) * 2   # 5초마다 간격이 줄어듦
        if gap < ARROW_MIN_GAP:
            gap = ARROW_MIN_GAP

        if self.timer >= gap and len(self.arrows) < MAX_ARROWS:
            self.timer = 0
            self.spawn(player)

        for a in self.arrows:
            a.update()

        alive = []
        for a in self.arrows:
            if not a.is_out():
                alive.append(a)
        self.arrows = alive

    def check_hit(self, player):
        for a in self.arrows:
            dx = a.x - player.x
            dy = a.y - player.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < PLAYER_HIT_R + ARROW_HIT_R:
                self.arrows.remove(a)
                return True
        return False

    def draw(self, d):
        for a in self.arrows:
            a.draw(d)
