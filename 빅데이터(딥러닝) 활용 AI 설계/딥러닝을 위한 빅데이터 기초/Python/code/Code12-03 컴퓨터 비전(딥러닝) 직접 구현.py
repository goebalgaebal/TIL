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
    rgb2hsv()

def openImageColor() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("컬러 파일", "*.jpg; *.png; *.bmp; *.tif"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return

    loadImageColor(filename)
    equlImageColor()
    displayImageColor()

def displayImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None:  # 예전에 실행한 적이 있다.
        canvas.destroy()
    VIEW_X = outW;  VIEW_Y = outH;  step = 1

    window.geometry(str(int(VIEW_Y * 1.2)) + 'x' + str(int(VIEW_X * 1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, step):
        tmpStr = ''
        for k in numpy.arange(0, outW, step):
            i = int(i); k = int(k)
            # r, g, b = outImage[k, i]
            r, g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r, g, b)
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

    saveFp = asksaveasfile(parent=window, mode='wb',
                          defaultextension='*.jpg', filetypes=(("JPG 파일", "*.jpg"), ("모든 파일", "*.*")))

    if saveFp == "" and saveFp == None :
        return
    # outImage.save(saveFp.name)
    pass
    print("SAVE COMPLETE")

def equlImageColor() :
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

def zoomOutImage2() :
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

def zoomInImage2():
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

def stretchImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW

    ## 메모리 확보
    outImage = []
    for i in range(3):
        outImage.append(malloc(outH, outW))

    maxVal = minVal = inImage[0][0]

    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]

    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = int(((inImage[i][k] - minVal) / (maxVal - minVal)) * 255)

    displayImageColor()

def histoEqualizeImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if inImage == None:
        return

    # 히스토그램 균일화는 영상의 밝기값에만 적용가능하고 컬러정보는 필요없다
    # 컬러영상을 다룰때는 YUV컬러 공간을 이용한다 Y - 밝기, U/V - 컬러
    # 입력영상을 YUV로 바꾸고 Y채널을 균일화 시킨뒤 다른 채널과 합한 결과를 출력
    pass

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

def rgb2hsv() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, photoRGB
    photoRGB = np.array(photoRGB).astype(np.float64)
    HSV = np.array(photoRGB).astype(np.float64)
    print(photoRGB.shape)
    width, height = photoRGB.shape[:2]
    print(width, height)


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
    global panYN
    panYN = True
    canvas.configure(cursor='mouse')

def mouseClickColor(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, panYN
    if panYN == False:
        return
    sx = event.x;   sy = event.y # 마우스 click 시작점

def mouseDropColor(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, panYN
    if panYN == False:
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
    panYN = False
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


#####################
## 전역변수 선언부 ##
#####################
R, G, B = 0, 1, 2
inImage, outImage = [], [] # 3차원 리스트(배열)
photoRGB = None # RGB값을 튜플로 가지고 있는 Image 객체
inH, inW, outH, outW = [0] * 4
window, canvas, paper = [None] * 3

imageFrame = None

#################
## 메인 코드부 ##
#################
if __name__ == '__main__':
    window = Tk()
    window.title("컴퓨터 비전 (컬러 라이브러리) ver 0.01")
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

    comvisionMenu2 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소점 처리(통계)", menu=comvisionMenu2)
    comvisionMenu2.add_command(label="이진화", command=bwImageColor)
    comvisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImage2)
    comvisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImage2)
    comvisionMenu2.add_separator()
    comvisionMenu2.add_command(label="히스토그램", command=histoImageColor)
    comvisionMenu2.add_command(label="히스토그램2", command=histoImage2Color)
    comvisionMenu2.add_separator()
    comvisionMenu2.add_command(label="명암대비", command=stretchImageColor)
    # comvisionMenu2.add_command(label="End-In 탐색", command=endInStretchImage)
    # comvisionMenu2.add_command(label="히스토그램 평활화", command=histoEqualizedImage)

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

    # comvisionMenu4 = Menu(mainMenu)
    # mainMenu.add_cascade(label="화소영역 처리", menu=comvisionMenu4)
    # comvisionMenu4.add_command(label="엠보싱", command=lambda: maskImage(emboss, True))
    # comvisionMenu4.add_command(label="블러링", command=lambda: maskImage(blurr))
    # comvisionMenu4.add_command(label="샤프닝", command=lambda: maskImage(sharpening))
    # comvisionMenu4.add_command(label="가우시안 필터링", command=lambda: maskImage(gaussian))
    # comvisionMenu4.add_command(label="고주파", command=lambda: maskImage(hpf, True))
    # comvisionMenu4.add_command(label="저주파", command=lambda: maskImage(lpf))
    # comvisionMenu4.add_separator()
    # comvisionMenu4.add_command(label="단순 경계선 검출", command=homogenOpImage)
    # comvisionMenu4.add_command(label="로버츠", command=lambda: firstOrderDiff("roberts"))
    # comvisionMenu4.add_command(label="프리윗", command=lambda: firstOrderDiff("prewitt"))
    # comvisionMenu4.add_command(label="소벨", command=lambda: firstOrderDiff("sobel"))
    # comvisionMenu4.add_command(label="라플라시안", command=secondOrderDiff)

    # comVisionMenu5 = Menu(mainMenu)
    # mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
    # comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysql)
    # comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysql)
    # comVisionMenu5.add_separator()
    # comVisionMenu5.add_command(label="CSV 열기", command=openCSV)
    # comVisionMenu5.add_command(label="CSV로 저장", command=saveCSV)
    # comVisionMenu5.add_separator()
    # comVisionMenu5.add_command(label="Excel 열기", command=openExcel)
    # comVisionMenu5.add_command(label="Excel로 저장", command=saveExcel)
    # comVisionMenu5.add_command(label="Excel art로 저장", command=saveExcelArt)

    imageFrame = tkinter.Frame(window)
    imageFrame.pack()

    status = Label(window, text = "이미지 정보 : ", bd = 1, relief = SUNKEN, anchor = W)  # 밑에 고정
    status.pack(side = BOTTOM, fill = X)

    window.mainloop()
