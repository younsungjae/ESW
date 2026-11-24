import math
import random
from config import (W, H, ARROW_LEN, ARROW_HIT_R, MAX_ARROWS, PLAYER_HIT_R, GRAZE_DIST,
                    VOLLEY_OFFSETS, FAN_ANGLES, COLOR_ARROW)


class Arrow:
    def __init__(self, x, y, angle, speed):
        # angle은 도 단위 (0: 오른쪽, 90: 아래, 180: 왼쪽, -90: 위)
        self.x = x
        self.y = y
        rad = math.radians(angle)
        self.dir_x = math.cos(rad)
        self.dir_y = math.sin(rad)
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


def aim(x, y, target_x, target_y):
    # (x, y)에서 목표를 향하는 각도 (도 단위)
    return math.degrees(math.atan2(target_y - y, target_x - x))


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

    def add(self, x, y, angle, speed):
        self.arrows.append(Arrow(x, y, angle, speed))

    def shoot_single(self, player, speed):
        x, y = random_edge()
        # 플레이어 근처를 노리게 (정확히 노리면 너무 어려움)
        target_x = player.x + random.randint(-30, 30)
        target_y = player.y + random.randint(-30, 30)
        self.add(x, y, aim(x, y, target_x, target_y), speed)

    def shoot_volley(self, player, speed):
        # 일제사격: 한쪽 벽에서 나란히 직진
        side = random.randint(0, 3)
        for offset in VOLLEY_OFFSETS:
            if side == 0:
                self.add(player.x + offset, -5, 90, speed)      # 위에서 아래로
            elif side == 1:
                self.add(player.x + offset, H + 5, -90, speed)  # 아래에서 위로
            elif side == 2:
                self.add(-5, player.y + offset, 0, speed)       # 왼쪽에서 오른쪽으로
            else:
                self.add(W + 5, player.y + offset, 180, speed)  # 오른쪽에서 왼쪽으로

    def shoot_fan(self, player, speed):
        # 부채꼴: 한 점에서 펼쳐서
        x, y = random_edge()
        center = aim(x, y, player.x, player.y)
        for a in FAN_ANGLES:
            self.add(x, y, center + a, speed)

    def shoot_edge(self, player, stage):
        gap = stage.arrow_gap()
        speed = stage.arrow_speed()

        self.timer = self.timer + 1
        if self.timer >= gap and len(self.arrows) < MAX_ARROWS:
            pattern = stage.pick_pattern()
            if pattern == "single":
                self.shoot_single(player, speed)
                self.timer = 0
            elif pattern == "volley":
                self.shoot_volley(player, speed)
                self.timer = -gap * 3   # 여러 발 쐈으니 더 오래 쉼
            else:
                self.shoot_fan(player, speed)
                self.timer = -gap * 3

    def update(self, player, stage):
        if stage.shooting():
            self.shoot_edge(player, stage)

        for a in self.arrows:
            a.update()

        alive = []
        for a in self.arrows:
            if not a.is_out():
                alive.append(a)
        self.arrows = alive

    def clear_all(self):
        self.arrows = []

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
