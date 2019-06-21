from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter.filedialog import *
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import matplotlib.pyplot as plt
import math
import numpy as np

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

def loadImageColor(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, photoRGB
    global photo
    inImage = []

    ## 데이터를 받아오는 방법 1
    photo = Image.open(fname) # PIL 객체
    inH = photo.height; inW = photo.width

    ## 입력영상 메모리 확보 ##
    for i in range(3) :
        inImage.append(malloc(inH, inW))

    # 파일 → 메모리
    photoRGB = photo.convert("RGB")
    for i in range(inH) :
        for k in range(inW) :
            r, g, b = photoRGB.getpixel((k, i))
            inImage[R][i][k] = r;   inImage[G][i][k] = g;   inImage[B][i][k] = b

    ## 데이터를 받아오는 방법 2
    # f = Image.open(fname)
    # inImage = f.load()
    # inH = f.height;     inW = f.width
    #print(inImage[10, 10]) # (225, 174, 129) 각 픽셀의 R, G, B값
    #print(type(inImage)) # <class 'PixelAccess'>

    print("입력 크기", inH, inW)
    #rgb2hsv()

def openImageColor() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("컬러 파일", "*.jpg; *.png; *.bmp; *.tif"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return

    loadImageColor(filename)
    equalImageColor()
    displayImageColor()

def displayImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y
    if canvas != None:  # 예전에 실행한 적이 있다.
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

    # print(btnFrame.winfo_width(), VIEW_X, VIEW_Y)
    if outW < btnFrame.winfo_width():  # 버튼 프레임보다 이미지가 작은 경우
        window.geometry(
            str(int(btnFrame.winfo_width() * 1.2)) + 'x' + str(int((btnFrame.winfo_height() + VIEW_Y) * 1.2)))  # 벽
    else:
        window.geometry(str(int(VIEW_X * 1.2)) + 'x' + str(int(VIEW_Y * 1.2)))
    canvas = Canvas(imageFrame, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, step):
        tmpStr = ''
        for k in numpy.arange(0, outW, step):
            i = int(i); k = int(k)
            # r, g, b = outImage[k, i]
            #print(np.array(outImage).shape)
            # if np.array(outImage).shape[0] == 3 :
            r, g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r, g, b)
            # else :
            #     h, s, v = outImage[i][k][0], outImage[i][k][1], outImage[i][k][2]
            #     tmpStr += ' #%02x%02x%02x' % (h, s, v)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    ## 마우스 이벤트
    canvas.bind("<Button-1>", mouseClickColor)
    canvas.bind("<ButtonRelease-1>", mouseDropColor)
    canvas.pack(expand=1, anchor=CENTER)

    status.configure(text="이미지 정보 : " + str(outW) + 'x' + str(outH))

def saveImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if outImage == None :
        return

    outArray = []
    for i in range(outH) :
        tmpList = []
        for k in range(outW) :
            tup = tuple([outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]])
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), "RGB")

    saveFp = asksaveasfile(parent=window, mode='wb',
                          defaultextension=".", filetypes=(("그림 파일", "*.jpg;*.png;*.tif"), ("모든 파일", "*.*")))

    if saveFp == "" and saveFp == None :
        return
    savePhoto.save(saveFp.name)
    print("SAVE COMPLETE")

def equalImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    ## 메모리 확보
    # 방법 1
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][i][k] = inImage[RGB][i][k]

    # # 방법 2
    # outImage = inImage
    displayImageColor()

######################
## 화소점 처리 함수 ##
######################
def addImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    value = askinteger("밝게/어둡게", "값을 입력해주세요", minvalue=-255, maxvalue=255)
    if value ==  None :
        return
    outH = inH; outW = inW

    ## 메모리 확보
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if inImage[RGB][i][k] + value > 255 :
                    outImage[RGB][i][k] = 255
                elif inImage[RGB][i][k] + value < 0 :
                    outImage[RGB][i][k] = 0
                else :
                    outImage[RGB][i][k] = inImage[RGB][i][k] + value

    displayImageColor()

def revImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH;
    outW = inW

    ## 메모리 확보
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = 255 - inImage[RGB][i][k]
    displayImageColor()

def biImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    rgb2gray()

    for i in range(inH):
        for k in range(inW):
            if outImage[R][i][k] >= 255 // 2 :
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = 255
            else :
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = 0
    displayImageColor()
    print("이진화 완료")

def avgImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    inSum = []; outSum = []
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                inSum.append(inImage[RGB][i][k])
                outSum.append(outImage[RGB][i][k])
    inAvg = int(np.array(inSum).mean())
    outAvg = int(np.array(outSum).mean())

    messagebox.showinfo("Average",
                        "입력 영상의 평균 : %d\n출력 영상의 평균 : %d" % (inAvg, outAvg))
    print("평균 출력 완료")

############################
## 화소점 처리(통계) 함수 ##
############################
def bwImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    rgb2gray()

    avg = int(np.array(outImage[R]).mean())

    for i in range(inH):
        for k in range(inW):
            if outImage[R][i][k] >= avg :
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = 255
            else :
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = 0
    displayImageColor()
    print("이진화 완료")

def zoomOutImage2Color() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    scale = askinteger("축소", "배율을 입력해주세요", minvalue=2, maxvalue=8)

    outH = inH // scale;    outW = inW // scale

    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    for RGB in range(3) :
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i // scale][k // scale] += inImage[RGB][i][k]

    for RGB in range(3) :
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] //= (scale * scale)
    displayImageColor()

def zoomInImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    scale = askinteger("축소", "배율을 입력해주세요", minvalue=2, maxvalue=4)

    outH = inH * scale; outW = inW * scale

    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    rH, rW, iH, iW = [0] * 4  # 실수 위치 및 정수 위치
    x, y = 0, 0  # 실수와 정수의 차이값 = 가중치
    C1, C2, C3, C4 = [0] * 4  # 결정할 위치(N)의 상하좌우 픽셀

    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                rH = i / scale; rW = k / scale
                iH = int(rH);   iW = int(rW)
                x = rW - iW;    y = rH - iH
                if 0 <= iH < inH - 1 and 0 <= iW < inW - 1:
                    C1 = inImage[RGB][iH][iW]
                    C2 = inImage[RGB][iH][iW + 1]
                    C3 = inImage[RGB][iH + 1][iW + 1]
                    C4 = inImage[RGB][iH + 1][iW]
                    newValue = C1 * (1 - y) * (1 - x) + C2 * (1 - y) * x + C3 * y * x + C4 * y * (1 - x)
                    outImage[RGB][i][k] = int(newValue)
    displayImageColor()

def histoImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if inImage == None :
        return

    x = np.arange(256)
    inCountList = [[0] * 256 for _ in range(3)]
    outCountList = [[0] * 256 for _ in range(3)]

    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                inCountList[RGB][inImage[RGB][i][k]] += 1
                outCountList[RGB][outImage[RGB][i][k]] += 1

    plt.figure(figsize=(12, 5)) # 그림(figure)의 크기. (가로,세로) 인치 단위
    plt.subplot(1, 2, 1)
    plt.title("inImage histgram RGB")
    plt.plot(x, inCountList[R], 'r', label = "R")
    plt.plot(x, inCountList[G], 'g', label="G")
    plt.plot(x, inCountList[B], 'b', label="B")

    plt.subplot(1, 2, 2)
    plt.title("outImage histgram RGB")
    plt.plot(x, outCountList[R], 'r', label="R")
    plt.plot(x, outCountList[G], 'g', label="G")
    plt.plot(x, outCountList[B], 'b', label="B")

    plt.show()

def histoImage2Color() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outCountList = [[0] * 256 for _ in range(3)]
    normalCountList = [[0] * 256 for _ in range(3)]

    # 빈도수 계산
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                outCountList[RGB][outImage[RGB][i][k]] += 1
        maxVal = max(outCountList[RGB]);    minVal = min(outCountList[RGB])
        High = 256
        # 정규화 = (카운트값 - 최소값) * High / (최대값 - 최소값)
        for i in range(len(outCountList[RGB])):
            normalCountList[RGB][i] = (outCountList[RGB][i] - minVal) * High / (maxVal - minVal)

    ## 서브 윈도창 생성 후 출력
    subWindow = Toplevel(window)
    subWindow.geometry('%dx%d' % (256 * 3, 256))
    subCanvas = Canvas(subWindow, width=256 * 3, height=256)
    subPaper = PhotoImage(width=256 * 3, height=256)
    subCanvas.create_image((256 * 3 // 2, 256 // 2), image=subPaper, state='normal')

    for RGB in range(3):
        for i in range(len(normalCountList[RGB])):
            for k in range(int(normalCountList[RGB][i])):
                if RGB == R:
                    subPaper.put('#A00000', (256 * RGB + i, 255 - k))
                elif RGB == G:
                    subPaper.put('#00A000', (256 * RGB + i, 255 - k))
                elif RGB == B:
                    subPaper.put('#0000A0', (256 * RGB + i, 255 - k))
    subCanvas.pack(expand=1, anchor=CENTER)
    subWindow.mainloop()

# 수정 필요
def stretchImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global inImageHSV
    if inImage == None:
        return

    # 히스토그램 균일화는 영상의 밝기값에만 적용가능하고 컬러정보는 필요없다
    rgb2hsvColorsys()

    maxVal = inImageHSV[2][0][0]
    minVal = inImageHSV[2][0][0]

    for i in range(inH):
        for k in range(inW):
            inImageHSV[2][i][k] = inImageHSV[2][i][k] * 255

    for i in range(inH):
        for k in range(inW):
            if inImageHSV[2][i][k] < minVal:
                minVal = inImageHSV[2][i][k]
            elif inImageHSV[2][i][k] > maxVal:
                maxVal = inImageHSV[2][i][k]
    print(minVal, maxVal)
    for i in range(inH):
        for k in range(inW):
            inImageHSV[2][i][k] = ((inImage[2][i][k] - minVal) / (maxVal - minVal)) * 255

    # HSV → RGB
    for i in range(outH):
        for k in range(outW):
            h, s, v = inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k]
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)
    displayImageColor()

# 수정 필요
def histoEqualizedImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global inImageHSV
    if inImage == None:
        return

    rgb2hsvColorsys()

    for i in range(inH):
        for k in range(inW):
            inImageHSV[2][i][k] = int(inImageHSV[2][i][k] * 255)

    ## 1. 히스토그램 생성
    histo = [0] * 256;  sumHisto = [0] * 256;   normalHisto = [0] * 256

    for i in range(inH):
        for k in range(inW):
            histo[inImageHSV[2][i][k]] += 1

    ## 2. 누적 빈도 수 계산
    sValue = 0
    for i in range(len(histo)):
        sValue += histo[i]
        sumHisto[i] = sValue

    ## 3. 누적 빈도수 정규화
    normalHisto = list(map(lambda x: int(x / (inW * inH) * 255), sumHisto))

    for i in range(inH):
        for k in range(inW):
            inImageHSV[2][i][k] = normalHisto[inImageHSV[2][i][k]]

    # HSV → RGB
    for i in range(outH):
        for k in range(outW):
            h, s, v = inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k]
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)
    displayImageColor()

def paraImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH;
    outW = inW

    ## 메모리 확보
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    LUT = [0 for _ in range(256)]
    for input in range(256):
        LUT[input] = int(255 - 255 * math.pow(input / 128 - 1, 2))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = LUT[inImage[RGB][i][k]]
    displayImageColor()

def morphImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW;

    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                                filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename2 == '' or filename2 == None:
        return
    inImage2 = []
    photo2 = Image.open(filename2)
    inW2 = photo2.width;    inH2 = photo2.height

    ## 메모리 확보
    for _ in range(3):
        inImage2.append(malloc(inH2, inW2))

    photoRGB2 = photo2.convert('RGB')
    for i in range(inH2):
        for k in range(inW2):
            r, g, b = photoRGB2.getpixel((k, i))
            inImage2[R][i][k] = r;  inImage2[G][i][k] = g;  inImage2[B][i][k] = b

    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    import threading
    import time
    def morpFunc():
        w1 = 1;
        w2 = 0
        for _ in range(20):
            for RGB in range(3):
                for i in range(inH):
                    for k in range(inW):
                        newValue = int(inImage[RGB][i][k] * w1 + inImage2[RGB][i][k] * w2)
                        if newValue > 255:
                            newValue = 255
                        elif newValue < 0:
                            newValue = 0
                        outImage[RGB][i][k] = newValue
            displayImageColor()
            w1 -= 0.05;
            w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()
    print("모핑 완료")

def addSvaluePillow():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo

    value = askfloat("", "0 ~ 1 ~ 10의 값을 입력해주세요")

    photo2 = photo.copy()
    photo2 = ImageEnhance.Color(photo2)
    photo2 = photo2.enhance(value)

    outH = inH; outW = inW
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    for i in range(outH):
        for k in range(outW):
            r, g, b = photo2.getpixel((k, i))
            outImage[R][i][k] = r;  outImage[G][i][k] = g;  outImage[B][i][k] = b
    displayImageColor()
    print("채도조절Pillow 처리 완료")

def addSvalueHSV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 입력 RGB --> 입력 HSV
    # 메모리 확보
    inImageHSV = []
    for i in range(3):
        inImageHSV.append(malloc(outH, outW))

    # RGB → HSV
    for i in range(inH):
        for k in range(inW):
            r, g, b = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] = h, s, v

    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    value = askfloat("", "-255 ~ 255의 값을 입력해주세요") # -255 ~ 255
    value /= 255

    # HSV → RGB
    for i in range(outH):
        for k in range(outW):
            newS = inImageHSV[1][i][k] + value
            if newS < 0 :
                newS = 0
            elif newS > 1.0 :
                newS = 1.0
            h, s, v = inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] * 255
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)
    displayImageColor()
    print("채도조절HSV 처리 완료")

def rgb2gray():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    ## 메모리 확보
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    for i in range(inH):
        for k in range(inW):
            gray = int(0.2989 * inImage[R][i][k] + 0.5870 * inImage[G][i][k] + 0.1140 * inImage[B][i][k])
            #gray = int((inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]) // 3)
            if gray > 255 :
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = 255
            elif gray < 0 :
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = 0
            else :
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = gray
    #displayImageColor()

def rgb2hsv() : # 구현 중
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, photoRGB
    photoRGB = np.array(photoRGB).astype(np.float64)
    HSV = np.array(photoRGB).astype(np.float64)
    print(photoRGB.shape)
    width, height = photoRGB.shape[:2]
    print(width, height)

    for i in range(width):
        for j in range(height):

            var_R = photoRGB[i, j, 0] / 255.0
            var_G = photoRGB[i, j, 1] / 255.0
            var_B = photoRGB[i, j, 2] / 255.0

            C_Min = min(var_R, var_G, var_B)
            C_Max = max(var_R, var_G, var_B)
            change = C_Max - C_Min

            V = C_Max
            if C_Max == 0:
                S = 0
            else:
                S = change / C_Max

            if change == 0:
                H = 0
            else:
                if var_R == C_Max:
                    H = 60 * (((var_R - var_B) / change) % 6)
                elif var_G == C_Max:
                    H = 60 * (((var_B - var_R) / change) + 2)
                elif var_B == C_Max:
                    H = 60 * (((var_R - var_B) / change) + 4)

            HSV[i, j, 0] = H
            HSV[i, j, 1] = S
            HSV[i, j, 2] = V
    outImage = HSV.astype(np.uint8)
    displayImageColor()

def rgb2hsvColorsys() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global inImageHSV
    ## 입력 RGB --> 입력 HSV
    # 메모리 확보
    inImageHSV = []
    for i in range(3):
        inImageHSV.append(malloc(outH, outW))

    # RGB → HSV
    for i in range(inH):
        for k in range(inW):
            r, g, b = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] = h, s, v

#########################
## 화소 영역 처리 함수 ##
#########################
def filterImagePIL(filter) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    ## 메모리 확보
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    if filter == "BLUR" :
        outImage = outImage.filter(ImageFilter.BLUR)
    elif filter == "GaussianBlur" :
        outImage = outImage.filter(ImageFilter.GaussianBlur(3))
    elif filter == "EMBOSS" :
        outImage = outImage.filter(ImageFilter.EMBOSS)
    elif filter == "SHARPEN" :
        outImage = outImage.filter(ImageFilter.SHARPEN)
    elif filter == "FIND_EDGES" :
        outImage = outImage.filter(ImageFilter.FIND_EDGES)

    outW = outImage.width
    outH = outImage.height
    displayImageColor()

######################
## 기하학 처리 함수 ##
######################
def upDownImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    outH = inH; outW = inW
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    for RGB in range(3) :
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][inH - i - 1][k] = inImage[RGB][i][k]

    displayImageColor()

def moveImageColor():
    global penYN
    penYN = True
    canvas.configure(cursor='mouse')

def mouseClickColor(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, penYN
    if penYN == False:
        return
    sx = event.x;   sy = event.y # 마우스 click 시작점

def mouseDropColor(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, penYN
    if penYN == False:
        return
    ex = event.x;   ey = event.y # 마우스 click 끝점

    outH = inH; outW = inW

    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    mx = sx - ex;   my = sy - ey
    print(inH, inW)
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if 0 <= i - my < outW and 0 <= k - mx < outH:
                    outImage[RGB][i - my][k - mx] = inImage[RGB][i][k]
                print(i - my, k - mx)
    penYN = False
    displayImageColor()

def zoomOutImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "배율을 입력해주세요", minvalue=2, maxvalue=16)

    outH = inH//scale;  outW = inW//scale;

    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                outImage[RGB][i][k] = inImage[RGB][i*scale][k*scale]
    displayImageColor()

def zoomInImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "배율을 입력해주세요", minvalue=2, maxvalue=8)

    outH = inH * scale; outW = inW * scale;

    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] = inImage[RGB][i // scale][k // scale]
    displayImageColor()

def rotateImageColor(val = "") :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    angle = askinteger("회전", "각도를 입력해주세요", minvalue = 1, maxvalue = 360)
    radian = angle * math.pi / 180
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                xs = i; ys = k
                xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
                yd = int(math.sin(radian) * xs + math.cos(radian) * ys)

                if 0 <= xd < inH and 0 <= yd < inW :
                    outImage[RGB][xd][yd] = inImage[RGB][i][k]
    displayImageColor()

def rotateImage2Color() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    angle = askinteger("회전", "각도를 입력해주세요", minvalue = -360, maxvalue = 360)
    radian = angle * math.pi / 180
    xc, yc = outW // 2, outH // 2
    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                xs = i; ys = k
                xd = int(xc + math.cos(radian) * (xs - xc) - math.sin(radian) * (ys - yc))
                yd = int(yc + math.sin(radian) * (xs - xc) + math.cos(radian) * (ys - yc))

                if 0 <= xd < outH and 0 <= yd < outW :
                    outImage[RGB][xs][ys] = inImage[RGB][xd][yd]
                else :
                    outImage[RGB][xs][ys] = 255
    displayImageColor()

####################
## 화소 영역 처리 ##
####################
def embossImageRGB() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    ## 컴퓨터 비전 알고리즘 ##
    MSIZE = 3
    mask = [[-1, 0, 0],
            [ 0, 0, 0],
            [ 0, 0, 1]]

    ## 임시 입력 영상 메모리 확보
    # tmpInImage, tmpOutUmage = [] * 2 # 메모리 공유
    tmpInImage, tmpOutUmage = [] , []
    for i in range(3):
        tmpInImage.append(malloc(inH + MSIZE - 1, inW + MSIZE -1, 127))
        tmpOutUmage.append(malloc(outH, outW))

    ## 원 입력 → 임시 입력
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                tmpInImage[RGB][i + MSIZE // 2][k + MSIZE // 2] = inImage[RGB][i][k]

    ## 회선 연산
    for RGB in range(3) :
        for i in range(MSIZE // 2, inH + MSIZE // 2) :
            for k in range(MSIZE // 2, inW + MSIZE // 2) :
                # 각 점 처리
                S = 0.0
                for m in range(MSIZE) :
                    for n in range(MSIZE) :
                        S += mask[m][n] * tmpInImage[RGB][i + m - MSIZE // 2][k + n - MSIZE // 2]
                tmpOutUmage[RGB][i - MSIZE // 2][k - MSIZE // 2] = S

    ## 127 더하기
    # 마스크의 합 = 0인 마스크 → 가중치 0, 일반적으로 어두워짐, 마스크의 합 = 1인 마스크 존재
    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                tmpOutUmage[RGB][i][k] += 127

    ## 임시 출력 → 원 출력 영상
    for RGB in range(3) :
        for i in range(outH):
            for k in range(outW):
                value = tmpOutUmage[RGB][i][k]
                if value > 255 :
                    value = 255
                elif value < 0 :
                    value = 0
                outImage[RGB][i][k] = int(value)

    displayImageColor()
    print("엠보싱 처리 완료")

def embossImagePillow() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo

    photo2 = photo.copy()
    photo2 = photo2.filter(ImageFilter.EMBOSS)

    outH = inH; outW = inW
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    for i in range(outH):
        for k in range(outW):
            r, g, b = photo2.getpixel((k, i))
            outImage[R][i][k] = r;  outImage[G][i][k] = g;  outImage[B][i][k] = b
    displayImageColor()
    print("엠보싱Pillow 처리 완료")

import colorsys
def embossImageHSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey
    global inImageHSV
    ## 입력 RGB --> 입력 HSV
    rgb2hsvColorsys()

    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ## 컴퓨터 비전 알고리즘 ##
    MSIZE = 3
    mask = [[-1, 0, 0],
            [ 0, 0, 0],
            [ 0, 0, 1]]

    ## 임시 입력 영상 메모리 확보
    tmpInImageV, tmpOutImageV = [] , []
    tmpInImageV = malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127)
    tmpOutImageV = malloc(outH, outW)

    ## 원 입력 → 임시 입력
    for i in range(inH) :
        for k in range(inW) :
            tmpInImageV[i + MSIZE // 2][k + MSIZE // 2] = inImageHSV[2][i][k]

    ## 회선 연산
    for i in range(MSIZE // 2, inH + MSIZE // 2) :
        for k in range(MSIZE // 2, inW + MSIZE // 2) :
            # 각 점 처리
            S = 0.0
            for m in range(MSIZE) :
                for n in range(MSIZE) :
                    S += mask[m][n] * tmpInImageV[i + m - MSIZE // 2][k + n - MSIZE // 2]
            tmpOutImageV[i - MSIZE // 2][k - MSIZE // 2] = S * 255

    ## 127 더하기
    for i in range(outH):
        for k in range(outW):
            tmpOutImageV[i][k] += 127
            if tmpOutImageV[i][k] > 255 :
                tmpOutImageV[i][k] = 255
            elif tmpOutImageV[i][k] < 0 :
                tmpOutImageV[i][k] = 0

    # HSV → RGB
    for i in range(outH):
        for k in range(outW):
            h, s, v = inImageHSV[0][i][k], inImageHSV[1][i][k], tmpOutImageV[i][k]
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            if penEmbossYN == True :
                if sx <= k <= ex and sy <= i <= ey :  # 범위에 포함되면
                    outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)
                else:
                    outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            else :
                outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)
    displayImageColor()
    print("엠보싱HSV 처리 완료")

def __embossImageHSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    ## 이벤트 바인드
    canvas.bind("<Button-3>", rightMouseClick_embossImageHSV)
    canvas.bind("<Button-1>", leftMouseClick)
    canvas.bind("<B1-Motion>", leftMouseMove)
    canvas.bind("<ButtonRelease-1>", leftMouseDrop_embossImageHSV)
    canvas.configure(cursor="mouse")

    print("엠보싱HSV영역선택 바인드")

def rightMouseClick_embossImageHSV(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey

    sx = 0; sy = 0; ex = inW - 1;   ey = inH - 1 # 이미지 시작 좌표, 마지막 좌표

    embossImageHSV()

    canvas.unbind("<Button-3>")
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def leftMouseClick(event) :
    global sx, sy, ex, ey
    sx = event.x;   sy = event.y
    print("leftMouseClick", sx, sy)

boxLine = None
def leftMouseMove(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, boxLine
    ex = event.x;   ey = event.y

    if not boxLine :
        pass
    else :
        canvas.delete(boxLine)
    boxLine = canvas.create_rectangle(sx, sy, ex, ey, fill = None)

def leftMouseDrop_embossImageHSV(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, penEmbossYN

    ex = event.x;    ey = event.y

    penEmbossYN = True
    embossImageHSV()
    penEmbossYN = False

    canvas.unbind("<Button-3>")
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def blurrImageRGB() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    ## 컴퓨터 비전 알고리즘 ##
    MSIZE = 3
    mask = [[1/9, 1/9, 1/9],
            [ 1/9, 1/9, 1/9],
            [ 1/9, 1/9, 1/9]]

    ## 임시 입력 영상 메모리 확보
    # tmpInImage, tmpOutUmage = [] * 2 # 메모리 공유
    tmpInImage, tmpOutUmage = [] , []
    for i in range(3):
        tmpInImage.append(malloc(inH + MSIZE - 1, inW + MSIZE -1, 127))
        tmpOutUmage.append(malloc(outH, outW))

    ## 원 입력 → 임시 입력
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                tmpInImage[RGB][i + MSIZE // 2][k + MSIZE // 2] = inImage[RGB][i][k]

    ## 회선 연산
    for RGB in range(3) :
        for i in range(MSIZE // 2, inH + MSIZE // 2) :
            for k in range(MSIZE // 2, inW + MSIZE // 2) :
                # 각 점 처리
                S = 0.0
                for m in range(MSIZE) :
                    for n in range(MSIZE) :
                        S += mask[m][n] * tmpInImage[RGB][i + m - MSIZE // 2][k + n - MSIZE // 2]
                tmpOutUmage[RGB][i - MSIZE // 2][k - MSIZE // 2] = S

    ## 임시 출력 → 원 출력 영상
    for RGB in range(3) :
        for i in range(outH):
            for k in range(outW):
                value = tmpOutUmage[RGB][i][k]
                if value > 255 :
                    value = 255
                elif value < 0 :
                    value = 0
                outImage[RGB][i][k] = int(value)

    displayImageColor()
    print("블러RGB 처리 완료")

def maskImageColor(mask, retouch=False):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global inImageHSV
    ## 입력 RGB --> 입력 HSV
    rgb2hsvColorsys()

    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ## 컴퓨터 비전 알고리즘 ##
    MSIZE = len(mask)

    ## 임시 입력 영상 메모리 확보
    tmpInImageV, tmpOutImageV = [], []
    tmpInImageV = malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127)
    tmpOutImageV = malloc(outH, outW)

    ## 원 입력 → 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImageV[i + MSIZE // 2][k + MSIZE // 2] = inImageHSV[2][i][k]

    ## 회선 연산
    for i in range(MSIZE // 2, inH + MSIZE // 2):
        for k in range(MSIZE // 2, inW + MSIZE // 2):
            # 각 점 처리
            S = 0.0
            for m in range(MSIZE):
                for n in range(MSIZE):
                    S += mask[m][n] * tmpInImageV[i + m - MSIZE // 2][k + n - MSIZE // 2]
            tmpOutImageV[i - MSIZE // 2][k - MSIZE // 2] = S * 255

    ## 127 더하기
    if retouch == True:
        for i in range(outH):
            for k in range(outW):
                tmpOutImageV[i][k] += 127
                if tmpOutImageV[i][k] > 255:
                    tmpOutImageV[i][k] = 255
                elif tmpOutImageV[i][k] < 0:
                    tmpOutImageV[i][k] = 0
    else :
        for i in range(outH):
            for k in range(outW):
                if tmpOutImageV[i][k] > 255:
                    tmpOutImageV[i][k] = 255
                elif tmpOutImageV[i][k] < 0:
                    tmpOutImageV[i][k] = 0

    # HSV → RGB
    for i in range(outH):
        for k in range(outW):
            h, s, v = inImageHSV[0][i][k], inImageHSV[1][i][k], tmpOutImageV[i][k]
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)
    displayImageColor()
    print("마스크 처리 완료")

#################
## 기타 입출력 ##
#################
###################
## MySQL DB 연동 ##
###################
import pymysql
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

## 임시 경로에 outImage를 저장
def saveTempImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    import tempfile;    import struct;  import random
    saveFp = tempfile.gettempdir() + "/" + str(random.randint(10000, 99999)) + ".png"
    if saveFp == '' or saveFp == None :
        return
    print(saveFp)
    saveFp = open(saveFp, mode='wb')
    for i in range(outH) :
        for k in range(outW) :
            saveFp.write(struct.pack('B', outImage[R][i][k]))
            #  #%02x%02x%02x' % (r, g, b)
    saveFp.close()
    return saveFp

def saveMysql() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global IP_ADDR, USER_NAME, USER_PASS, DB_NAME, CHAR_SET
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

    #os.remove(fullname)
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
def loadCSVColor(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = 0
    fp = open(fname, "r")
    for _ in fp :
        fsize += 1
    inH = inW = int(math.sqrt(fsize))
    fp.close()

    ## 입력영상 메모리 확보 ##
    inImage = []
    for i in range(3):
        inImage.append(malloc(inH, inW))

    # 파일 → 메모리
    with open(fname, "r") as rFp:
        for row_list in rFp :
            row, col, r, g, b = list(map(int, row_list.strip().split(",")))
            inImage[R][row][col], inImage[G][row][col], inImage[B][row][col] = r, g, b

def openCSVColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                               filetypes=(("CSV 파일", "*.csv;"), ("모든 파일", "*.*")))
    loadCSVColor(filename)
    equalImageColor()

import csv
def saveCSVColor() :
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
                row_list = [i, k, outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]]
                csvWriter.writerow(row_list)
    print("CSV save OK")

############################
## EXCEL 데이터 관련 함수 ##
############################
import xlrd
def openExcelColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=None, filetypes=(("엑셀 파일", "*.xls;*.xlsx"),
                                                       ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return

    # 헤더는 존재하지 않는다고 가정
    # sheet는 3개(R, G, B)라고 가정
    workbook = xlrd.open_workbook(filename)
    ws = workbook.sheets()[0]
    inH, inW = ws.nrows, ws.ncols
    for i in range(3):
        inImage.append(malloc(inH, inW))

    for RGB in range(3) :
        ws = workbook.sheets()[RGB]
        print("LOAD", ws.name, RGB, "Sheet")
        for i in range(inH) :
            for k in range(inW) :
                inImage[RGB][i][k] = int(ws.cell_value(i, k))
    equalImageColor()

import xlwt
def saveExcelColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode="wb",
                           defaultextension="*.xls",
                           filetypes=(("XLS 파일", "*.xls;"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return

    xlsName = saveFp.name
    sheetName = os.path.basename(filename)# sheet하나에 데이터가 들어있다고 가정

    wb = xlwt.Workbook() # 파일 자체 준비
    for RGB in range(3) :
        ws = wb.add_sheet(str(RGB))  # sheet 생성
        for i in range(outH) :
            for k in range(outW) :
                ws.write(i, k, outImage[RGB][i][k])
    wb.save(xlsName) # xlsName으로 파일 저장
    print("Excel save OK")

import xlsxwriter
def saveExcelArtColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode="wb",
                           defaultextension="*.xls",
                           filetypes=(("XLS 파일", "*.xls;"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None or filename == None or filename == "" :
        return

    xlsName = saveFp.name
    sheetName = os.path.basename(filename)# sheet하나에 데이터가 들어감

    wb = xlsxwriter.Workbook(xlsName) # xlsName의 파일 자체 준비
    ws = wb.add_worksheet(sheetName) # sheet 생성

    ws.set_column(0, outW -1, 1.0) # 0부터 outW-1까지 약 0.34
    for i in range(outH) :
        ws.set_row(i, 9.5) # i번재 행을 약 0.35

    for i in range(outH) :
        for k in range(outW) :
            # data 값으로 셀의 배경색을 조절 #000000 ~ #FFFFFF
            hexStr = "#"
            for RGB in range(3) :
                data = outImage[RGB][i][k]
                if data > 15 :
                    hexStr += hex(data)[2:] # ox를 떼고 RGB값을 같은 값으로 넣어준다
                else :
                    hexStr += "0" + hex(data)[2:]

            # 셀의 포맷 준비
            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)

            ws.write(i, k, "", cell_format) # ""자리를 실제 들어가는 값
    wb.close() # 파일 저장
    print("Excel save OK")

#####################
## 전역변수 선언부 ##
#####################
R, G, B = 0, 1, 2
inImage, outImage = [], [] # 3차원 리스트(배열)
inImageHSV = [] # RGB → HSV 로 변환 시 필요한 변수
photoRGB = None # RGB값을 튜플로 가지고 있는 Image 객체
inH, inW, outH, outW = [0] * 4

penYN = False
penEmbossYN = False
sx, sy, ex, ey = [0] * 4

window, canvas, paper = [None] * 3
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)
btnFrame, imageFrame = None, None

BMSIZE = 5
blurr = [[1 / (BMSIZE * BMSIZE) for i in range(BMSIZE)] for k in range(BMSIZE)]


# algorithm mask
emboss = [[-1, 0, 0],
        [0, 0, 0],
        [0, 0, 1]]

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

IP_ADDR = "192.168.56.110"
USER_NAME = "root"
USER_PASS = "1234"
DB_NAME = "BigData_DB"
CHAR_SET = "utf8"

#################
## 메인 코드부 ##
#################
if __name__ == '__main__':
    window = Tk()
    window.title("컴퓨터 비전 (컬러) ver 0.01")
    window.geometry("500x500")
    window.resizable(width=True, height=True)

    # 메뉴 생성
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="파일", menu=fileMenu)
    fileMenu.add_cascade(label="열기", command=openImageColor)
    fileMenu.add_cascade(label="저장", command=saveImageColor)

    comvisionMenu1 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소점 처리", menu=comvisionMenu1)
    comvisionMenu1.add_command(label="밝게하기", command=addImageColor)
    comvisionMenu1.add_command(label="어둡게하기", command=addImageColor)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="화소값 반전", command=revImageColor)
    comvisionMenu1.add_command(label="이진화", command=biImageColor)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="입/출력 영상의 평균값", command=avgImageColor)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="파라볼라", command=paraImageColor)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="모핑", command=morphImageColor)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="채도조절 Pillow", command=addSvaluePillow)
    comvisionMenu1.add_command(label="채도조절 HSV", command=addSvalueHSV)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="HSV 테스트", command=rgb2hsv)

    comvisionMenu2 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소점 처리(통계)", menu=comvisionMenu2)
    comvisionMenu2.add_command(label="이진화", command=bwImageColor)
    comvisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImage2Color)
    comvisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImage2Color)
    comvisionMenu2.add_separator()
    comvisionMenu2.add_command(label="히스토그램", command=histoImageColor)
    comvisionMenu2.add_command(label="히스토그램2", command=histoImage2Color)
    comvisionMenu2.add_separator()
    comvisionMenu2.add_command(label="명암대비", command=stretchImageColor)
    # comvisionMenu2.add_command(label="End-In 탐색", command=endInStretchImage)
    comvisionMenu2.add_command(label="히스토그램 평활화", command=histoEqualizedImageColor)

    comvisionMenu3 = Menu(mainMenu)
    mainMenu.add_cascade(label="기하학 처리", menu=comvisionMenu3)
    comvisionMenu3.add_command(label="상하반전", command=upDownImageColor)
    comvisionMenu3.add_separator()
    comvisionMenu3.add_command(label="이동", command=moveImageColor)
    comvisionMenu3.add_separator()
    comvisionMenu3.add_command(label="축소", command=zoomOutImageColor)
    comvisionMenu3.add_command(label="확대", command=zoomInImageColor)
    comvisionMenu3.add_separator()
    comvisionMenu3.add_command(label="회전", command=rotateImageColor)
    comvisionMenu3.add_command(label="회전2(중심, 역방향)", command=rotateImage2Color)

    comvisionMenu4 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소영역 처리", menu=comvisionMenu4)
    comvisionMenu4.add_command(label="엠보싱RGB", command=embossImageRGB)
    comvisionMenu4.add_command(label="엠보싱Pillow", command=embossImagePillow)
    # comvisionMenu4.add_command(label="엠보싱HSV", command=embossImageHSV)
    comvisionMenu4.add_command(label="엠보싱HSV", command=lambda: maskImageColor(emboss, True))
    comvisionMenu4.add_command(label="엠보싱HSV영역선택", command=__embossImageHSV)
    comvisionMenu4.add_command(label="블러링RGB", command=blurrImageRGB)
    comvisionMenu4.add_command(label="블러링HSV", command=lambda: maskImageColor(blurr))
    comvisionMenu4.add_command(label="샤프닝", command=lambda: maskImageColor(sharpening))
    comvisionMenu4.add_command(label="가우시안 필터링", command=lambda: maskImageColor(gaussian))
    comvisionMenu4.add_command(label="고주파", command=lambda: maskImageColor(hpf, True))
    comvisionMenu4.add_command(label="저주파", command=lambda: maskImageColor(lpf))
    comvisionMenu4.add_separator()
    # comvisionMenu4.add_command(label="단순 경계선 검출", command=homogenOpImage)
    # comvisionMenu4.add_command(label="로버츠", command=lambda: firstOrderDiff("roberts"))
    # comvisionMenu4.add_command(label="프리윗", command=lambda: firstOrderDiff("prewitt"))
    # comvisionMenu4.add_command(label="소벨", command=lambda: firstOrderDiff("sobel"))
    # comvisionMenu4.add_command(label="라플라시안", command=secondOrderDiff)

    comVisionMenu5 = Menu(mainMenu)
    mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
    # comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysql)
    comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysql)
    comVisionMenu5.add_separator()
    comVisionMenu5.add_command(label="CSV 열기", command=openCSVColor)
    comVisionMenu5.add_command(label="CSV로 저장", command=saveCSVColor)
    comVisionMenu5.add_separator()
    comVisionMenu5.add_command(label="Excel 열기", command=openExcelColor)
    comVisionMenu5.add_command(label="Excel로 저장", command=saveExcelColor)
    comVisionMenu5.add_command(label="Excel art로 저장", command=saveExcelArtColor)

    btnFrame = tkinter.Frame(window)
    btnFrame.pack()

    imageFrame = tkinter.Frame(window)
    imageFrame.pack()

    status = Label(window, text = "이미지 정보 : ", bd = 1, relief = SUNKEN, anchor = W)  # 밑에 고정
    status.pack(side = BOTTOM, fill = X)

    window.mainloop()
