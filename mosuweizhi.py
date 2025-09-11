import pyautogui
import time
import os

def show_mouse_position():
    try:
        while True:
            x, y = pyautogui.position()
            os.system('cls')  # Windows清屏
            print(f"当前鼠标位置: X={x}, Y={y}")
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n已退出。")

if __name__ == "__main__":
    show_mouse_position()
