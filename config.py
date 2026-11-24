import os

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
SWORD_RADIUS = 110     # 검기로 지우는 범위
SWORD_EFFECT_TIME = 15

# 하루 흐름 (초)
DAY_TIME = 25
DUSK_TIME = 35
REST_TIME = 3          # 보스 잡고 다음 날까지 쉬는 시간
LAST_DAY = 3

# 시간대별 화살: 몇 번 계산마다 한 발 / 속도 (날이 지날수록 더 어려워짐, 밤에는 보스만 쏨)
ARROW_GAPS = {"morning": 36, "dusk": 24}
ARROW_SPEEDS = {"morning": 1.5, "dusk": 1.9}

# 보스
BOSS_R = 12
BOSS_ARROW_SPEED = 1.6
BOSS_GAUGE = 5         # 보스전에서는 0.5초마다 게이지가 저절로 참

# 패턴 모양
VOLLEY_OFFSETS = [-56, -28, 0, 28, 56]   # 일제사격: 플레이어 기준으로 화살을 놓을 위치
FAN_ANGLES = [-30, -15, 0, 15, 30]       # 부채꼴: 가운데 방향에서 벌릴 각도 (도)

ARROW_LEN = 8
ARROW_HIT_R = 2
ARROW_MIN_GAP = 6        # 가장 빠를 때 6번마다 한 발 (0.1초)
MAX_ARROWS = 60

COLOR_BG = (12, 28, 18)
BG_COLORS = {"morning": (38, 72, 44), "dusk": (78, 44, 32), "night": (12, 16, 34), "rest": (40, 46, 70)}
COLOR_PLAYER = (255, 230, 240)
COLOR_HITBOX = (255, 60, 90)
COLOR_ARROW = (255, 220, 120)
COLOR_HP = (255, 80, 100)
COLOR_DASH = (120, 220, 255)
COLOR_GRAY = (90, 100, 95)
COLOR_SWORD = (200, 160, 255)
COLOR_TEXT = (200, 255, 200)

# 갈무리11 Bold (OFL 1.1, assets/fonts/OFL.md)
FONT_PATH = os.path.join(os.path.dirname(__file__), "assets", "fonts", "Galmuri11-Bold.ttf")
