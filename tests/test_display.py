import time                                           # 시간 지연(sleep)용
import board, digitalio                               # 핀 이름, 디지털 입출력
from PIL import Image, ImageDraw                      # 그림 그릴 도화지(Image)와 붓(ImageDraw)
from adafruit_rgb_display import st7789              # 화면 칩 ST7789 드라이버

cs_pin  = digitalio.DigitalInOut(board.CE0)           # 화면 선택(CS) 핀 = CE0 (GPIO8)
dc_pin  = digitalio.DigitalInOut(board.D25)           # DC 핀: 지금 보내는 게 "명령"인지 "픽셀 데이터"인지 구분
rst_pin = digitalio.DigitalInOut(board.D24)           # 화면 리셋 핀

backlight = digitalio.DigitalInOut(board.D26)         # 백라이트 핀 (GPIO26)
backlight.switch_to_output()                          # 출력 모드로 설정
backlight.value = True                                # HIGH → 백라이트 켜기 (안 켜면 화면이 계속 검정)

spi = board.SPI()                                     # SPI 통로 열기
disp = st7789.ST7789(                                 # 화면 객체 만들기
    spi, width=240, height=240, rotation=180, y_offset=80,           # 240x240 해상도, 회전 없음
    cs=cs_pin, dc=dc_pin, rst=rst_pin, baudrate=24000000,  # 위의 핀들 연결, SPI 속도 24MHz
)

img = Image.new("RGB", (disp.width, disp.height))    # 화면 크기만 한 빈 도화지
draw = ImageDraw.Draw(img)                            # 그 도화지에 그릴 붓
for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]:  # 빨강, 초록, 파랑, 흰색 순서로
    draw.rectangle((0, 0, 239, 239), fill=color)     # 도화지 전체를 그 색으로 칠하고
    disp.image(img)                                   # 화면으로 전송
    print("color", color)                             # 터미널에도 현재 색 출력
    time.sleep(0.6)                                   # 0.6초 대기

draw.rectangle((0, 0, 239, 239), fill=(0, 0, 0))     # 검정으로 지우고
draw.text((20, 110), "READY", fill=(0, 255, 0))      # 초록색 READY 글자
disp.image(img)                                       # 화면으로 전송
print("done")                                         # 끝
