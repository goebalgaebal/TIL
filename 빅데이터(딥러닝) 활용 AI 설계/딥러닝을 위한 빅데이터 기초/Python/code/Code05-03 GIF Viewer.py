#frame 참고 : http://openbookproject.net/py4fun/gui/tkPhone.html

from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
import os

## 전역변수 선언부 ##
dirList = []
num = 0 # 현재 사진 순번

## 함수 선언부 ##
def reloadImg(num) :
    photo = PhotoImage(file=dirList[num])
    pLabel.configure(image=photo)  # 기존에 존재하는 label의 속성을 바꿈
    pLabel.photo = photo

    label1.configure(text=dirList[num].split("\\")[-1])

def clickPrev() :
    global num
    num -= 1
    if num < 0 :
        num = len(dirList) - 1
    reloadImg(num)

def clickNext() :
    global num
    num += 1
    if num >= len(dirList) :
        num = 0
    reloadImg(num)

def keyPress(event) :
    global num

    # messagebox.showinfo("Title", event.keycode)

    if event.keycode == 36 : # Home key 입력
        num = 0
        reloadImg(num)

    elif event.keycode == 35 : # End key 입력
        num = len(dirList) - 1
        reloadImg(num)

    elif event.keycode == 37:  # ← 입력
        clickPrev()

    elif event.keycode == 39:  # → 입력
        clickNext()

    # 숫자 key 입력 씨, 현재 그림 + 숫자 위치 : 넘치면 마지막 그림
    elif event.keycode in range(97, 106) : # 97  = 1, 105 = 9
        num += event.keycode - 96

        if num >= len(dirList):
            num = len(dirList) -1
            reloadImg(num)

def hopImage(count = 0) :
    if count == 0 :
        count = askinteger("건너뛸 수", "원하시는 숫자를 입력해주세요 ", )
    for _ in range(count) :
        clickNext()

def selectFile() :
    filename = askopenfilename(parent = window, filetypes = (("GIF파일", "*.gif;*.raw"), ("모든파일", "*.*")))
    fnameLabel.configure(text = "선택한 파일 이름 : " + str(filename).split("/")[-1])

## 메인 코드 ##
window = Tk()
window.title("GIF 사진 뷰어 (ver 0.01)")
window.geometry("500x320")
window.resizable(width = True, height = True)

# folder = askdirectory(parent = window)
# for dirName, subDirList, fnames in os.walk(folder) :
for dirName, subDirList, fnames in os.walk("images\\") :
    for fname in fnames :
        if os.path.splitext(fname)[1].upper() == ".GIF" :
            dirList.append(os.path.join(dirName, fname))

#메뉴 생성
mainMenu = Menu(window)
window.config(menu = mainMenu)

moveMenu1 = Menu(mainMenu)
moveMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label = "이동", menu = moveMenu1)
mainMenu.add_cascade(label = "건너뛰기", menu = moveMenu2)

moveMenu1.add_cascade(label = "앞으로", command = clickNext)
moveMenu1.add_cascade(label = "뒤로", command = clickPrev)

# 매개변수를 넘기고싶을 때 lambda 함수 사용
moveMenu2.add_cascade(label = "1", command = lambda : hopImage(1))
moveMenu2.add_cascade(label = "3", command = lambda : hopImage(3))
moveMenu2.add_cascade(label = "5", command = lambda : hopImage(5))
moveMenu2.add_cascade(label = "원하는 수", command = hopImage)
moveMenu2.add_separator()
moveMenu2.add_command(label = "파일 선택", command = selectFile)

#버튼 프레임 생성
frame1 = Frame(window)
frame1.pack()

label1 = Label(frame1, text = dirList[num].split("\\")[-1])
btnPrev = Button(frame1, text = "이전", command = clickPrev)
btnNext = Button(frame1, text = "다음", command = clickNext)

btnPrev.grid(row = 0, column = 0)
label1.grid(row = 0, column = 1)
btnNext.grid(row = 0, column = 2)

#이미지 프레임 생성
frame2 = Frame(window)
frame2.pack()

photo = PhotoImage(file = dirList[num])
pLabel = Label(frame2, image = photo)
pLabel.pack(expand = 1, anchor = CENTER)

#키보드 입력 이벤트 처리
window.bind("<Key>", keyPress)

fnameLabel = Label(frame2, text = "선택한 파일 이름 : " + dirList[num].split("\\")[-1])
fnameLabel.pack()

window.mainloop()
