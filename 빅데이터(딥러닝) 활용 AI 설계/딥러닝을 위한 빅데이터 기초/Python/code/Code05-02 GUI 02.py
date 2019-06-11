from tkinter import *
from tkinter import messagebox
def clickButton() :
    messagebox.showinfo("요기 제목", "요기 내용")

window = Tk() # root = Tk()

label1 = Label(window, text = "python 공부 중") # Label(부모 - 객체를 붙일 창, option) 객체 생성
label2 = Label(window, text = "python 공부 중", font = ("궁서체", 30),fg = "blue")
label3 = Label(window, text = "python 공부 중", bg = "red", width = 20, height = 5, anchor = SE)

photo = PhotoImage(file = "images\Pet_GIF\Pet_GIF(128x128)/cat02_128.gif")
label4 = Label(window, image = photo)
button1 = Button(window, text = "나를 눌러줘", command = clickButton)
button2 = Button(window, image = photo, command = clickButton)

label1.pack(side = LEFT) # 생성한 객체를 붙인다
label2.pack(side = RIGHT)
label3.pack()
label4.pack()
button1.pack()
button2.pack()
window.mainloop()