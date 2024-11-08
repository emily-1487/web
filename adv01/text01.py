import tkinter as tk
import random

# 初始化主窗口
root = tk.Tk()
root.title("隨機顏色切換範例")

# 創建標籤
label = tk.Label(root, text="Hello, World!", font=("Helvetica", 32))
label.pack(pady=20)

# 定義顏色列表
colors = [
    "red",
    "blue",
    "green",
    "yellow",
    "orange",
    "purple",
    "pink",
    "brown",
    "cyan",
    "magenta",
]


# 隨機切換顏色的函數
def toggle_color():
    new_color = random.choice(colors)
    label.config(fg=new_color)


# 創建按鈕
button = tk.Button(root, text="按我", command=toggle_color, font=("Helvetica", 24))
button.pack(pady=20)

# 運行主循環
root.mainloop()
