from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
import os

## 전역변수 선언부 ##
photo = None

## 함수 선언부 ##
def loadImg(fileDir) :
    global photo
    photo = PhotoImage(file=fileDir)
    pLabel.configure(image=photo)
    pLabel.photo = photo
    print("load " + photo["file"])

def selectFile() :
    filename = askopenfilename(parent = window, filetypes = (("GIF파일", "*.gif;*.raw"), ("모든파일", "*.*")))

    if str(filename) == "" :
        messagebox.showinfo("Error", "파일이 선택되지 않았습니다")
        return
    label.configure(text = "선택한 파일 이름 : " + str(filename).split("/")[-1])

    loadImg(str(filename))

def zoomIn() :
    global photo

    if label["text"] == "[파일] → [사진 선택] 에서\n사진을 선택해주세요" :
        messagebox.showinfo("Error", "사진을 선택해주세요")
        return
    value = askinteger("확대배수", "확대할 배수를 입력하세요 (2~8)", minvalue = 1, maxvalue = 8)

    try :
        photo = photo.zoom(value, value)
        pLabel.configure(image=photo)
        pLabel.photo = photo

    except :
        messagebox.showinfo("Error", "배수가 입력되지 않았습니다")
        return


def zoomOut() :
    global photo
    if label["text"] == "[파일] → [사진 선택] 에서\n사진을 선택해주세요" :
        messagebox.showinfo("Error", "사진을 선택해주세요")
        return

    value = askinteger("축소배수", "축소할 배수를 입력하세요 (2~8)", minvalue = 1, maxvalue = 8)

    try :
        photo = photo.subsample(value, value)
        pLabel.configure(image=photo)
        pLabel.photo = photo

    except :
        messagebox.showinfo("Error", "배수가 입력되지 않았습니다")
        return

## 메인 코드 ##
if __name__ == '__main__':
    window = Tk()
    window.title("GIF 사진 뷰어 (ver 0.01)")
    window.geometry("500x320")
    window.resizable(width = True, height = True)

    #메뉴 생성
    mainMenu = Menu(window)
    window.config(menu = mainMenu)

    fileMenu = Menu(mainMenu)
    effectMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "파일", menu = fileMenu)
    mainMenu.add_cascade(label = "이미지 효과", menu = effectMenu)

    fileMenu.add_cascade(label = "사진 선택", command = selectFile)

    effectMenu.add_command(label = "확대하기", command = zoomIn)
    effectMenu.add_command(label = "축소하기", command = zoomOut)

    #사진과 사진 파일명 출력 객체 생성
    photo = PhotoImage(file = "")
    pLabel = Label(window, image = photo)
    pLabel.pack(expand = 1, anchor = CENTER)

    label = Label(window, text = "[파일] → [사진 선택] 에서\n사진을 선택해주세요")
    label.pack()

    window.mainloop()
