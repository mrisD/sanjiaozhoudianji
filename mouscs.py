import pyautogui
PRICE_REGION = (1016, 356, 100, 50)
BUY_BUTTON = (950, 600)
pyautogui.moveTo(BUY_BUTTON[0], BUY_BUTTON[1], duration=0.2)
screenshot = pyautogui.screenshot(region=PRICE_REGION).save('1.jpg')
