import math
import random
from config import (W, H, ARROW_LEN, ARROW_HIT_R, MAX_ARROWS, PLAYER_HIT_R, GRAZE_DIST, COLOR_ARROW)


class Arrow:
    def __init__(self, x, y, target_x, target_y, speed):
        self.x = x
        self.y = y
        angle = math.atan2(target_y - y, target_x - x)
        self.dir_x = math.cos(angle)
        self.dir_y = math.sin(angle)
        self.speed = speed
        self.grazed = False   # 이미 스친 화살은 다시 안 셈

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

    def spawn(self, player, speed):
        x, y = random_edge()
        # 플레이어 근처를 노리게 (정확히 노리면 너무 어려움)
        target_x = player.x + random.randint(-30, 30)
        target_y = player.y + random.randint(-30, 30)
        self.arrows.append(Arrow(x, y, target_x, target_y, speed))

    def update(self, player, gap, speed):
        # gap: 몇 번 계산마다 한 발 쏠지, speed: 화살 속도 (시간대마다 다름)
        self.timer = self.timer + 1
        if self.timer >= gap and len(self.arrows) < MAX_ARROWS:
            self.timer = 0
            self.spawn(player, speed)

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

    def check_graze(self, player):
        count = 0
        for a in self.arrows:
            if not a.grazed:
                dx = a.x - player.x
                dy = a.y - player.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < GRAZE_DIST:
                    a.grazed = True
                    count = count + 1
        return count

    def clear_near(self, x, y, radius):
        alive = []
        for a in self.arrows:
            dx = a.x - x
            dy = a.y - y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > radius:
                alive.append(a)
        self.arrows = alive

    def draw(self, d):
        for a in self.arrows:
            a.draw(d)
