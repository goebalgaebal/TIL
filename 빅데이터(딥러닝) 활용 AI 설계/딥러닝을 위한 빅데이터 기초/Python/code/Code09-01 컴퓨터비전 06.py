from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import pymysql
import datetime
import tempfile

#################
## 함수 선언부 ##
#################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w, initValue = 0) :
    returnMemory = []
    for _ in range(h) :
        tmpList = []
        for _ in range(w) :
            tmpList.append(initValue)
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
    print("입력 크기", inH, inW)
    #print(inImage[1][1]) # ord() : 문자의 아스키 코드값을 리턴하는 함수

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
    global imageFrame, btnFrame, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y
    if canvas != None : # 이전에 실행한 적이 있는 경우(이전 이미지가 있는 경우)
        canvas.destroy()

    ## 고정된 화면 크기
    if inH <= VIEW_Y or inW <= VIEW_X :
        outW = inW
        outH = inH
        step = 1
    else :
        outW = VIEW_X
        outH = VIEW_Y
        step = inW / VIEW_X # 정수로 떨어지지 않는 경우 처리를 위해 실수로 계산
    print("Display Func", "출력 크기", outH, outW)
    window.geometry(str(int(outH * 1.2)) + 'x' + str(int(outW * 1.2)))
    canvas = Canvas(imageFrame, height=outH, width=outW)
    paper = PhotoImage(height=outH, width=outW)
    canvas.create_image((outH // 2, outW // 2), image=paper, state="normal")

    # print(btnFrame.winfo_height(), btnFrame.winfo_width())
    # displayW = btnFrame.winfo_width() if outW < btnFrame.winfo_width() else outW
    # print(str(displayW) + 'x' + str(btnFrame.winfo_height() + outH))
    # print(str(displayW) + 'x' + str(btnFrame.winfo_height() + outH))
    # ## 화면 크기 조절 ##
    # window.geometry(str(displayW) + 'x' + str(btnFrame.winfo_height() + outH))
    # canvas = Canvas(imageFrame, height = outH, width = outW)
    # paper = PhotoImage(height = outH, width = outW) # 크기가 정해진 빈 종이
    # canvas.create_image((outH // 2, outW // 2), image = paper, state = "normal") # 붙일 위치 = 중앙점, 붙일 이미지

    ## 출력 영상을 화면에 한점씩 찍기 ##
    # for i in range(outH) :
    #     for k in range(outW) :
    #         r = g = b = outImage[i][k]
    #         paper.put("#%02x%02x%02x" % (r, g, b), (k, i))  # #RRGGBB

    ## 영상 출력 성능 개선
    import numpy
    rgbStr = "" # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, inH, step) : # numpy의 arange는 실수 step 사용 가능
        tmpStr = ""
        for k in numpy.arange(0, inW, step) :
            i = int(i); k = int(k)
            r = g = b = outImage[i][k]
            tmpStr += ' #%02x%02x%02x'  % (r, g, b) # [중요] 앞 한 칸 뛰기
        rgbStr += '{' + tmpStr + '} '# [중요] 뒤 한 칸 뛰기
    paper.put(rgbStr)


    ## 더 성능을 개선시키려면 C++로 비디오 카드 접근 시도해보기

    ## 마우스 이벤트
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)

    canvas.pack(expand = 1, anchor = CENTER)

    status.configure(text = "이미지 정보 : " + str(outW) + 'x' + str(outH))

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

# 반전영상 알고리즘
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

# 이진화 알고리즘
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

# 파라볼라 알고리즘 with LUT
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

# 영상 회전 알고리즘
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
        angle = askinteger("회전", "각도를 입력해주세요", minvalue = 1, maxvalue = 360)
        radian = angle * math.pi / 180
        for i in range(inH) :
            for k in range(inW) :
                xs = i
                ys = k
                xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
                yd = int(math.sin(radian) * xs + math.cos(radian) * ys)

                if 0 <= xd < inH and 0 <= yd < inW :
                    outImage[xd][yd] = inImage[i][k]
        displayImage()

# 영상 회전 알고리즘 - 중심, 역방향
def rotateImage2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    angle = askinteger("회전", "각도를 입력해주세요", minvalue = 1, maxvalue = 360)
    radian = angle * math.pi / 180
    xc, yc = outW // 2, outH // 2
    for i in range(outH) :
        for k in range(outW) :
            xs = i
            ys = k

            # forward mapping → hole이 생김
            xd = int(xc + math.cos(radian) * (xs - xc) - math.sin(radian) * (ys - yc))
            yd = int(yc + math.sin(radian) * (xs - xc) + math.cos(radian) * (ys - yc))

            # backward mapping

            if 0 <= xd < outH and 0 <= yd < outW :
                outImage[xs][ys] = inImage[xd][yd]
            else :
                outImage[xs][ys] = 255
    displayImage()

def zoomOutImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    scale = askinteger("축소", "배율을 입력해주세요", minvalue=2, maxvalue=8)

    ## [중요] 출력 영상 크기 결정 ##
    outH = inH // scale
    outW = inW // scale

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    ## forward 방식
    # for i in range(inH):
    #     for k in range(inW):
    #         outImage[i // scale][k // scale] = inImage[i][k]

    ## backward 방식 - 속도 개선
    for i in range(outH):
        for k in range(outW):
             outImage[i][k] = inImage[i * scale][k * scale]
    displayImage()

# 영상 축소 알고리즘 (평균변환)
def zoomOutImage2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    scale = askinteger("축소", "배율을 입력해주세요", minvalue=2, maxvalue=8)

    ## [중요] 출력 영상 크기 결정 ##
    outH = inH // scale
    outW = inW // scale

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            outImage[i // scale][k // scale] += inImage[i][k]

    for i in range(outH) :
        for k in range(outW) :
            outImage[i][k] //= (scale * scale)
    displayImage()

# 영상 확대 알고리즘
def zoomInImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    scale = askinteger("축소", "배율을 입력해주세요", minvalue=2, maxvalue=4)

    ## [중요] 출력 영상 크기 결정 ##
    outH = inH * scale
    outW = inW * scale

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    ## forward
    # for i in range(inH):
    #     for k in range(inW):
    #         outImage[i * scale][k * scale] = inImage[i][k]

    ## backward
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i // scale][k // scale]
    displayImage()

# 영상 확대 알고리즘 (양선형보간)
def zoomInImage2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    scale = askinteger("축소", "배율을 입력해주세요", minvalue=2, maxvalue=4)

    ## [중요] 출력 영상 크기 결정 ##
    outH = inH * scale
    outW = inW * scale

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    rH, rW, iH, iW = [0] * 4 # 실수 위치 및 정수 위치
    x, y = 0, 0 # 실수와 정수의 차이값 = 가중치
    C1, C2, C3, C4 = [0] * 4 # 결정할 위치(N)의 상하좌우 픽셀
    for i in range(outH):
        for k in range(outW):
            rH = i / scale; rW = k / scale
            iH = int(rH);   iW = int(rW)
            x = rW - iW;    y = rH - iH
            if 0 <= iH < inH - 1 and 0 <= iW < inW - 1:
                C1 = inImage[iH][iW]
                C2 = inImage[iH][iW + 1]
                C3 = inImage[iH + 1][iW + 1]
                C4 = inImage[iH + 1][iW]
                newValue = C1 * (1 - y) * (1 - x) + C2 * (1 - y) * x + C3 * y * x + C4 * y * (1 - x)
                outImage[i][k] = int(newValue)

    displayImage()

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

# 히스토그램
import matplotlib.pyplot as plt
def histoImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    inCountList = [0] * 256
    outCountList = [0] * 256

    for i in range(inH) :
        for k in range(inW) :
            inCountList[inImage[i][k]] += 1

    for i in range(outH) :
        for k in range(outW) :
            outCountList[outImage[i][k]] += 1

    plt.plot(inCountList)
    plt.plot(outCountList)
    plt.show()

def histoImage2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outCountList = [0] * 256
    normalCountList = [0] * 256

    # 빈도수 계산
    for i in range(inH) :
        for k in range(inW) :
            outCountList[inImage[i][k]] += 1

    maxVal = max(outCountList)
    minVal = min(outCountList)
    High = 256
    # 정규화 = (카운트값 - 최소값) * High / (최대값 - 최소값)
    for i in range(len(outCountList)) :
        normalCountList[i] = (outCountList[i] - minVal) * High / (maxVal - minVal)

    ## 서브 윈도우창 생성 후 출력
    subWindow = Toplevel(window) # window 창의 아래 level에 있다
    subWindow.geometry("256x256")
    subCanvas = Canvas(subWindow, width = 256, height = 256)
    subPaper = PhotoImage(width = 256, height = 256)
    subCanvas.create_image((256 // 2, 256//2), image = subPaper, state = "normal")

    for i in range(len(normalCountList)) :
        for k in range(int(normalCountList[i])) :
            data = 0
            subPaper.put("#%02x%02x%02x" % (data, data, data), (i, 255 - k)) # 회전 고려
    subCanvas.pack(expand = 1, anchor = CENTER)
    subWindow.mainloop()

# 스트레칭 알고리즘
def stretchImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    maxVal = inImage[0][0] # 유지되도 관계없는 값을 넣는다
    minVal = inImage[0][0]
    for i in range(inH) :
        for k in range(inW) :
            if inImage[i][k] < minVal :
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal :
                maxVal = inImage[i][k]

    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = int(((inImage[i][k] - minVal) / (maxVal - minVal)) * 255)

    displayImage()

# 앤드-인 탐색 알고리즘
def endInStretchImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    maxVal = inImage[0][0] # 유지되도 관계없는 값을 넣는다
    minVal = inImage[0][0]
    for i in range(inH) :
        for k in range(inW) :
            if inImage[i][k] < minVal :
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal :
                maxVal = inImage[i][k]

    minAdd = askinteger("최소", "최소 추가", minvalue = 0, maxvalue = 255)
    maxMinus = askinteger("최대", "최소 감소", minvalue=0, maxvalue=255)
    minVal += minAdd
    maxVal -= maxMinus

    for i in range(inH) :
        for k in range(inW) :
            value = int(((inImage[i][k] - minVal) / (maxVal - minVal)) * 255)
            if value < 0 :
                value = 0
            elif value > 255 :
                value = 255
            outImage[i][k] = value
    displayImage()

# 히스토그램 평활화 알고리즘
def histoEqualizedImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    ## 1. 히스토그램 생성
    histo = [0] * 256;  sumHisto = [0] * 256;   normalHisto = [0] * 256
    for i in range(inH):
        for k in range(inW):
            histo[inImage[i][k]] += 1

    ## 2. 누적 빈도 수 계산
    sValue = 0
    for i in range(len(histo)) :
        sValue += histo[i]
        sumHisto[i] = sValue

    ## 3. 누적 빈도수 정규화
    normalHisto = list(map(lambda x : int(x / (inW * inH) * 255) , sumHisto))

    ## 영상처리
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = normalHisto[inImage[i][k]]

    displayImage()

# 마스크를 활용한 알고리즘
def maskImage(mask, retouch = False) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    MSIZE = len(mask)

    ## 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127)  # 중간값을 넘겨주는 것이 좋다
    tmpOutImage = malloc(outH, outW)

    ## 원 입력 → 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + MSIZE // 2][k + MSIZE // 2] = inImage[i][k]

    ## 회선 연산
    for i in range(MSIZE // 2, inH + MSIZE // 2):
        for k in range(MSIZE // 2, inW + MSIZE // 2):
            # 각 점 처리
            S = 0.0
            for m in range(MSIZE):
                for n in range(MSIZE):
                    S += mask[m][n] * tmpInImage[i + m - MSIZE // 2][k + n - MSIZE // 2]
            tmpOutImage[i - MSIZE // 2][k - MSIZE // 2] = S

    if retouch == True :
        ## 127 더하기
        # 마스크의 합 = 0인 마스크 → 가중치 0, 일반적으로 어두워짐, 마스크의 합 = 1인 마스크 존재
        for i in range(outH):
            for k in range(outW):
                tmpOutImage[i][k] += 127

    ## 임시 출력 → 원 출력 영상
    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = int(value)

    displayImage()
    print("마스크 처리 완료")

# 유사 연산자 에지 검출 알고리즘
def homogenOpImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    MSIZE = 3

    ## 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127)  # 중간값을 넘겨주는 것이 좋다
    tmpOutImage = malloc(outH, outW)

    ## 원 입력 → 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + MSIZE // 2][k + MSIZE // 2] = inImage[i][k]

    ## 회선 연산
    for i in range(MSIZE // 2, inH + MSIZE // 2):
        for k in range(MSIZE // 2, inW + MSIZE // 2):
            # 각 점 처리
            np = []
            for m in range(MSIZE):
                for n in range(MSIZE):
                    np.append(abs(tmpInImage[i][k] - tmpInImage[i + m - MSIZE // 2][k + n - MSIZE // 2]))
            tmpOutImage[i - MSIZE // 2][k - MSIZE // 2] = max(np)

    ## 임시 출력 → 원 출력 영상
    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = int(value)

    displayImage()
    print("단순 경계선 검출 완료")

# 1차 미분 회선 알고리즘
def firstOrderDiff(mask) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    MSIZE = 3

    if mask == "roberts" : # 로버츠 에지 검출 마스크
        maskRow = [[-1, 0, 0],
                   [ 0, 1, 0],
                   [ 0, 0, 0]]
        maskCol = [[0, 0, -1],
                   [0, 1,  0],
                   [0, 0,  0]]

    elif mask == "prewitt" : # 프리윗 에지 검출 마스크
        maskRow = [[-1, -1, -1],
                   [ 0,  0,  0],
                   [ 1,  1,  1]]
        maskCol = [[1, 0, -1],
                   [1, 0, -1],
                   [1, 0, -1]]
    else : # 소벨 에지 검출 마스크
        maskRow = [[-1, -2, -1],
                   [0, 0, 0],
                   [1, 2, 1]]
        maskCol = [[1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1]]

    ## 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127)  # 중간값을 넘겨주는 것이 좋다
    tmpOutImage = malloc(outH, outW)

    ## 원 입력 → 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + MSIZE // 2][k + MSIZE // 2] = inImage[i][k]

    ## 회선 연산
    for i in range(MSIZE // 2, inH + MSIZE // 2):
        for k in range(MSIZE // 2, inW + MSIZE // 2):
            # 각 점 처리
            valRow, valCol = 0.0, 0.0
            for m in range(MSIZE):
                for n in range(MSIZE):
                    valRow += maskRow[m][n] * tmpInImage[i + m - MSIZE // 2][k + n - MSIZE // 2]
                    valCol += maskCol[m][n] * tmpInImage[i + m - MSIZE // 2][k + n - MSIZE // 2]
            tmpOutImage[i - MSIZE // 2][k - MSIZE // 2] = math.sqrt(valRow * valRow + valCol * valCol)

    ## 임시 출력 → 원 출력 영상
    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = int(value)

    displayImage()
    print("1차 미분 회선 에지 검출 처리 완료")

# 라플라시안 에지 검출 알고리즘
def secondOrderDiff() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    MSIZE = 3
    mask = [[0, -1,  0],
            [-1, 4, -1],
            [0, -1,  0]]

    ## 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127)  # 중간값을 넘겨주는 것이 좋다
    tmpOutImage = malloc(outH, outW)

    ## 원 입력 → 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + MSIZE // 2][k + MSIZE // 2] = inImage[i][k]

    ## 회선 연산
    for i in range(MSIZE // 2, inH + MSIZE // 2):
        for k in range(MSIZE // 2, inW + MSIZE // 2):
            # 각 점 처리
            S = 0.0
            for m in range(MSIZE):
                for n in range(MSIZE):
                    S += mask[m][n] * tmpInImage[i + m - MSIZE // 2][k + n - MSIZE // 2]
            tmpOutImage[i - MSIZE // 2][k - MSIZE // 2] = S

    ## 임시 출력 → 원 출력 영상
    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = int(value)

    displayImage()
    print("라플라시안 완료")

# 모핑 알고리즘
def morphImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## [중요] 출력 영상 크기 결정 ##
    outH = inH
    outW = inW
    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw;"), ("모든 파일", "*.*")))

    if filename2 == "" or filename2 == None :
        return
    fsize = os.path.getsize(filename2)  # 파일의 크기 (바이트)
    inH2 = inW2 = int(math.sqrt(fsize))  # 핵심 코드

    ## 입력영상 메모리 확보 ##
    inImage2 = malloc(inH2, inW2)

    # 파일 → 메모리
    with open(filename2, 'rb') as rFp:  # 이진파일을 읽기 모드로 열기
        for i in range(inH2):
            for k in range(inW2):
                inImage2[i][k] = int(ord(rFp.read(1)))

    ## 메모리 할당 ##
    outImage = []
    outImage = malloc(outH, outW)

    ## 컴퓨터 비전 알고리즘 ##
    # w1 = askinteger("원영상 가중치", "가중치 값(%)을 입력해주세요", minvalue=0, maxvalue=100)
    # w2 = 1 - (w1 / 100)
    # w1 = 1 - w2
    # for i in range(inH):
    #     for k in range(inW):
    #         newValue = int(inImage[i][k] * w1 + inImage2[i][k] * w2)
    #         if newValue > 255:  # overflow 처리
    #             newValue = 255
    #         if newValue < 0:  # underflow 처리
    #             newValue = 0
    #         outImage[i][k] = newValue
    # displayImage()

    import threading
    import time
    def morpFunc():
        w1 = 1;
        w2 = 0
        for _ in range(20):
            for i in range(inH):
                for k in range(inW):
                    newValue = int(inImage[i][k] * w1 + inImage2[i][k] * w2)
                    if newValue > 255:
                        newValue = 255
                    elif newValue < 0:
                        newValue = 0
                    outImage[i][k] = newValue
            displayImage()
            w1 -= 0.05;
            w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()
    print("모핑 완료")

###################
## MySQL DB 연동 ##
###################
def selectFile() :
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw;"), ("모든 파일", "*.*")))

    if filename == "" or filename == None :
        return
    edt1.delete(0, "end")
    edt1.insert(0, str(filename))

def selectFolder() :
    dirName = askdirectory()
    if dirName == "" or dirName == None :
        return
    edt1.delete(0, "end")
    edt1.insert(0, str(dirName))
    print("선택된 경로", dirName)

# 경로를 받아서 INSERT SQL 작성 함수
def createSql(dirName) :
    with open(dirName, "rb") as rfp :
        fsize = os.path.getsize(dirName)  # 파일의 크기 (바이트)
        binData = rfp.read()
        binList = [binData[byte] for byte in range(fsize)]

    # 평균, 최대값, 최소값
    avgVal = sum(binList) // fsize
    maxVal = max(binList)
    minVal = min(binList)

    fname = os.path.basename(dirName)
    height = width = int(math.sqrt(fsize))
    upDate = datetime.datetime.now().strftime("%y-%m-%d")
    upUser = USER_NAME

    sql = "INSERT INTO rawIMAGE_TBL(raw_id, raw_height, raw_width, raw_fname, " \
          "raw_avg, raw_max, raw_min, " \
          "raw_update, raw_uploader, raw_data) " \
          "VALUES(NULL, " + str(height) + ", " + str(width) + ", '" + fname + "'," + \
          str(avgVal) + ", " + str(maxVal) + ", " + str(minVal) + ", '" + upDate + "', '" + upUser + "', %s )"
    return sql, binData

def uploadData() :
    con = pymysql.connect(host = IP_ADDR, user = USER_NAME, password = USER_PASS,
                          db = DB_NAME, charset = CHAR_SET)
    cur = con.cursor()

    fullname = edt1.get()
    if os.path.isfile(fullname) : # 파일을 선택한 경우
        sql, binData = createSql(fullname)
        print(sql)
        tupleData = (binData, )
        cur.execute(sql, tupleData)
    else : # 폴더를 선택한 경우
        try :
            fileList = os.listdir(fullname)
        except :
            messagebox.showinfo("Error", "잘못된 경로를 입력하셨습니다")
            return

        for file in fileList :
            sql, binData = createSql(fullname + "\\" + file)
            print(sql)
            tupleData = (binData,)
            cur.execute(sql, tupleData)

    con.commit()
    cur.close()
    con.close()
    print("Upload Complete")

def downloadData() :
    con = pymysql.connect(host = IP_ADDR, user = USER_NAME, password = USER_PASS,
                          db = DB_NAME, charset = CHAR_SET)
    cur = con.cursor()
    sql = "SELECT raw_fname, raw_data FROM rawImage_TBL WHERE raw_id = 1"
    cur.execute(sql)
    fname, binData = cur.fetchone()

    fullpath = tempfile.gettempdir() + "/" + fname
    with open(fullpath, "wb") as wfp :
        wfp.write(binData)
    print("경로", fullpath)

    con.commit()
    cur.close()
    con.close()
    print("Download Complete")

#####################
## 전역변수 선언부 ##
#####################
inImage, outImage = [], []
inH, inW, outH, outW = [0] * 4
window, canvas, paper = [None] * 3
filename = ""
penYN = False
sx, sy, ex, ey = [0] * 4

VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)

btnFrame, imageFrame = None, None

IP_ADDR = "192.168.56.108"
USER_NAME = "root"
USER_PASS = "1234"
DB_NAME = "BigData_DB"
CHAR_SET = "utf8"

# algorithm mask
emboss = [[-1, 0, 0],
        [0, 0, 0],
        [0, 0, 1]]

BMSIZE = 5
blurr = [[1 / (BMSIZE * BMSIZE) for i in range(BMSIZE)] for k in range(BMSIZE)]

sharpening = [[0, -1, 0],
              [-1, 5, -1],
              [0, -1, 0]]

gaussian = [[1 / 16, 1 / 8, 1 / 16],
            [1 / 8, 1 / 4, 1 / 8],
            [1 / 16, 1 / 8, 1 / 16]]

# 고주파
hpf = [[-1/9, -1/9, -1/9],
       [-1/9,  8/9, -1/9],
       [-1/9, -1/9, -1/9]]

# 저주파
lpf = [[1 / 9, 1 / 9, 1 / 9],
       [1 / 9, 1 / 9, 1 / 9],
       [1 / 9, 1 / 9, 1 / 9]]

#################
## 메인 코드부 ##
#################
if __name__ == '__main__':
    window = Tk()
    window.title("컴퓨터 비전 (딥러닝 기법) ver 0.03")
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
    comvisionMenu1.add_command(label="파라볼라", command=paraImage)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="모핑", command=morphImage)

    comvisionMenu2 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소점 처리(통계)", menu=comvisionMenu2)
    comvisionMenu2.add_command(label="이진화", command=bwImage)
    comvisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImage2)
    comvisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImage2)
    comvisionMenu2.add_separator()
    comvisionMenu2.add_command(label = "히스토그램", command = histoImage)
    comvisionMenu2.add_command(label="히스토그램2", command=histoImage2)
    comvisionMenu2.add_separator()
    comvisionMenu2.add_command(label="명암대비", command=stretchImage)
    comvisionMenu2.add_command(label="End-In 탐색", command=endInStretchImage)
    comvisionMenu2.add_command(label="히스토그램 평활화", command=histoEqualizedImage)

    comvisionMenu3 = Menu(mainMenu)
    mainMenu.add_cascade(label="기하학 처리", menu=comvisionMenu3)
    comvisionMenu3.add_command(label="상하반전", command=upDownImage)
    comvisionMenu3.add_command(label="오른쪽 90도 회전", command=lambda : rotateImage("RIGHT"))
    comvisionMenu3.add_separator()
    comvisionMenu3.add_command(label="이동", command = moveImage)
    comvisionMenu3.add_separator()
    comvisionMenu3.add_command(label="축소", command=zoomOutImage)
    comvisionMenu3.add_command(label="확대", command=zoomInImage)
    comvisionMenu3.add_separator()
    comvisionMenu3.add_command(label="회전", command=rotateImage)
    comvisionMenu3.add_command(label="회전2(중심, 역방향)", command=rotateImage2)

    comvisionMenu4 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소영역 처리", menu=comvisionMenu4)
    comvisionMenu4.add_command(label="엠보싱", command = lambda : maskImage(emboss, True))
    comvisionMenu4.add_command(label="블러링", command = lambda : maskImage(blurr))
    comvisionMenu4.add_command(label="샤프닝", command = lambda : maskImage(sharpening))
    comvisionMenu4.add_command(label="가우시안 필터링", command = lambda : maskImage(gaussian))
    comvisionMenu4.add_command(label="고주파", command = lambda : maskImage(hpf, True))
    comvisionMenu4.add_command(label="저주파", command = lambda : maskImage(lpf))
    comvisionMenu4.add_separator()
    comvisionMenu4.add_command(label="단순 경계선 검출", command=homogenOpImage)
    comvisionMenu4.add_command(label="로버츠", command=lambda : firstOrderDiff("roberts"))
    comvisionMenu4.add_command(label="프리윗", command=lambda: firstOrderDiff("prewitt"))
    comvisionMenu4.add_command(label="소벨", command=lambda: firstOrderDiff("sobel"))
    comvisionMenu4.add_command(label="라플라시안", command=secondOrderDiff)

    btnFrame = tkinter.Frame(window)
    btnFrame.pack()

    edt1 = Entry(btnFrame, width=20)
    edt1.pack(side = "left")

    btnFile = Button(btnFrame, text="파일 탐색", command=selectFile)
    btnFile.pack(side = "left")

    btnFolder = Button(btnFrame, text="폴더 탐색", command=selectFolder)
    btnFolder.pack(side="left")

    btnUpload = Button(btnFrame, text="업로드", command=uploadData)
    btnUpload.pack(side = "left")

    btnDownload = Button(btnFrame, text="다운로드", command=downloadData)
    btnDownload.pack(side = "left")

    imageFrame = tkinter.Frame(window)
    imageFrame.pack()

    status = Label(window, text = "이미지 정보 : ", bd = 1, relief = SUNKEN, anchor = W)  # 밑에 고정
    status.pack(side = BOTTOM, fill = X)

    window.mainloop()
