## 그림판 만들기 ##
from tkinter import *
from tkinter.colorchooser import *
from tkinter.simpledialog import *
import random

## 함수 선언 부분 ##
def mouseClick(event) :
    global x1, y1, x2, y2
    x1 = event.x
    y1 = event.y

def mouseDrop(event) :
    global x1, y1, x2, y2, penWidth, penColor
    x2 = event.x
    y2 = event.y
    canvas.create_line(x1, y1, x2, y2, width = penWidth, fill = penColor)

def getColor() :
    global penColor
    color = askcolor()
    penColor = color[1]

def getWidth() :
    global penWidth
    penWidth = askinteger("선 두께", "선 두께(1~10)를 입력하세요", minvalue = 1, maxvalue = 10)

def drawLine() :
    global x1, y1, x2, y2, penWidth, penColor
    x1, y1, x2, y2 = getRandomPoint(), getRandomPoint(), getRandomPoint(), getRandomPoint()
    canvas.create_line(x1, y1,x2, y2, width=penWidth, fill=penColor)

def getRandomPoint() :
    return random.randint(0, 300)

def drawOval() :
    global x1, y1, x2, y2, penWidth, penColor
    x1, y1, x2, y2 = getRandomPoint(), getRandomPoint(), getRandomPoint(), getRandomPoint()
    canvas.create_oval(x1, y1,x2, y2, fill = penColor, outline = penColor, width = penWidth)

## 전역 변수 선언 부분 ##
window = None
canvas = None
x1, y1, x2, y2 = None, None, None, None
penColor = "black"
penWidth = 5

## 메인 코드 부분 ##
if __name__ == '__main__':
    window = Tk()
    window.title("그림판 (ver 0.01)")
    canvas = Canvas(window, height = 300, width = 300)
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.pack()

    mainMenu = Menu(window)
    window.config(menu = mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "설정", menu = fileMenu)
    fileMenu.add_command(label = "선 색상 선택", command = getColor)
    fileMenu.add_separator()
    fileMenu.add_command(label = "선 두께 설정", command = getWidth)

    figureMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "도형", menu = figureMenu)
    figureMenu.add_command(label = "선", command = drawLine)
    figureMenu.add_command(label = "원", command = drawOval)

    window.mainloop()