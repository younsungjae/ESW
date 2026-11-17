import math
import random
from config import (W, H, ARROW_LEN, ARROW_HIT_R, MAX_ARROWS, PLAYER_HIT_R, GRAZE_DIST,
                    VOLLEY_GAP, FAN_ANGLE, BURST_GAP, COLOR_ARROW)


class Arrow:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
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


def aim(x, y, target_x, target_y):
    # (x, y)에서 목표를 향하는 각도
    return math.atan2(target_y - y, target_x - x)


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
        # 조준 연사: 같은 자리에서 몇 발을 이어서 쏨
        self.burst_left = 0
        self.burst_timer = 0
        self.burst_x = 0
        self.burst_y = 0
        self.burst_speed = 0

    def add(self, x, y, angle, speed):
        self.arrows.append(Arrow(x, y, angle, speed))

    def shoot_single(self, player, speed):
        x, y = random_edge()
        # 플레이어 근처를 노리게 (정확히 노리면 너무 어려움)
        target_x = player.x + random.randint(-30, 30)
        target_y = player.y + random.randint(-30, 30)
        self.add(x, y, aim(x, y, target_x, target_y), speed)

    def shoot_volley(self, player, speed, count):
        # 일제사격: 한쪽 벽에서 나란히 직진
        side = random.randint(0, 3)
        for i in range(count):
            offset = (i - (count - 1) / 2) * VOLLEY_GAP
            if side == 0:
                self.add(player.x + offset, -5, math.radians(90), speed)    # 위 → 아래
            elif side == 1:
                self.add(player.x + offset, H + 5, math.radians(-90), speed)  # 아래 → 위
            elif side == 2:
                self.add(-5, player.y + offset, math.radians(0), speed)     # 왼쪽 → 오른쪽
            else:
                self.add(W + 5, player.y + offset, math.radians(180), speed)  # 오른쪽 → 왼쪽

    def shoot_fan(self, player, speed, count):
        # 부채꼴: 한 점에서 펼쳐서
        x, y = random_edge()
        center = aim(x, y, player.x, player.y)
        for i in range(count):
            offset = (i - (count - 1) / 2) * math.radians(FAN_ANGLE)
            self.add(x, y, center + offset, speed)

    def start_burst(self, speed, count):
        # 조준 연사 준비 (실제 발사는 update에서 한 발씩)
        self.burst_x, self.burst_y = random_edge()
        self.burst_left = count
        self.burst_timer = 0
        self.burst_speed = speed

    def update(self, player, stage):
        gap = stage.arrow_gap()
        speed = stage.arrow_speed()

        self.timer = self.timer + 1
        if self.timer >= gap and len(self.arrows) < MAX_ARROWS:
            pattern = stage.pick_pattern()
            count = stage.pattern_count()
            if pattern == "single":
                self.shoot_single(player, speed)
                self.timer = 0
            else:
                if pattern == "volley":
                    self.shoot_volley(player, speed, count)
                elif pattern == "fan":
                    self.shoot_fan(player, speed, count)
                elif pattern == "burst":
                    self.start_burst(speed, count)
                self.timer = -gap * 2   # 여러 발을 쐈으니 다음까지 세 배로 쉼

        if self.burst_left > 0:
            self.burst_timer = self.burst_timer - 1
            if self.burst_timer <= 0:
                angle = aim(self.burst_x, self.burst_y, player.x, player.y)   # 정확히 조준
                self.add(self.burst_x, self.burst_y, angle, self.burst_speed)
                self.burst_left = self.burst_left - 1
                self.burst_timer = BURST_GAP

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
