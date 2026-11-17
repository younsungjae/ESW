import random
from config import (LOGIC_HZ, DAY_TIME, DUSK_TIME, NIGHT_TIME, LAST_DAY,
                    ARROW_GAPS, ARROW_SPEEDS, ARROW_MIN_GAP, PATTERNS, BG_COLORS)


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
        table = PATTERNS[self.phase]
        names = list(table.keys())
        weights = list(table.values())
        return random.choices(names, weights)[0]

    def pattern_count(self):
        # 패턴 한 번에 쏘는 화살 수: 1일차 3발, 2일차 4발, 3일차 5발
        return 2 + self.day

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
