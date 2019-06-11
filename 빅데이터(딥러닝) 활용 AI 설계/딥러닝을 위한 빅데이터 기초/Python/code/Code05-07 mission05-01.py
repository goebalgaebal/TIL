from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
import os

## 전역변수 선언부 ##
fDir = None

## 함수 선언부 ##
def selectFile() :
    global fDir
    filename = askopenfilename(parent = window, filetypes = (("TXT파일", "*.txt;*.ini"), ("모든파일", "*.*")))

    if str(filename) == "" :
        messagebox.showinfo("Error", "파일이 선택되지 않았습니다")
        return
    label.configure(text = "선택한 파일 이름 : " + str(filename).split("/")[-1])
    fDir = str(filename)
    readFile(str(filename))

def readFile(filename) :
    text.delete(1.0, END)
    text.insert("end", open(filename, "r").read())

def saveFile():
    global fDir
    outFp = open(fDir, "w")
    outFp.write(text.get(1.0, END)[:-1])
    outFp.close()

## 메인 코드 ##
if __name__ == '__main__':
    window = Tk()
    window.title("메모장 (ver 0.01)")
    window.geometry("500x320")
    window.resizable(width = True, height = True)

    #메뉴 생성
    mainMenu = Menu(window)
    window.config(menu = mainMenu)

    fileMenu = Menu(mainMenu)
    editMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "파일", menu = fileMenu)
    mainMenu.add_cascade(label = "편집", menu = editMenu)

    fileMenu.add_cascade(label = "열기", command = selectFile)
    fileMenu.add_cascade(label = "저장", command = saveFile)

    editMenu.add_command(label = "바꾸기", command = None)
    editMenu.add_command(label = "복사", command = None)
    editMenu.add_command(label = "붙여넣기", command = None)

    label = Label(window, text = "[파일] → [열기] 에서 파일을 선택해주세요")
    label.pack()

    #text 위젯 생성
    text = Text(window)
    text.pack()
    window.mainloop()
