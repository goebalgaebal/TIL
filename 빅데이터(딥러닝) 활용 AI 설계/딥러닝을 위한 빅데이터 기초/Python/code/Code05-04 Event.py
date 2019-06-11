from tkinter import *
from tkinter import messagebox
## 전역변수 선언부 ##

## 함수 선언부 ##
def click(event) :
    txt = ""
    if event.num == 1 : # 왼쪽 버튼
        txt += "왼쪽버튼 : "
    elif event.num == 3 : # 오른쪽 버튼
        txt += "오른쪽버튼 : "
    else :
        txt += "가운데 버튼 : "
    txt += str(event.x) + ", " + str(event.y)
    messagebox.showinfo("요기 제목", txt)

def keyPress(event) :
    messagebox.showinfo("요기 제목", chr(event.keycode))

## 메인 코드 ##
window = Tk()
window.geometry("500x300")

window.bind("<Button>", click)

photo = PhotoImage(file = "images\Pet_GIF\Pet_GIF(128x128)/cat02_128.gif")
label1 = Label(window, image = photo)

# window.bind("<Key>", keyPress)
window.bind("a", keyPress)

label1.pack(expand = 1, anchor = CENTER)
window.mainloop()
