from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter.filedialog import *
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import matplotlib.pyplot as plt
import numpy as np

#################
## 함수 선언부 ##
#################
# 파일을 선택해서 메모리로 로딩하는 함수
def openImagePIL() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("컬러 파일", "*.jpg; *.png; *.bmp; *.tif"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return

    inImage = Image.open(filename);
    inW = inImage.width
    inH = inImage.height

    outImage = inImage.copy()
    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def displayImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None:  # 예전에 실행한 적이 있다
        canvas.destroy()
    VIEW_X = outW;  VIEW_Y = outH
    step = 1
    window.geometry(str(int(VIEW_Y * 1.2)) + 'x' + str(int(VIEW_X * 1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbImage = outImage.convert('RGB')
    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, step):
        tmpStr = ''
        for k in numpy.arange(0, outW, step):
            i = int(i);
            k = int(k)
            r, g, b = rgbImage.getpixel((k, i))
            tmpStr += ' #%02x%02x%02x' % (r, g, b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

def saveImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if outImage == None :
        return

    saveFp = asksaveasfile(parent=window, mode='wb',
                          defaultextension='*.jpg', filetypes=(("JPG 파일", "*.jpg"), ("모든 파일", "*.*")))

    if saveFp == "" and saveFp == None :
        return
    outImage.save(saveFp.name)
    print("SAVE COMPLETE")

######################
## 화소점 처리 함수 ##
######################
def addImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    value = askfloat("밝게/어둡게", "값을 입력해주세요", minvalue=-16.0, maxvalue=16.0)
    if value ==  None :
        return
    outImage = inImage.copy()
    outImage = ImageEnhance.Brightness(outImage).enhance(value)

    outW = outImage.width
    outH = outImage.height
    displayImagePIL()

def invertImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    outImage = ImageOps.invert(inImage)

    outW = outImage.width
    outH = outImage.height
    displayImagePIL()

def histoImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if inImage == None :
        return
    # histogram() RGB 각 채널의 histogram을 return
    yR = inImage.histogram()[0:256]
    yG = inImage.histogram()[256:512]
    yB = inImage.histogram()[512:768]
    x = np.arange(256)

    plt.figure(figsize=(12, 5)) # 그림(figure)의 크기. (가로,세로) 인치 단위
    plt.subplot(1, 3, 1)
    plt.title("histgram R")
    plt.bar(x, yR)

    plt.subplot(1, 3, 2)
    plt.title("histgram G")
    plt.bar(x, yG)

    plt.subplot(1, 3, 3)
    plt.title("histgram B")
    plt.bar(x, yB)

    plt.show()

def histoEqualizeImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if inImage == None:
        return

    # 히스토그램 균일화는 영상의 밝기값에만 적용가능하고 컬러정보는 필요없다
    # 컬러영상을 다룰때는 YUV컬러 공간을 이용한다 Y - 밝기, U/V - 컬러
    # 입력영상을 YUV로 바꾸고 Y채널을 균일화 시킨뒤 다른 채널과 합한 결과를 출력
    pass

#########################
## 화소 영역 처리 함수 ##
#########################
def filterImagePIL(filter) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outImage = inImage.copy()

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
    displayImagePIL()

######################
## 기하학 처리 함수 ##
######################
def upDownImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outImage = inImage.transpose(Image.FLIP_TOP_BOTTOM)

    outW = outImage.width
    outH = outImage.height
    displayImagePIL()

def zoomImagePIL(motion) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    scale = askinteger("확대", "배율을 입력해주세요", minvalue=1, maxvalue=8)
    outImage = inImage.copy()

    if motion == "IN":
        outImage = outImage.resize((inW*scale, inH*scale))
    else :
        outImage = outImage.resize((inW // scale, inH // scale))

    outW = outImage.width
    outH = outImage.height
    displayImagePIL()

def rotateImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if outImage == None :
        return

    angle = askinteger("회전", "각도를 입력해주세요", minvalue = 0, maxvalue = 360)
    if angle == None:
        return

    outImage = inImage.copy()
    outImage = outImage.rotate(-angle)

    outW = outImage.width
    outH = outImage.height
    displayImagePIL()





#####################
## 전역변수 선언부 ##
#####################
inImage, outImage = None, None # 객체
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
    fileMenu.add_cascade(label="열기", command=openImagePIL)
    fileMenu.add_cascade(label="저장", command=saveImagePIL)

    comvisionMenu1 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소점 처리", menu=comvisionMenu1)
    comvisionMenu1.add_command(label="밝게하기", command=addImagePIL)
    comvisionMenu1.add_command(label="어둡게하기", command=addImagePIL)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="화소값 반전", command=invertImagePIL)
    comvisionMenu1.add_separator()
    comvisionMenu1.add_command(label="히스토그램", command=histoImagePIL)
    comvisionMenu1.add_command(label="히스토그램 평활화", command=histoEqualizeImagePIL)


    comvisionMenu2 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소영역 처리", menu=comvisionMenu2)
    comvisionMenu2.add_command(label="블러링", command=lambda : filterImagePIL("BLUR"))
    comvisionMenu2.add_command(label="가우시안 블러링", command=lambda : filterImagePIL("GaussianBlur"))
    comvisionMenu2.add_command(label="엠보싱", command=lambda : filterImagePIL("EMBOSS"))
    comvisionMenu2.add_command(label="샤프닝", command=lambda : filterImagePIL("SHARPEN"))
    comvisionMenu2.add_command(label="경계선 검출", command=lambda : filterImagePIL("FIND_EDGES"))

    comvisionMenu3 = Menu(mainMenu)
    mainMenu.add_cascade(label="기하학 처리", menu=comvisionMenu3)
    comvisionMenu3.add_command(label="상하반전", command=upDownImagePIL)
    comvisionMenu3.add_separator()
    comvisionMenu3.add_command(label="확대", command=lambda : zoomImagePIL("IN"))
    comvisionMenu3.add_command(label="축소", command=lambda : zoomImagePIL("OUT"))




    imageFrame = tkinter.Frame(window)
    imageFrame.pack()

    status = Label(window, text = "이미지 정보 : ", bd = 1, relief = SUNKEN, anchor = W)  # 밑에 고정
    status.pack(side = BOTTOM, fill = X)

    window.mainloop()
