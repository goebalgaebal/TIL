'''
데이터 시각화 및 컴퓨터 비전 알고리즘 중에서 RAW 데이터를 반전하는 reverse() 함수를 다음 조건에 맞춰 구현하시오.
- 메모리 할당은 malloc(높이, 폭) 함수를 사용한다.
- 화면 출력은 display() 함수를 사용한다.
- 전역 변수 : window, canvas, paper, inW, inH, outW, outH, inImage, outImage
'''
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import numpy as np

#################
## 함수 선언부 ##
#################
def malloc(h, w, initValue = 0, dataType = "uint8") :
    returnMemory = []
    returnMemory = np.zeros((h, w), dtype = dataType)
    returnMemory += initValue
    return returnMemory

def loadImage(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = os.path.getsize(fname)
    inH = inW = int(math.sqrt(fsize))

    inImage = []
    inImage = np.fromfile(fname, dtype = "uint8")
    inImage = inImage.reshape([inH, inW])

    print("LOAD 입력 크기", inH, inW)

def openImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw;"), ("모든 파일", "*.*")))
    if filename == "" or filename == None :
        messagebox.showinfo("Error", "출력하고자 하는 파일을 선택해주세요")
        return
    loadImage(filename)
    equalImage()

def displayImage() :
    global imageFrame, btnFrame, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y
    if canvas != None :
        canvas.destroy()

    if inH <= VIEW_Y or inW <= VIEW_X :
        outW = inW
        outH = inH
        step = 1
    else :
        outW = VIEW_X
        outH = VIEW_Y
        step = inW / VIEW_X

    window.geometry(str(int(outH * 1.2)) + 'x' + str(int(outW * 1.2)))
    canvas = Canvas(window, height=outH, width=outW)
    paper = PhotoImage(height=outH, width=outW)
    canvas.create_image((outH // 2, outW // 2), image=paper, state="normal")


    import numpy
    rgbStr = ""
    for i in numpy.arange(0, inH, step) :
        tmpStr = ""
        for k in numpy.arange(0, inW, step) :
            i = int(i); k = int(k)
            r = g = b = int(outImage[i][k])
            tmpStr += ' #%02x%02x%02x'  % (r, g, b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.pack(expand = 1, anchor = CENTER)
    status.configure(text = "이미지 정보 : " + str(outW) + 'x' + str(outH))

# 동일 영상 알고리즘
def equalImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    outImage = inImage[:]
    displayImage()

# 반전영상 알고리즘
def reverseImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if filename == "" or filename == None :
        messagebox.showinfo("Error", "파일을 선택해주세요")
        return

    outImage = 255 - inImage
    displayImage()
    print("화소값 반전 완료")

#####################
## 전역변수 선언부 ##
#####################
inImage, outImage = [], []
inH, inW, outH, outW = [0] * 4
window, canvas, paper = [None] * 3
filename = ""

VIEW_X, VIEW_Y = 512, 512

#################
## 메인 코드부 ##
#################
if __name__ == '__main__':
    window = Tk()
    window.title("컴퓨터 비전 (딥러닝 기법) ver 0.05")
    window.geometry("500x500")
    window.resizable(width=True, height=True)

    # 메뉴 생성
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="파일", menu=fileMenu)
    fileMenu.add_cascade(label="열기", command=openImage)

    status = Label(window, text="이미지 정보 : ", bd=1, relief=SUNKEN, anchor=W)
    status.pack(side=BOTTOM, fill=X)

    btnReverse = Button(window, text = "reverse", command = reverseImage, width = 10)
    btnReverse.pack(side=BOTTOM, pady = 5)
    window.mainloop()
