import pyautogui
import pytesseract
from PIL import Image
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import sys
import ctypes

def is_admin():
    """判断当前是否有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # 如果没有管理员权限，就以管理员身份重新运行脚本
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()  # 退出当前进程，新的进程继续运行

print("已以管理员模式运行！")
# 默认配置
config = {
    "price_region_x": 290,
    "price_region_y": 170,
    "price_region_w": 50,
    "price_region_h": 30,
    "buy_button_x": 1640,
    "buy_button_y": 865,
    "target_price": 800,
    "shuaxin_x":130,
    "shuaxin_y":180,
    "tesseract_cmd": r"D:\ocrrr\tesseract.exe",
}

running = False  # 控制自动购买循环


# ----------- 核心逻辑 -----------
MAX_LOG_LINES = 200  # 最多保留200行

def log(message):
    txt_log.config(state='normal')
    txt_log.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
    # 删除多余行
    lines = txt_log.get("1.0", tk.END).splitlines()
    if len(lines) > MAX_LOG_LINES:
        txt_log.delete("1.0", f"{len(lines) - MAX_LOG_LINES + 1}.0")
    txt_log.see(tk.END)
    txt_log.config(state='disabled')



def get_price_tesseract():
    region = (
        config["price_region_x"],
        config["price_region_y"],
        config["price_region_w"],
        config["price_region_h"]
    )
    screenshot = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(screenshot, config="--psm 7 digits")
    text = ''.join(filter(str.isdigit, text))
    return int(text) if text else None


def buy_item():
    pyautogui.moveTo(config["buy_button_x"], config["buy_button_y"], duration=0.2)
    pyautogui.click()
    log("已点击购买按钮！")
    pyautogui.moveTo(config["shuaxin_x"], config["shuaxin_y"], duration=0.2)
    pyautogui.click()



def auto_buy():
    """自动购买循环（子线程运行）"""
    # Tesseract路径
    pytesseract.pytesseract.tesseract_cmd = config.get("tesseract_cmd")
    time.sleep(3)  # 切换到模拟器
    log("开始自动购买...")
    while running:
        price = get_price_tesseract()
        if price:
            log(f"当前价格: {price}")
            if price <= config["target_price"]:
                buy_item()
        else:
            log("未识别到价格")
        time.sleep(0.1)
    log("自动购买已停止")


# ----------- GUI 回调 -----------
def start_auto_buy():
    global running
    if running:
        messagebox.showinfo("提示", "自动购买已经在运行中！")
        return
    running = True
    messagebox.showinfo("提示", "3秒后开始自动购买，请切换到模拟器界面！")
    t = threading.Thread(target=auto_buy, daemon=True)
    t.start()


def stop_auto_buy():
    global running
    running = False


def save_config():
    try:
        config["price_region_x"] = int(entry_price_x.get())
        config["price_region_y"] = int(entry_price_y.get())
        config["price_region_w"] = int(entry_price_w.get())
        config["price_region_h"] = int(entry_price_h.get())
        config["buy_button_x"] = int(entry_buy_x.get())
        config["buy_button_y"] = int(entry_buy_y.get())
        config["target_price"] = int(entry_target_price.get())
        config["shuaxin_x"] = int(entry_refresh_x.get())
        config["shuaxin_y"] = int(entry_refresh_y.get())
        config["tesseract_cmd"] = int(entry_tesseract.get())
        log("配置已保存！")
    except ValueError:
        messagebox.showerror("错误", "请输入正确的数字！")


# ----------- GUI 界面 -----------
root = tk.Tk()
root.title("自动购买工具")
root.geometry("500x480")  # 高度调大一些
root.resizable(False, False)

# 价格区域
tk.Label(root, text="价格区域 X:").grid(row=0, column=0, padx=5, pady=5)
entry_price_x = tk.Entry(root, width=10)
entry_price_x.grid(row=0, column=1)
entry_price_x.insert(0, config["price_region_x"])

tk.Label(root, text="价格区域 Y:").grid(row=0, column=2, padx=5, pady=5)
entry_price_y = tk.Entry(root, width=10)
entry_price_y.grid(row=0, column=3)
entry_price_y.insert(0, config["price_region_y"])

tk.Label(root, text="宽度 W:").grid(row=1, column=0, padx=5, pady=5)
entry_price_w = tk.Entry(root, width=10)
entry_price_w.grid(row=1, column=1)
entry_price_w.insert(0, config["price_region_w"])

tk.Label(root, text="高度 H:").grid(row=1, column=2, padx=5, pady=5)
entry_price_h = tk.Entry(root, width=10)
entry_price_h.grid(row=1, column=3)
entry_price_h.insert(0, config["price_region_h"])

# 购买按钮
tk.Label(root, text="购买按钮 X:").grid(row=2, column=0, padx=5, pady=5)
entry_buy_x = tk.Entry(root, width=10)
entry_buy_x.grid(row=2, column=1)
entry_buy_x.insert(0, config["buy_button_x"])

tk.Label(root, text="购买按钮 Y:").grid(row=2, column=2, padx=5, pady=5)
entry_buy_y = tk.Entry(root, width=10)
entry_buy_y.grid(row=2, column=3)
entry_buy_y.insert(0, config["buy_button_y"])

# ✅ 新增刷新按钮（插在购买按钮和目标价格之间）
tk.Label(root, text="刷新按钮 X:").grid(row=3, column=0, padx=5, pady=5)
entry_refresh_x = tk.Entry(root, width=10)
entry_refresh_x.grid(row=3, column=1)
entry_refresh_x.insert(0, config["shuaxin_x"])

tk.Label(root, text="刷新按钮 Y:").grid(row=3, column=2, padx=5, pady=5)
entry_refresh_y = tk.Entry(root, width=10)
entry_refresh_y.grid(row=3, column=3)
entry_refresh_y.insert(0, config["shuaxin_y"])

# 目标价格（下移一行）
tk.Label(root, text="目标价格:").grid(row=4, column=0, padx=5, pady=5)
entry_target_price = tk.Entry(root, width=10)
entry_target_price.grid(row=4, column=1)
entry_target_price.insert(0, config["target_price"])

# 按钮
tk.Button(root, text="保存配置", command=save_config, width=15).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="开始自动购买", command=start_auto_buy, width=15, bg="green", fg="white").grid(row=5, column=2, columnspan=2)
tk.Button(root, text="停止", command=stop_auto_buy, width=15, bg="red", fg="white").grid(row=6, column=0, columnspan=4, pady=5)

# tesseract位置
tk.Label(root, text="tesseract位置:").grid(row=7, column=0, padx=5, pady=5)
entry_tesseract = tk.Entry(root, width=30)
entry_tesseract.grid(row=7, column=1)
entry_tesseract.insert(0, config["tesseract_cmd"])
# 日志输出区域
txt_log = scrolledtext.ScrolledText(root, width=60, height=10, state='disabled')
txt_log.grid(row=8, column=0, columnspan=4, padx=5, pady=10)

root.mainloop()
