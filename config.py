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

ARROW_SPEED = 1.5        # 처음 속도
ARROW_LEN = 8
ARROW_HIT_R = 2
ARROW_START_GAP = 40     # 처음엔 40번 계산마다 한 발 (약 0.67초)
ARROW_MIN_GAP = 6        # 가장 빠를 때 6번마다 한 발 (0.1초)
MAX_ARROWS = 60

COLOR_BG = (12, 28, 18)
COLOR_PLAYER = (255, 230, 240)
COLOR_HITBOX = (255, 60, 90)
COLOR_ARROW = (255, 220, 120)
COLOR_HP = (255, 80, 100)
COLOR_TEXT = (200, 255, 200)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
