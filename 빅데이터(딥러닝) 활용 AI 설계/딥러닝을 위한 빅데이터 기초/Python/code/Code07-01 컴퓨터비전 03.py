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
    print(inImage[1][1]) # ord() : 문자의 아스키 코드값을 리턴하는 함수

# 파일을 선택해서 메모리로 로딩하는 함수
def openImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw;"), ("모든 파일", "*.*")))
    loadImage(filename)
    equalImage()

import struct
def saveImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent = window, mode = "wb", defaultextension = "*.raw", filetypes=(("RAW 파일", "*.raw;"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None :
        return

    for i in range(outH) :
        for k in range(outW) :
            # 1byte 단위로 저장
            saveFp.write(struct.pack("B", outImage[i][k]))
    saveFp.close()

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
    # for i in range(outH) :
    #     for k in range(outW) :
    #         r = g = b = outImage[i][k]
    #         paper.put("#%02x%02x%02x" % (r, g, b), (k, i))  # #RRGGBB

    ## 영상 출력 성능 개선
    rgbStr = "" # 전체 픽셀의 문자열을 저장
    for i in range(outH) :
        tmpStr = ""
        for k in range(outW) :
            r = g = b = outImage[i][k]
            tmpStr += ' #%02x%02x%02x'  % (r, g, b) # [중요] 앞 한 칸 뛰기
        rgbStr += '{' + tmpStr + '} '# [중요] 뒤 한 칸 뛰기
    paper.put(rgbStr)

    ## 더 성능을 개선시키려면 C++로 비디오 카드 접근 시도해보기

    ## 마우스 이벤트
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)

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

def addImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    value = askinteger("밝게/어둡게 하기", "값을 입력해주세요", minvalue = -255, maxvalue = 255)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] + value
            if outImage[i][k] > 255 : # overflow 처리
                outImage[i][k] = 255
            if outImage[i][k] < 0:  # underflow 처리
                outImage[i][k] = 0
    displayImage()
    print("밝게하기 완료")

def multiplyImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    value = askinteger("영상곱셈", "값을 입력해주세요", minvalue=1)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] * value
            if outImage[i][k] > 255:  # overflow 처리
                outImage[i][k] = 255
    displayImage()
    print("영상곱셈 완료")

def dividingImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    value = askinteger("영상곱셈", "값을 입력해주세요", minvalue=1)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] // value
    displayImage()
    print("영상 나눗셈 완료")

def reverseImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 255 - inImage[i][k]
    displayImage()
    print("화소값 반전 완료")

def binarizationImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] >= 255 // 2 :
                outImage[i][k] = 255
            else :
                outImage[i][k] = 0
    displayImage()
    print("이진화 완료")

def bwImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += inImage[i][k]
    avg = sum // (inH * inW)

    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] >= avg:
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
    displayImage()
    print("이진화(통계) 완료")

def paraImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    LUT = [0 for _ in range(256)] # LookUp Tale 연산량이 줄어듦
    # 0 ~ 255 값의 각 계산을 미리 연산
    for input in range(256) :
        LUT[input] = int(255 - 255 * math.pow(input/128 - 1, 2))
    for i in range(inH):
        for k in range(inW):
            input = inImage[i][k]
            outImage[i][k] = LUT[inImage[i][k]]

    displayImage()
    print("파라볼라 완료")

# 상하반전 알고리즘
def upDownImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    for i in range(inH):
        for k in range(inW):
            outImage[inH - i - 1][k] = inImage[i][k]

    displayImage()

def avgImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    ## 컴퓨터 비전 알고리즘 ##
    inAvg = outAvg = 0
    inSum = outSum = 0
    for i in range(inH):
        for k in range(inW):
            inSum += inImage[i][k]
    inAvg = inSum // (inH * inW)

    for i in range(outH):
        for k in range(outW):
            outSum += outImage[i][k]
    outAvg = outSum // (outH * outW)

    messagebox.showinfo("입/출력 영상 평균값",
                        "입력 영상 평균값 : {0}\n출력 영상 평균값 : {1}".format(inAvg, outAvg))
    print("입/출력 영상 평균값 구하기 완료")

def rotateImage(val = "") :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    # 오른쪽 90도 회전
    if val == "RIGHT" :
        for i in range(inH):
            for k in range(inW):
                outImage[i][k] = inImage[inW - k - 1][i]
        displayImage()
        return
    else :
        messagebox.showinfo("Error", "아직 구현 중")

# def moveImage() :
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#     ## [중요] 출력 영상 크기 결정 ##
#     outH = inH
#     outW = inW
#
#     ## 메모리 할당 ##
#     outImage = []
#     outImage = malloc(outH, outW)
#
#     ## 컴퓨터 비전 알고리즘 ##
#     valVertical = askinteger("상하이동", "값을 입력해주세요\n상(-)\t하(+)", minvalue=-255 , maxvalue = 255)
#     valhorizontal = askinteger("좌우이동", "값을 입력해주세요\n좌(-)\t우(+)", minvalue=-255 , maxvalue = 255)
#
#     for i in range(inH):
#         for k in range(inW):
#             if i + valVertical > outW - 1 or i + valVertical < 0 or k + valhorizontal > outH - 1 or k + valhorizontal < 0:
#                 continue
#             outImage[i + valVertical][k + valhorizontal] = inImage[i][k]
#
#     displayImage()

def resizeImage(func) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    rate = askinteger("축소", "값을 입력해주세요(2, 4, 8)", minvalue=2, maxvalue=8)
    ## [중요] 출력 영상 크기 결정 ##
    if func == 1 : # 축소
        outH = inH // rate
        outW = inW // rate
    else :
        outH = inH * rate
        outW = inW * rate

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    if func == 1 : # 평균을 이용한 서브 샘플링
        for i in range(0, inH, rate) :
            for k in range(0, inW, rate) :
                mask = []
                for x in range(i, i + rate) :
                    for y in range(k, k + rate) :
                        mask.append(inImage[x][y])
                outImage[i // rate][k // rate] = sum(mask) // len(mask)
    else : # 가장 인접한 이웃 화소 보간법으로 영상 확대
        for i in range(outH) :
            for k in range(outW) :
                outImage[i][k] = inImage[i // rate][k // rate]
    displayImage()
    print("리사이즈 완료")

# 화면이동 알고리즘
def moveImage() :
    global penYN
    penYN = True

    canvas.configure(cursor = "mouse")

def mouseClick(event) :
    global sx, sy, ex, ey, penTY
    if penYN == False :
        return
    sx = event.x
    sy = event.y

def mouseDrop(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, penTY
    if penYN == False :
        return
    ex = event.x
    ey = event.y

    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    mx = sx - ex
    my = sy - ey

    for i in range(inH):
        for k in range(inW):
            if 0 <= i - my < outW and 0 <= k - mx < outH :
                outImage[i - my][k - mx] = inImage[i][k]
    penYN == False
    displayImage()


#####################
## 전역변수 선언부 ##
#####################
inImage, outImage = [], []
inH, inW, outH, outW = [0] * 4
window, canvas, paper = [None] * 3
filename = ""
penYN = False
sx, sy, ex, ey = [0] * 4

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
    mainMenu.add_cascade(label="화소점 처리", menu=comvisionMenu1)
    comvisionMenu1.add_command(label="밝게하기", command=addImage)
    comvisionMenu1.add_command(label="어둡게하기", command=addImage)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="영상 곱셈", command=multiplyImage)
    comvisionMenu1.add_command(label="영상 나눗셈", command=dividingImage)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="화소값 반전", command=reverseImage)
    comvisionMenu1.add_command(label="이진화", command=binarizationImage)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="입/출력 영상의 평균값", command=avgImage)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="Posterizing", command=posterizingImage)
    comvisionMenu1.add_command(label="감마보정", command=gammaCorrection)
    comvisionMenu1.add_command(label="명암 대비 스트레칭", command=stretchingImage)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="파라볼라", command=paraImage)

    comvisionMenu2 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소점 처리(통계)", menu=comvisionMenu2)
    comvisionMenu2.add_command(label="이진화", command=bwImage)

    comvisionMenu3 = Menu(mainMenu)

    mainMenu.add_cascade(label="기하학 처리", menu=comvisionMenu3)
    comvisionMenu3.add_command(label="상하반전", command=upDownImage)
    comvisionMenu3.add_command(label="오른쪽 90도 회전", command=lambda : rotateImage("RIGHT"))
    comvisionMenu3.add_separator()
    comvisionMenu3.add_command(label="이동", command = moveImage)
    comvisionMenu3.add_separator()
    comvisionMenu3.add_command(label="축소", command=lambda : resizeImage(1))
    comvisionMenu3.add_command(label="확대", command=lambda : resizeImage(2))
    comvisionMenu3.add_separator()
    comvisionMenu3.add_command(label="회전", command=rotateImage)

    window.mainloop()
