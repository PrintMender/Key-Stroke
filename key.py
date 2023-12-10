#f5 をしたときに出てくるPython Debugのターミナルにpipやpyinstallerなどをぶち込む
# pyinstaller --add-data "./images;images", "./icon.ico"  key.py --onefile --noconsole

#エラーの場合
#windowsのターミナルで
# pyinstaller icon.spec

from pynput.mouse import Listener, Button
import threading
import time
import tkinter as tk
from PIL import Image, ImageTk
import keyboard
import os
import sys

left_click_count = 0
right_click_count = 0
start_time = time.time()
left_click = False
right_click = False
global running
running = True
def on_click(x, y, button, pressed):
    global left_click_count, right_click_count, start_time, left_click, right_click

    if pressed:
        if button == Button.left:
            left_click_count += 1
            left_click = True
        elif button == Button.right:
            right_click_count += 1
            right_click = True
    else:
        if button == Button.left:
            left_click = False
        elif button == Button.right:
            right_click = False

    check_clicks()

def check_clicks():
    if left_click and right_click:
        label_lmb.config(image=image_lmb_pressed)
        label_rmb.config(image=image_rmb_pressed)
    elif left_click:
        label_lmb.config(image=image_lmb_pressed)
        label_rmb.config(image=image_rmb)  # 右クリックが解除された場合、通常の画像に戻す
    elif right_click:
        label_lmb.config(image=image_lmb)  # 左クリックが解除された場合、通常の画像に戻す
        label_rmb.config(image=image_rmb_pressed)
    else:
        label_lmb.config(image=image_lmb)
        label_rmb.config(image=image_rmb)

def start_listener():
    with Listener(on_click=on_click) as listener:
        listener.join()

def calculate_clicks_per_second():
    global left_click_count, right_click_count, start_time, running

    while running:
        time.sleep(1)
        elapsed_time = time.time() - start_time
        left_clicks_per_second = left_click_count / elapsed_time
        right_clicks_per_second = right_click_count / elapsed_time

        lmb_cps_label.config(text=f"Left cps : {left_clicks_per_second:.2f}")
        rmb_cps_label.config(text=f"Right cps : {right_clicks_per_second:.2f}")
        #print(f"Left clicks per second: {left_clicks_per_second:.2f}, Right clicks per second: {right_clicks_per_second:.2f}")

        # リセット
        left_click_count = 0
        right_click_count = 0
        start_time = time.time()

# クリック計測スレッドを開始
click_thread = threading.Thread(target=calculate_clicks_per_second)
click_thread.start()

def on_closing():
    global running
    running = False
    root.destroy()  # ウィンドウを閉じる

def main():
    def load_image(file_name, width, height):
        if getattr(sys, 'frozen', False):
            # 実行ファイルが一時ディレクトリに展開された場合
            current_dir = os.path.dirname(sys.executable)
            file_path = os.path.join(current_dir, "images", file_name)
        else:
            # 通常の実行時
            file_path = os.path.join(os.path.dirname(__file__), "images", file_name)
       
        image = Image.open(file_path)
        image = image.resize((width, height))
        photo = ImageTk.PhotoImage(image)
        return photo

    def on_key_event(e):
        if e.event_type == keyboard.KEY_DOWN:
            on_key_pressed(e.name)
        elif e.event_type == keyboard.KEY_UP:
            on_key_released(e.name)

    def on_key_pressed(key):
        #print(key)
        if key == "w" or key == "W":
            label_w.config(image=image_w_pressed)
        elif key == "a" or key == "A":
            label_a.config(image=image_a_pressed)
        elif key == "s" or key == "S":
            label_s.config(image=image_s_pressed)
        elif key == "d" or key == "D":
            label_d.config(image=image_d_pressed)
        elif key == "space":
            label_space.config(image=image_space_pressed)

    def on_key_released(key):
        if key == "w" or key == "W":
            label_w.config(image=image_w)
        elif key == "a" or key == "A":
            label_a.config(image=image_a)
        elif key == "s" or key == "S":
            label_s.config(image=image_s)
        elif key == "d" or key == "D":
            label_d.config(image=image_d)
        elif key == "space":
            label_space.config(image=image_space)

    # Tkinterウィンドウを作成
    global root
    root = tk.Tk()
    root.title("key stroke")
    root.geometry("155x300")
    root.resizable(False, False)
    root.wm_attributes("-transparentcolor", "white")
    tk.Frame(root, background="white").pack(expand=True, fill=tk.BOTH)
    root.lift()
    root.wm_attributes("-topmost", 1)
    root.overrideredirect(False)
    root.iconbitmap("./icon.ico")


    # WASDの画像をロード
    width, height = 50, 50  # 画像の幅と高さを指定
    image_w = load_image("w.png", width, height)
    image_a = load_image("a.png", width, height)
    image_s = load_image("s.png", width, height)
    image_d = load_image("d.png", width, height)
    image_space = load_image("space.png", 150, height)
    global image_lmb, image_rmb
    image_lmb = load_image("lmb.png", 75, height)
    image_rmb = load_image("rmb.png", 75, height)

    image_w_pressed = load_image("w_p.png", width, height)
    image_a_pressed = load_image("a_p.png", width, height)
    image_s_pressed = load_image("s_p.png", width, height)
    image_d_pressed = load_image("d_p.png", width, height)
    image_space_pressed = load_image("space_p.png", 150, height)
    global image_lmb_pressed, image_rmb_pressed
    image_lmb_pressed = load_image("lmb_p.png", 75,height)
    image_rmb_pressed = load_image("rmb_p.png", 75, height)
    # WASDのラベルを作成
    label_w = tk.Label(root, image=image_w, relief="flat")
    label_w.place(x=50, y=0)

    label_a = tk.Label(root, image=image_a, relief="flat")
    label_a.place(x=0, y=50)

    label_s = tk.Label(root, image=image_s, relief="flat")
    label_s.place(x=50, y=50)

    label_d = tk.Label(root, image=image_d, relief="flat")
    label_d.place(x=100, y=50)

    global label_lmb
    label_lmb = tk.Label(root, image=image_lmb, relief="flat")
    label_lmb.place(x=0, y=100)

    global label_rmb
    label_rmb = tk.Label(root, image=image_rmb, relief="flat")
    label_rmb.place(x=75, y=100)

    label_space = tk.Label(root, image=image_space, relief="flat")
    label_space.place(x=0, y=150)

    global lmb_cps_label
    lmb_cps_label = tk.Label(root, text="Left cps : ")
    lmb_cps_label.place(x=0, y=210)
    lmb_cps_label.config(font="Arial")

    global rmb_cps_label
    rmb_cps_label = tk.Label(root, text="Right cps : ")
    rmb_cps_label.place(x=0, y=240)
    rmb_cps_label.config(font="Arial")

    # 別スレッドでpynputのリスナーを開始
    listener_thread = threading.Thread(target=start_listener, daemon=True)
    listener_thread.start()

    keyboard.hook(on_key_event)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.bind("<ButtonPress-1>", lambda event: start_drag(root, event))
    root.bind("<B1-Motion>", lambda event: on_drag_motion(root, event)) 


    # Tkinterウィンドウを表示
    root.mainloop()

def start_drag(root, event):
    root.x = event.x
    root.y = event.y

def on_drag_motion(root, event):
    x = root.winfo_x() + (event.x - root.x)
    y = root.winfo_y() + (event.y - root.y)
    root.geometry(f"+{x}+{y}")
    
if __name__ == "__main__":
    main()
