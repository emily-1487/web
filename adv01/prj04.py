#####################匯入模組###############################
from tkinter import *

#####################建立視窗###############################
windows = Tk()
windows.title("My first GUI")


#####################定義函數###############################
def hi_fun():
    global change
    if change == False:
        display.config(text="", fg="white", bg="white")
    else:
        display.config(text="按我會爆炸", fg="red", bg="black")
    change = not (change)


change = False

#####################建立按鈕###############################
btn1 = Button(windows, text="按我會爆炸", command=hi_fun)
btn1.pack()
# btn2 = Button(windows, text="瘋子才會按我", command=clean_fun)
# btn2.pack()
#####################建立標籤###############################
display = Label(windows, text="不要按我啊!!!")
display.pack()
#####################運行應用程式###############################
windows.mainloop()
