import random
from config import (LOGIC_HZ, DAY_TIME, DUSK_TIME, NIGHT_TIME, LAST_DAY,
                    ARROW_GAPS, ARROW_SPEEDS, ARROW_MIN_GAP, BG_COLORS)


class Stage:
    def __init__(self):
        self.day = 1
        self.phase = "morning"   # morning / dusk / night
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
        elif self.phase == "night" and self.timer >= NIGHT_TIME * LOGIC_HZ:
            # 임시: 보스 넣으면 보스를 잡았을 때 넘어가게 바꿀 것
            if self.day == LAST_DAY:
                self.finished = True
            else:
                self.day = self.day + 1
                self.change("morning")

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
        if self.phase == "dusk":
            if n <= 4:
                return "single"
            if n <= 6:
                return "volley"
            return "fan"
        if n <= 3:
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
        return "DAY " + str(self.day) + " " + self.phase.upper()

    def banner_text(self):
        if self.phase == "morning":
            return "DAY " + str(self.day)
        return self.phase.upper()
