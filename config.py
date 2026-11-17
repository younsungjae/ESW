# 화면 가로세로
W = 240 
H = 240

LOGIC_HZ = 60
STEP = 1 / LOGIC_HZ
FPS = 20

PLAYER_SPEED = 2.0
PLAYER_DRAW_R = 7  # 그림 반지름
PLAYER_HIT_R = 3   # 판정 반지름, 판정은 그림보다 작게 함
PLAYER_HP = 3
INVINCIBLE_TIME = 90   # 맞은 뒤 무적 1.5초

DASH_SPEED = 4.5       # 대시 중 한 번에 이동하는 거리
DASH_TIME = 10         # 대시 지속 (약 0.17초, 이동 거리 약 45)
DASH_COOLDOWN = 180    # 다시 쓰려면 3초

GRAZE_DIST = 16        # 중심 거리가 이보다 가까우면 스침 (맞는 거리는 5)
GAUGE_PER_GRAZE = 10   # 한 번 스칠 때 게이지
GAUGE_MAX = 100        # 게이지가 다 차면 검기 1개
SWORD_MAX = 3
SWORD_RADIUS = 70      # 검기로 지우는 범위
SWORD_EFFECT_TIME = 15

# 하루 흐름 (초)
DAY_TIME = 25
DUSK_TIME = 35
NIGHT_TIME = 20        # 보스 넣기 전까지 임시로 밤도 시간으로 넘어감
LAST_DAY = 3

# 시간대별 화살: 몇 번 계산마다 한 발 / 속도 (날이 지날수록 더 어려워짐)
ARROW_GAPS = {"morning": 36, "dusk": 24, "night": 18}
ARROW_SPEEDS = {"morning": 1.5, "dusk": 1.9, "night": 2.2}

# 시간대별 패턴이 나올 비율 (숫자가 클수록 자주)
PATTERNS = {
    "morning": {"single": 7, "volley": 3},
    "dusk": {"single": 4, "volley": 2, "fan": 4},
    "night": {"single": 2, "volley": 2, "fan": 3, "burst": 3},
}
VOLLEY_GAP = 28        # 일제사격 화살 사이 간격 (픽셀)
FAN_ANGLE = 15         # 부채꼴 화살 사이 각도
BURST_GAP = 10         # 조준 연사 발사 간격

ARROW_LEN = 8
ARROW_HIT_R = 2
ARROW_MIN_GAP = 6        # 가장 빠를 때 6번마다 한 발 (0.1초)
MAX_ARROWS = 60

COLOR_BG = (12, 28, 18)
BG_COLORS = {"morning": (38, 72, 44), "dusk": (78, 44, 32), "night": (12, 16, 34)}
COLOR_PLAYER = (255, 230, 240)
COLOR_HITBOX = (255, 60, 90)
COLOR_ARROW = (255, 220, 120)
COLOR_HP = (255, 80, 100)
COLOR_DASH = (120, 220, 255)
COLOR_GRAY = (90, 100, 95)
COLOR_SWORD = (200, 160, 255)
COLOR_TEXT = (200, 255, 200)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
