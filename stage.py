import random
from config import (LOGIC_HZ, DAY_TIME, DUSK_TIME, REST_TIME, LAST_DAY,
                    ARROW_GAPS, ARROW_SPEEDS, ARROW_MIN_GAP, BG_COLORS)


class Stage:
    def __init__(self):
        self.day = 1
        self.phase = "morning"   # morning / dusk / night / rest
        self.timer = 0           # 지금 시간대가 시작되고 지난 계산 횟수
        self.banner = 120        # 시간대가 바뀔 때 큰 글씨 2초 표시
        self.finished = False

    def update(self):
        self.timer = self.timer + 1
        if self.banner > 0:
            self.banner = self.banner - 1

        if self.phase == "morning" and self.timer >= DAY_TIME * LOGIC_HZ:
            self.change("dusk")
        elif self.phase == "dusk" and self.timer >= DUSK_TIME * LOGIC_HZ:
            self.change("night")
        elif self.phase == "rest" and self.timer >= REST_TIME * LOGIC_HZ:
            self.day = self.day + 1
            self.change("morning")
        # 밤은 시간으로 안 끝나고, 보스를 잡으면 boss_defeated()로 넘어감

    def boss_defeated(self):
        if self.day == LAST_DAY:
            self.finished = True
        else:
            self.change("rest")

    def change(self, phase):
        self.phase = phase
        self.timer = 0
        self.banner = 120

    def arrow_gap(self):
        gap = ARROW_GAPS[self.phase] - (self.day - 1) * 4
        if gap < ARROW_MIN_GAP:
            gap = ARROW_MIN_GAP
        return gap

    def arrow_speed(self):
        return ARROW_SPEEDS[self.phase] + (self.day - 1) * 0.2

    def pick_pattern(self):
        # 1~10 중 하나를 뽑아서 시간대마다 다른 비율로 패턴 고르기
        n = random.randint(1, 10)
        if self.phase == "morning":
            if n <= 7:
                return "single"
            return "volley"
        if n <= 4:
            return "single"
        if n <= 6:
            return "volley"
        return "fan"

    def bg_color(self):
        # 날이 지날수록 숲이 어두워짐
        r, g, b = BG_COLORS[self.phase]
        dark = 1 - (self.day - 1) * 0.15
        return (int(r * dark), int(g * dark), int(b * dark))

    def name(self):
        if self.phase == "morning":
            return str(self.day) + "일차 낮"
        if self.phase == "dusk":
            return str(self.day) + "일차 해질녘"
        if self.phase == "night":
            return str(self.day) + "일차 밤"
        return str(self.day) + "일차 클리어"

    def banner_text(self):
        if self.phase == "morning":
            return str(self.day) + "일차"
        if self.phase == "dusk":
            return "해질녘"
        if self.phase == "night":
            return "WARNING"
        return str(self.day) + "일차 클리어!"

    def shooting(self):
        # 가장자리 화살은 낮과 해질녘에만
        if self.phase == "morning" or self.phase == "dusk":
            return True
        return False
