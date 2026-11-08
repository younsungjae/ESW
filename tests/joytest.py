import time                                            # 시간 측정·대기용
import board, digitalio                                # 핀 이름, 디지털 입출력

PINS = {                                               # 이름: 핀 번호 (방향은 실제와 다를 수 있어서 ? 표시)
    "UP?": board.D17, "DOWN?": board.D22,              # 조이스틱 위·아래
    "LEFT?": board.D27, "RIGHT?": board.D23,           # 조이스틱 왼쪽·오른쪽
    "CENTER": board.D4,                                # 조이스틱 누르기
    "BTN_A": board.D5, "BTN_B": board.D6,              # 앞면 버튼 A·B
}

btns = {}                                              # 버튼 객체를 담을 사전
for name, pin in PINS.items():                         # 핀마다 반복
    b = digitalio.DigitalInOut(pin)                    # 디지털 입출력으로 잡기
    b.direction = digitalio.Direction.INPUT            # 입력 모드
    b.pull = digitalio.Pull.UP                         # 풀업: 평소 HIGH, 누르면 LOW
    btns[name] = b                                     # 사전에 저장

print("20초간 눌러보세요...")                            # 안내
end = time.time() + 20                                 # 지금부터 20초 뒤 시각
while time.time() < end:                               # 20초 동안 반복 (폴링!)
    pressed = [n for n, b in btns.items() if not b.value]  # LOW(False)인 버튼 = 눌린 버튼 이름 모으기
    if pressed:                                        # 하나라도 눌렸으면
        print("PRESSED:", pressed)                     # 이름 출력
        time.sleep(0.2)                                # 같은 누름이 너무 많이 찍히지 않게 0.2초 쉼
    time.sleep(0.01)                                   # 10ms마다 확인 (CPU 과부하 방지)