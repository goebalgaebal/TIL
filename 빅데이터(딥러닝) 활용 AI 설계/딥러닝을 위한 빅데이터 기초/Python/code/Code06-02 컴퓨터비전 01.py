from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path

#################
## 함수 선언부 ##
#################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w) :
    returnMemory = []
    for _ in range(h) :
        tmpList = []
        for _ in range(w) :
            tmpList.append(0)
        returnMemory.append(tmpList)
    return returnMemory

# 파일을 메모리로 로딩하는 함수
def loadImage(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = os.path.getsize(fname) # 파일의 크기 (바이트)
    # math.sqrt()의 결과값은 실수형
    inH = inW = int(math.sqrt(fsize)) # 핵심 코드

    ## 입력영상 메모리 확보 ##
    #inImage.clear()
    #inImage = [] # 새로운 이미지를 불러올 때, 데이터 누적 방지
    inImage = malloc(inH, inW)

    # 파일 → 메모리
    with open(fname, 'rb') as rFp:  # 이진파일을 읽기 모드로 열기
        for i in range(inH) :
            for k in range(inW) :
                inImage[i][k] = int(ord(rFp.read(1))) # 읽어온 파일에서 1byte씩 읽어서(아스키코드) 정수형 데이터로 대입
    print(inH, inW)
    print(inImage[100][100]) # ord() : 문자의 아스키 코드값을 리턴하는 함수

# 파일을 선택해서 메모리로 로딩하는 함수
def openImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw;"), ("모든 파일", "*.*")))
    loadImage(filename)
    equalImage()

def saveImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    pass

def displayImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 이전에 실행한 적이 있는 경우(이전 이미지가 있는 경우)
        canvas.destroy()

    ## 화면 크기 조절 ##
    window.geometry(str(outH) + 'x' + str(outW))
    canvas = Canvas(window, height = outH, width = outW)
    paper = PhotoImage(height = outH, width = outW) # 크기가 정해진 빈 종이
    canvas.create_image((outH // 2, outW // 2), image = paper, state = "normal") # 붙일 위치 = 중앙점, 붙일 이미지

    ## 출력 영상을 화면에 한점씩 찍기 ##
    for i in range(outH) :
        for k in range(outW) :
            r = g = b = outImage[i][k]
            paper.put("#%02x%02x%02x" % (r, g, b), (k, i))  # #RRGGBB
    canvas.pack(expand = 1, anchor = CENTER)

##############################################
## 컴퓨터 비전(영상처리) 알고리즘 함수 모음 ##
##############################################

# 동일 영상 알고리즘
def equalImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = inImage[i][k]

    displayImage()

#####################
## 전역변수 선언부 ##
#####################
inImage, outImage = [], []
inH, inW, outH, outW = [0] * 4
window, canvas, paper = [None] * 3
filename = ""

#################
## 메인 코드부 ##
#################
if __name__ == '__main__':
    window = Tk()
    window.title("컴퓨터 비전 (딥러닝 기법) ver 0.01")
    window.geometry("500x500")
    window.resizable(width=True, height=True)

    # 메뉴 생성
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="파일", menu=fileMenu)
    fileMenu.add_cascade(label="열기", command=openImage)
    fileMenu.add_cascade(label="저장", command=saveImage)

    comvisionMenu1 = Menu(mainMenu)
    mainMenu.add_cascade(label="알고리즘A", menu=comvisionMenu1)
    comvisionMenu1.add_command(label="알고리즘1", command=None)
    comvisionMenu1.add_command(label="알고리즘2", command=None)






    window.mainloop()
