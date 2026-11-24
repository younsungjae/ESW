import math
import random
from config import W, BOSS_R, BOSS_ARROW_SPEED, SWORD_RADIUS, COLOR_TEXT, COLOR_GRAY


class Boss:
    def __init__(self, day):
        self.day = day
        self.x = W / 2
        self.y = -20          # 화면 위 밖에서 내려옴
        self.vx = 0.6         # 좌우로 움직이는 속도
        self.timer = 0
        self.enter = 120      # 등장 2초 동안은 공격도 안 하고 안 맞음
        self.hurt = 0         # 맞은 뒤 잠깐 깜빡 (이때는 안 맞음)

        # 보스마다 다른 값 (0이면 그 공격은 안 씀)
        if day == 1:
            self.name = "GWANGMA"
            self.hp = 3
            self.color = (230, 120, 40)
            self.single_gap = 12   # 무작위 한 발 간격
            self.circle_gap = 0    # 원형 확산 간격
        elif day == 2:
            self.name = "HYEOLMA"
            self.hp = 4
            self.color = (200, 30, 40)
            self.single_gap = 0
            self.circle_gap = 50
        else:
            self.name = "CHEONMA"
            self.hp = 5
            self.color = (180, 60, 255)
            self.single_gap = 16
            self.circle_gap = 70
        self.max_hp = self.hp
        self.turn = 0         # 원형 확산 각도를 조금씩 돌리기

    def update(self, arrows):
        if self.hurt > 0:
            self.hurt = self.hurt - 1

        # 등장: 천천히 내려오기만 함
        if self.enter > 0:
            self.enter = self.enter - 1
            self.y = self.y + 0.7
            return

        # 좌우로 왔다갔다
        self.x = self.x + self.vx
        if self.x < 30 or self.x > W - 30:
            self.vx = -self.vx

        single_gap = self.single_gap
        circle_gap = self.circle_gap
        speed = BOSS_ARROW_SPEED
        # 천마는 체력이 절반 이하면 더 빨라짐
        if self.day == 3 and self.hp <= self.max_hp / 2:
            single_gap = 10
            circle_gap = 45
            speed = speed + 0.4

        self.timer = self.timer + 1
        if single_gap > 0 and self.timer % single_gap == 0:
            self.shoot_random(arrows, speed)
        if circle_gap > 0 and self.timer % circle_gap == 0:
            self.shoot_circle(arrows, speed)

    def shoot_random(self, arrows, speed):
        # 아무 방향으로 한 발
        arrows.add(self.x, self.y, random.randint(0, 359), speed)

    def shoot_circle(self, arrows, speed):
        # 30도마다 한 발씩 한 바퀴 (12발)
        for angle in range(0, 360, 30):
            arrows.add(self.x, self.y, angle + self.turn, speed)
        # 다음엔 15도 돌려서 쏨 (빈틈 위치가 바뀜)
        if self.turn == 0:
            self.turn = 15
        else:
            self.turn = 0

    def in_range(self, player):
        # 검기가 닿는 거리인지
        dx = self.x - player.x
        dy = self.y - player.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < SWORD_RADIUS + BOSS_R:
            return True
        return False

    def hit(self):
        if self.enter > 0 or self.hurt > 0:
            return False
        self.hp = self.hp - 1
        self.hurt = 30
        return True

    def is_dead(self):
        if self.hp <= 0:
            return True
        return False

    def draw(self, d):
        if self.hurt > 0 and (self.hurt // 4) % 2 == 1:
            return
        r = BOSS_R
        d.ellipse((self.x - r, self.y - r, self.x + r, self.y + r), fill=self.color)
        d.ellipse((self.x - 4, self.y - 4, self.x + 4, self.y + 4), fill=(0, 0, 0))

    def draw_hp(self, d, font):
        # 화면 아래쪽에 이름과 체력 칸
        d.text((60, 206), self.name, font=font, fill=COLOR_TEXT)
        for i in range(self.max_hp):
            left = 60 + i * 24
            if i < self.hp:
                d.rectangle((left, 224, left + 20, 230), fill=self.color)
            else:
                d.rectangle((left, 224, left + 20, 230), outline=COLOR_GRAY)
