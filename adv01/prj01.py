#####################匯入模組###############################
from tkinter import *

#####################建立視窗###############################
windows = Tk()
windows.title("My first GUI")


#####################定義函數###############################
def hi_fun():
    print("hi 沙必")


#####################建立按鈕###############################
btn1 = Button(windows, text="按我會爆炸", command=hi_fun)
btn1.pack()
#####################建立標籤###############################
display = Label(windows, text="不要按我啊!!!", fg="red", bg="black")
display.pack()
#####################運行應用程式###############################
windows.mainloop()
