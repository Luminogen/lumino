import pyautogui
import time
import subprocess
import os
import pyperclip
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# 카카오톡 실행 및 로그인
def run_kakaotalk():
    kakaotalk_path = r"C:\Program Files (x86)\Kakao\KakaoTalk\KakaoTalk.exe"
    
    if os.path.exists(kakaotalk_path):
        kakaotalk_process = subprocess.Popen(kakaotalk_path)
        print("카카오톡을 실행했습니다.")
        return kakaotalk_process  # 프로세스 반환
    else:
        print("카카오톡 실행 파일을 찾을 수 없습니다.")
        return None

def enter_password(password):
    # 잠시 대기하여 카카오톡이 실행된 후 비밀번호 입력 창이 뜨는 시간을 확보
    time.sleep(10)

    # 비밀번호 입력
    pyautogui.write(password)
    pyautogui.press('enter')
    print("비밀번호를 입력하고 로그인 시도했습니다.")

def navigate_to_chat_menu():
    # 채팅 메뉴로 이동하는 로직 (채팅 메뉴 버튼의 좌표를 설정)
    time.sleep(3)  # 카카오톡이 로그인된 후 대기
    chat_menu_button_coords = (796, 315)  # 여기에 실제 채팅 메뉴 버튼 좌표를 입력하세요.
    pyautogui.doubleClick(chat_menu_button_coords)
    print("채팅 메뉴로 이동했습니다.")

def open_chatroom(name):
    # 채팅방 이름으로 검색 (Ctrl+F 또는 검색 기능을 사용하여 채팅방 찾기)
    time.sleep(3)  # 채팅 메뉴로 진입 후 대기

    # 검색창 클릭 (검색창 위치에 맞는 좌표 필요)
    search_box_coords = (1044, 256)  # 여기에 검색창 좌표를 입력하세요.
    pyautogui.click(search_box_coords)

    # 한글 채팅방 이름을 클립보드로 복사하고 붙여넣기
    pyperclip.copy(name)
    time.sleep(2)
    
    # Ctrl + V로 붙여넣기
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    # 채팅방 이름 입력 후 엔터
    pyautogui.press('enter')
    print(f"{name} 채팅방을 찾았습니다.")

def send_message(message):
    # 클립보드에 메시지 복사
    pyperclip.copy(message)
    # 붙여넣기 (Ctrl + V)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    print(f"메시지를 보냈습니다: {message}")

# Playwright로 데이터를 가져오는 함수
def get_coinness_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Coinness 웹 페이지로 이동
        page.goto("https://coinness.com/")

        # 페이지의 HTML 콘텐츠 가져오기
        content = page.content()

        # BeautifulSoup을 사용하여 데이터를 파싱
        soup = BeautifulSoup(content, "html.parser")

        # 특정 클래스명을 가진 div 안에 있는 a 태그만 선택
        div = soup.find('div', class_='BreakingNewsTitle-sc-glfxh-4 dFiHgV')
        if div:
            # 각 a 태그의 텍스트 추출 (줄바꿈과 공백을 포함하여 정확하게)
            a_tags = div.find_all('a')
            texts = [a.get_text() for a in a_tags]
            return texts
        else:
            return []

# 10분마다 스크립트 실행하기
def run_every_10_minutes():
    previous_message = ""  # 이전에 전송된 메시지를 저장할 변수

    while True:
        # 카카오톡 실행
        kakaotalk_process = run_kakaotalk()
        if kakaotalk_process:
            enter_password("")  # 비밀번호 입력
            
            # 채팅 메뉴로 이동
            navigate_to_chat_menu()

            # ''라는 이름의 채팅방 열기
            open_chatroom("")

            # Playwright로 Coinness 데이터를 가져와서 메시지로 전송
            coinness_data = get_coinness_data()
            if coinness_data:
                # 새로운 메시지 생성
                message = "⚛속보\n" + '\n'.join(coinness_data)

                # 이전 메시지와 비교하여 새로운 데이터가 있는지 확인
                if message != previous_message:
                    send_message(message)  # 메시지를 채팅창에 입력
                    previous_message = message  # 새로운 메시지를 이전 메시지로 저장
                else:
                    print("새로운 데이터가 없어서 메시지를 전송하지 않았습니다.")
            else:
                print("Coinness 데이터를 가져오지 못했습니다.")
            
            time.sleep(5)  # 스크립트 종료 전에 대기하여 동작을 확인
            print("카카오톡 자동화가 완료되었습니다.")
        else:
            print("카카오톡을 실행할 수 없습니다.")
        
        # 카카오톡 프로세스를 종료
        if kakaotalk_process:
            kakaotalk_process.terminate()
            print("카카오톡 프로세스를 종료했습니다.")

        # 10분 대기 (600초) 중 1분마다 상태를 출력
        for i in range(10):
            print(f"I'm still running... {i + 1}분 경과")
            time.sleep(60)  # 1분 대기

# 메인 로직 실행
if __name__ == "__main__":


    run_every_10_minutes()
