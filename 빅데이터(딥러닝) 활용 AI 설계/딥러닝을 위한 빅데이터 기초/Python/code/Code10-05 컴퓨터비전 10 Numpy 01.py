from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import pymysql
import datetime
import tempfile
import random
import struct # saveImage()
import numpy as np
import time # 성능 비교

#################
## 함수 선언부 ##
#################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w, initValue = 0, dataType = "uint8") :
    returnMemory = []
    returnMemory = np.zeros((h, w), dtype = dataType)
    returnMemory += initValue
    return returnMemory

# 파일을 메모리로 로딩하는 함수
def loadImage(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = os.path.getsize(fname)
    inH = inW = int(math.sqrt(fsize))

    inImage = np.fromfile(fname, dtype = "uint8")
    inImage = inImage.reshape([inH, inW])

    print("LOAD 입력 크기", inH, inW)

# 파일을 선택해서 메모리로 로딩하는 함수
def openImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw;"), ("모든 파일", "*.*")))
    # start = time.time()
    loadImage(filename)
    equalImage()
    # print("OPEN IMAGE", time.time() - start)

def saveImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent = window, mode = "wb", defaultextension = "*.raw",
                           filetypes=(("RAW 파일", "*.raw;"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None :
        return

    for i in range(outH) :
        for k in range(outW) :
            # 1byte 단위로 저장
            saveFp.write(struct.pack("B", outImage[i][k]))
    saveFp.close()

def displayImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y
    if canvas != None:  # 이전에 실행한 적이 있는 경우(이전 이미지가 있는 경우)
        canvas.destroy()

    ## 고정된 화면 크기
    if outH <= VIEW_Y or outW <= VIEW_X:
        VIEW_X = outW
        VIEW_Y = outH
        step = 1

    else:
        VIEW_X = 512
        VIEW_Y = 512
        step = outW / VIEW_X  # 정수로 떨어지지 않는 경우 처리를 위해 실수로 계산

    print(btnFrame.winfo_width(), VIEW_X, VIEW_Y)
    if outW < btnFrame.winfo_width() : # 버튼 프레임보다 이미지가 작은 경우
        window.geometry(str(int(btnFrame.winfo_width() * 1.2)) + 'x' + str(int((btnFrame.winfo_height() + VIEW_Y) * 1.2)))  # 벽
    else :
        window.geometry(str(int(VIEW_X * 1.2)) + 'x' + str(int(VIEW_Y * 1.2)))
    canvas = Canvas(imageFrame, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    ## 화면 크기를 조절
    # window.geometry(str(outH) + 'x' + str(outW)) # 벽
    # canvas = Canvas(window, height=outH, width=outW) # 보드
    # paper = PhotoImage(height=outH, width=outW) # 빈 종이
    # canvas.create_image((outH//2, outW//2), image=paper, state='normal')
    # ## 출력영상 --> 화면에 한점씩 찍자.
    # for i in range(outH) :
    #     for k in range(outW) :
    #         r = g = b = outImage[i][k]
    #         paper.put("#%02x%02x%02x" % (r, g, b), (k, i))
    ## 영상 출력 성능 개선
    import numpy
    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, step):
        tmpStr = ''
        for k in numpy.arange(0, outW, step):
            i = int(i);
            k = int(k)
            r = g = b = int(outImage[i][k])
            tmpStr += ' #%02x%02x%02x' % (r, g, b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    ## 마우스 이벤트
    canvas.bind('<Button-1>', mouseClick)
    canvas.bind('<ButtonRelease-1>', mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)

    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

##############################################
## 컴퓨터 비전(영상처리) 알고리즘 함수 모음 ##
##############################################

# 동일 영상 알고리즘
def equalImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    # outImage = inImage.copy()
    outImage = inImage[:]
    displayImage()

def addImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    value = askinteger("밝게/어둡게 하기", "값을 입력해주세요", minvalue = -255, maxvalue = 255)
    inImage = inImage.astype(np.int16) # uint8은 255가 최대값이라 error가 날 수 있으므로 np.int16으로 변환 후 계산
    outImage = inImage + value

    # start = time.time()
    outImage = np.where(outImage > 255, 255, outImage)
    outImage = np.where(outImage < 0, 0, outImage)
    # iter = np.nditer(outImage, flags=["multi_index"], op_flags=["readwrite"])
    # while not iter.finished :
    #     idx = iter.multi_index
    #     if outImage[idx] > 255 :
    #         outImage[idx] = 255
    #     elif outImage[idx] < 0 :
    #         outImage[idx] = 0
    #     iter.iternext()
    # seconds = time.time() - start
    displayImage()
    # status.configure(text = status.cget("text") + "\t소요시간 {0:.2f}".format(seconds))
    # print("ADD IMAGE", seconds)
    print("밝게하기 완료")

def multiplyImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    value = askinteger("영상곱셈", "값을 입력해주세요", minvalue=1)
    outImage = inImage * value
    outImage = np.where(outImage > 255, 255, outImage)
    outImage = np.where(outImage < 0, 0, outImage)

    displayImage()
    print("영상곱셈 완료")

def dividingImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW
    outImage = malloc(outH, outW)

    value = askinteger("영상곱셈", "값을 입력해주세요", minvalue=1)
    outImage = inImage // value
    displayImage()
    print("영상 나눗셈 완료")

# 반전영상 알고리즘
def reverseImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    outImage = 255 - inImage
    displayImage()
    print("화소값 반전 완료")

# 이진화 알고리즘
def binarizationImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    outImage = np.where(inImage >= (255 // 2), 255, 0)
    displayImage()
    print("이진화 완료")

def bwImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    outImage = np.where(inImage >= inImage.mean(), 255, 0)
    displayImage()
    print("이진화(통계) 완료")

# 파라볼라 알고리즘 with LUT
def paraImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    x = np.array([i for i in range(0, 256)])
    LUT = 255 - 255 * np.power(x / 128 - 1, 2)
    outImage = np.array(LUT)[inImage]
    displayImage()
    print("파라볼라 완료")

# 상하반전 알고리즘
def upDownImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    outImage = np.flip(inImage)
    # outImage = inImage[::-1, :]
    displayImage()

def avgImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    messagebox.showinfo("입/출력 영상 평균값",
                        "입력 영상 평균값 : {0}\n출력 영상 평균값 : {1}".format(int(inImage.mean()),
                                                                  int(outImage.mean())))
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
    for i in range(outH):
        for k in range(outW):
            xs = i
            ys = k

            # forward mapping → hole이 생김
            xd = int(xc + math.cos(radian) * (xs - xc) - math.sin(radian) * (ys - yc))
            yd = int(yc + math.sin(radian) * (xs - xc) + math.cos(radian) * (ys - yc))

            # backward mapping
            if 0 <= xd < outH and 0 <= yd < outW:
                outImage[xs][ys] = inImage[xd][yd]
            else:
                outImage[xs][ys] = 255
    displayImage()

def zoomOutImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    scale = askinteger("축소", "배율을 입력해주세요", minvalue=2, maxvalue=8)
    outH = inH // scale;    outW = inW // scale

    outImage = inImage[:]
    outImage = inImage[::scale, ::scale]
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
    outH = inH * scale; outW = inW * scale

    outImage = [];  outImage = malloc(outH, outW)
    print("ZOOMIN", outH, outW)
    outImage = np.kron(inImage, np.ones((scale, scale)))
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

    outH = inH; outW = inW
    outImage = malloc(outH, outW)

    mx = sx - ex;   my = sy - ey
    if mx < 0 and my < 0 :
        outImage[-mx:inH, -my:inW] = inImage[0:inH+mx, 0:inW+my]
    elif mx > 0 and my >= 0 :
        outImage[0:inH-mx, 0:inW-my] = inImage[mx:inH, my:inW]
    elif mx < 0 and my >= 0 :
        outImage[0:inH-mx, -my:inW] = inImage[mx:inH, 0:inW+my]
    elif mx >= 0 and my < 0:
        outImage[-mx:inH, 0:inW-my] = inImage[0:inH+mx, my:inW]

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

## 임시 경로에 outImage를 저장
def saveTempImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    import tempfile
    saveFp = tempfile.gettempdir() + "/" + str(random.randint(10000, 99999)) + ".raw"
    if saveFp == '' or saveFp == None :
        return
    print(saveFp)
    saveFp = open(saveFp, mode='wb')
    for i in range(outH) :
        for k in range(outW) :
            saveFp.write(struct.pack('B', outImage[i][k]))
    saveFp.close()
    return saveFp

def findStat(fname) :
    # 파일 열고 읽기
    fsize = os.path.getsize(fname)
    inH = inW = int(math.sqrt(fsize))

    inImage = malloc(inH, inW)

    # 파일 → 메모리
    with open(fname, 'rb') as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1)))

    sum = 0
    for i in range(inH) :
        for k in range(inW) :
            sum += inImage[i][k]
    avg = sum // (inH * inW)

    maxVal = inImage[0][0]
    minVal = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]

    return avg, maxVal, minVal

def saveMysql() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    try:
        sql = '''
                CREATE TABLE rawImage_TBL (
                raw_id INT AUTO_INCREMENT PRIMARY KEY,
                raw_fname VARCHAR(30),
                raw_extname CHAR(5),
                raw_height SMALLINT, raw_width SMALLINT,
                raw_avg TINYINT UNSIGNED, 
                raw_max TINYINT UNSIGNED,
                raw_min TINYINT UNSIGNED)
            '''
        cur.execute()
    except:  # 이미 TABLE이 존재하는 경우
        pass

    ## outImage를 임시 폴더에 저장하고, 이걸 fullname으로 전달
    fullname = saveTempImage()
    fullname = fullname.name
    with open(fullname, 'rb') as rfp:
        binData = rfp.read()

    fname, extname = os.path.basename(fullname).split(".")
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))

    avgVal, maxVal, minVal = findStat(fullname)  # 평균, 최대, 최소

    sql = "INSERT INTO rawImage_TBL(raw_id, raw_fname, raw_extname, raw_height, raw_width, "
    sql += "raw_avg, raw_max, raw_min, raw_data) "
    sql += "VALUES(NULL, '" + fname + "', '" + extname + "', " + str(height) + ", " + str(width) + ", "
    sql += str(avgVal) + ", " + str(maxVal) + ", " + str(minVal) + " , %s )"

    tupleData = (binData,)
    cur.execute(sql, tupleData)

    con.commit()
    cur.close()
    con.close()

    os.remove(fullname)
    print("Upload Complete")

def loadMysql() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    sql = "SELECT raw_id, raw_fname, raw_extname, raw_height, raw_width "
    sql += "FROM rawImage_TBL"
    cur.execute(sql)

    queryList = cur.fetchall()
    rowList = [':'.join(map(str, row)) for row in queryList]

    def selectRecord() :
        global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
        selIndex = listbox.curselection()[0] # 선택한 것 중 첫번째
        subWindow.destroy()
        raw_id = queryList[selIndex][0]

        sql = "SELECT raw_fname, raw_extname, raw_data FROM rawImage_TBL "
        sql += "WHERE raw_id = " + str(raw_id)

        cur.execute(sql)
        fname, extname, binData = cur.fetchone()

        fullpath = tempfile.gettempdir() + "/" + fname + "." + extname
        with open(fullpath, "wb") as wfp:
            wfp.write(binData)
        print("경로", fullpath, "에 저장")

        loadImage(fullpath)
        equalImage()

        con.commit()
        cur.close()
        con.close()


    ### 서브 윈도우창에 목록 출력하기
    subWindow = Toplevel(window)  # window 창의 아래 level에 있다
    listbox = Listbox(subWindow)
    btn = Button(subWindow, text = "선택", command = selectRecord)

    for rowStr in rowList :
        listbox.insert(END, rowStr)

    listbox.pack(expand=1, anchor=CENTER)
    btn.pack()
    subWindow.mainloop()

    cur.close()
    con.close()

##########################
## CSV 데이터 관련 함수 ##
##########################
def loadCSV(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = 0
    fp = open(fname, "r")
    for _ in fp :
        fsize += 1
    inH = inW = int(math.sqrt(fsize))
    fp.close()

    ## 입력영상 메모리 확보 ##
    inImage = []
    inImage = malloc(inH, inW)

    # 파일 → 메모리
    with open(fname, "r") as rFp:
        for row_list in rFp :
            row, col, value = list(map(int, row_list.strip().split(",")))
            inImage[row][col] = value

def openCSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                               filetypes=(("CSV 파일", "*.csv;"), ("모든 파일", "*.*")))
    loadCSV(filename)
    equalImage()

import csv
def saveCSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent = window, mode = "wb",
                           defaultextension = "*.csv",
                           filetypes=(("CSV 파일", "*.csv;"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None :
        return

    with open(saveFp.name, "w", newline="") as wFp:
        csvWriter = csv.writer(wFp)
        for i in range(outH) :
            for k in range(outW) :
                row_list = [i, k, outImage[i][k]]
                csvWriter.writerow(row_list)
    print("CSV save OK")

############################
## EXCEL 데이터 관련 함수 ##
############################
import xlrd
def openExcel() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=None, filetypes=(("엑셀 파일", "*.xls;*.xlsx"),
                                                       ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return

    # 헤더는 존재하지 않는다고 가정
    # sheet는 1개라고 가정
    workbook = xlrd.open_workbook(filename)
    ws = workbook.sheets()[0]
    print("LOAD Sheet",ws.name)

    inH, inW = ws.nrows, ws.ncols
    inImage = malloc(inH, inW)

    for i in range(inH) :
        for k in range(inW) :
            inImage[i][k] = int(ws.cell_value(i, k))
    equalImage()

import xlwt
def saveExcel():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode="wb",
                           defaultextension="*.xls",
                           filetypes=(("XLS 파일", "*.xls;"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return

    xlsName = saveFp.name
    sheetName = os.path.basename(filename)# sheet하나에 데이터가 들어있다고 가정

    wb = xlwt.Workbook() # 파일 자체 준비
    ws = wb.add_sheet(sheetName) # sheet 생성
    for i in range(outH) :
        for k in range(outW) :
            ws.write(i, k, outImage[i][k])
    wb.save(xlsName) # xlsName으로 파일 저장
    print("Excel save OK")

import xlsxwriter
def saveExcelArt():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode="wb",
                           defaultextension="*.xls",
                           filetypes=(("XLS 파일", "*.xls;"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return

    xlsName = saveFp.name
    sheetName = os.path.basename(filename)# sheet하나에 데이터가 들어있다고 가정

    wb = xlsxwriter.Workbook(xlsName) # xlsName의 파일 자체 준비
    ws = wb.add_worksheet(sheetName) # sheet 생성

    ws.set_column(0, outW -1, 1.0) # 0부터 outW-1까지 약 0.34
    for i in range(outH) :
        ws.set_row(i, 9.5) # i번재 행을 약 0.35

    for i in range(outH) :
        for k in range(outW) :
            data = outImage[i][k]
            # data 값으로 셀의 배경색을 조절 #000000 ~ #FFFFFF
            if data > 15 :
                hexStr = "#" + hex(data)[2:] * 3 # ox를 떼고 RGB값을 같은 값으로 넣어준다
            else :
                hexStr = "#" + ("0" + hex(data)[2:]) * 3

            # 셀의 포맷 준비
            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)

            ws.write(i, k, "", cell_format) # ""자리를 실제 들어가는 값
    wb.close() # 파일 저장
    print("Excel save OK")

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

IP_ADDR = "192.168.56.109"
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
    window.title("컴퓨터 비전 (딥러닝 기법) ver 0.05")
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
    comvisionMenu4.add_command(label="엠보싱", command=lambda: maskImage(emboss, True))
    comvisionMenu4.add_command(label="블러링", command=lambda: maskImage(blurr))
    comvisionMenu4.add_command(label="샤프닝", command=lambda: maskImage(sharpening))
    comvisionMenu4.add_command(label="가우시안 필터링", command=lambda: maskImage(gaussian))
    comvisionMenu4.add_command(label="고주파", command=lambda: maskImage(hpf, True))
    comvisionMenu4.add_command(label="저주파", command=lambda: maskImage(lpf))
    comvisionMenu4.add_separator()
    comvisionMenu4.add_command(label="단순 경계선 검출", command=homogenOpImage)
    comvisionMenu4.add_command(label="로버츠", command=lambda: firstOrderDiff("roberts"))
    comvisionMenu4.add_command(label="프리윗", command=lambda: firstOrderDiff("prewitt"))
    comvisionMenu4.add_command(label="소벨", command=lambda: firstOrderDiff("sobel"))
    comvisionMenu4.add_command(label="라플라시안", command=secondOrderDiff)

    comVisionMenu5 = Menu(mainMenu)
    mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
    comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysql)
    comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysql)
    comVisionMenu5.add_separator()
    comVisionMenu5.add_command(label="CSV 열기", command=openCSV)
    comVisionMenu5.add_command(label="CSV로 저장", command=saveCSV)
    comVisionMenu5.add_separator()
    comVisionMenu5.add_command(label="Excel 열기", command=openExcel)
    comVisionMenu5.add_command(label="Excel로 저장", command=saveExcel)
    comVisionMenu5.add_command(label="Excel art로 저장", command=saveExcelArt)

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
