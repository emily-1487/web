#####################匯入模組###############################
from tkinter import *
from PIL import Image, ImageTk
import sys
import os

####################設定工作目錄##########################
os.chdir(sys.path[0])


####################定義函數###############################
def move_circle(event):
    key = event.keysym
    print(key)
    if key == "Right":
        canvas.move(circle, 10, 0)
    elif key == "Left":
        canvas.move(circle, -10, 0)
    elif key == "Up":
        canvas.move(circle, 0, -10)
    elif key == "Down":
        canvas.move(circle, 0, 10)
    elif key == "d":
        canvas.move(rect, 10, 0)
    elif key == "a":
        canvas.move(rect, -10, 0)
    elif key == "w":
        canvas.move(rect, 0, -10)
    elif key == "s":
        canvas.move(rect, 0, 10)


def exit_fun():
    windows.destroy()


#####################建立視窗###############################
windows = Tk()
windows.title("My first GUI")
#####################建立按鈕###############################
quit_btn = Button(windows, text="Quit", command=exit_fun)
quit_btn.pack()
####################創建畫布#############################
canvas = Canvas(windows, width=600, height=600, bg="white")
canvas.pack()
####################設定視窗圖片#############################\
# windows.iconbitmap("crocodile2.ico")
####################載入圖片####################
# img = PhotoImage(file="crocodile2.gif")
image = Image.open("crocodile2.gif")
img = ImageTk.PhotoImage(image)
#####################顯示圖片##############################
my_img = canvas.create_image(300, 300, image=img)
#####################畫圖片##############################
circle = canvas.create_oval(250, 150, 300, 200, fill="green")
rect = canvas.create_rectangle(220, 400, 340, 430, fill="blue")
msg = canvas.create_text(
    300,
    100,
    text="瑪莉歐say我弟是個壞孩子，非常壞的壞孩子",
    fill="black",
    font=("Arial", 20),
)
######################綁定案件事件############################
canvas.bind_all("<Key>", move_circle)

#####################運行應用程式###############################
windows.mainloop()
