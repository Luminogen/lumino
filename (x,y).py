import pyautogui
import time

print("마우스를 원하는 위치에 두고 좌표를 확인하세요.")

try:
    while True:
        x, y = pyautogui.position()  # 현재 마우스 좌표
        print(f"현재 마우스 좌표: ({x}, {y})")
        time.sleep(1)  # 1초 간격으로 좌표를 출력
except KeyboardInterrupt:
    print("좌표 확인이 중지되었습니다.")