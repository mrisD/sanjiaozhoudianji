import pyautogui
import pytesseract
from PIL import Image
import time

# Tesseract路径
pytesseract.pytesseract.tesseract_cmd = r"D:\ocrrr\tesseract.exe"

# 固定区域（左上角X, 左上角Y, 宽, 高）
PRICE_REGION = (1300, 770, 200, 30)
BUY_BUTTON = (1400, 850)
TARGET_PRICE = 800

def get_price_tesseract():
    """截图价格区域并用Tesseract识别"""
    screenshot = pyautogui.screenshot(region=PRICE_REGION)
    text = pytesseract.image_to_string(screenshot, config="--psm 7 digits")
    text = ''.join(filter(str.isdigit, text))
    return int(text) if text else None

def buy_item():
    """点击购买按钮"""
    pyautogui.moveTo(BUY_BUTTON[0], BUY_BUTTON[1], duration=0.2)
    pyautogui.click()
    print("已点击购买按钮！")

def auto_buy():
    time.sleep(3)  # 给你3秒切换到模拟器
    while True:
        price = get_price_tesseract()
        if price:
            print(f"当前价格: {price}")
            if price <= TARGET_PRICE:
                buy_item()

        else:
            print("未识别到价格")
        time.sleep(1)  # 每秒检测一次

if __name__ == "__main__":
    auto_buy()
