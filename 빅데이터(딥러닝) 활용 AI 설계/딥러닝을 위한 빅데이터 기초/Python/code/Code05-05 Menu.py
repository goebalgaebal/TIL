from tkinter import *
from tkinter import messagebox
## 전역변수 선언부 ##

## 함수 선언부 ##
def fileClick() :
    messagebox.showinfo("요기 제목", "요기 내용")
## 메인 코드 ##
window = Tk()
window.geometry("500x300")
mainMenu = Menu(window)
window.config(menu = mainMenu)

fileMenu = Menu(mainMenu) # mainMenu에 fileMenu를 붙인다

mainMenu.add_cascade(label = "파일", menu = fileMenu)
fileMenu.add_cascade(label = "열기", command = fileClick)
fileMenu.add_separator()
fileMenu.add_cascade(label = "종료", command = None)

window.mainloop()
