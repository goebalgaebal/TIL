from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *

## 전역변수 선언부 ##
selectStr = None
textPanel = None
filename = None
window, label = None

## 함수 선언부 ##
def openFile() :
    global filename, textPanel, window
    filename = askopenfilename(parent=window,
                               filetypes=(("텍스트 파일", "*.txt;*.ini;*.py"), ("모든 파일", "*.*")))

    with open(filename, 'r') as inputFp : # with ~ as 문을 사용하면 close()함수를 사용하지 않아도 된다
        strList = inputFp.readlines()
        totStr = ''.join(strList)

        textPanel.delete(1.0, END)
        textPanel.insert(END, totStr)

        label.configure(text="선택한 파일 이름 : " + str(filename).split("/")[-1])

def saveFile():
    global filename, textPanel
    with open(filename, 'w') as wirtFp :
        wirtFp.writelines(textPanel.get("1.0",END)[:-1])
    print("저장 완료")

def change() : # 특정 문자열을 찾아서 새 문자열로 바꿈
    global textPanel
    oldStr = askstring("기존 문자", "바꾸고자하는 문자열을 입력해주세요")
    newStr = askstring("새 문자", "새 문자열을 입력해주세요")
    memoStr = textPanel.get("1.0", END) # textPanel의 전체 문자열을 가져옴

    # replace(old, new, [count]) → replace("찾을값", "바꿀값", [바꿀횟수])
    # 좌측부터 변경
    # count를 명시하지 않으면 전체를 바꿈
    memoStr = memoStr.replace(oldStr, newStr)
    print(memoStr)
    textPanel.delete("1.0", END)  # 1행 0열 ~ 끝
    textPanel.insert(END, memoStr)

def paste() :
    global selectStr, textPanel
    cur = textPanel.index(INSERT) # 현재 cursor의 위치를 받아옴
    textPanel.insert(cur, selectStr)

def copy() :
    global selectStr, textPanel
    selectStr = textPanel.selection_get() # 현재 선택한 block의 문자열을 가져옴

## 메인 코드 ##
if __name__ == '__main__':
    window = Tk()
    window.title("메모장 (ver 0.01)")
    window.geometry("500x320")
    window.resizable(width = True, height = True)

    #메뉴 생성
    mainMenu = Menu(window)
    window.config(menu = mainMenu)

    fileMenu = Menu(mainMenu)
    editMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "파일", menu = fileMenu)
    mainMenu.add_cascade(label = "편집", menu = editMenu)

    fileMenu.add_cascade(label = "열기", command = openFile)
    fileMenu.add_cascade(label = "저장", command = saveFile)

    editMenu.add_command(label = "바꾸기", command = change)
    editMenu.add_command(label = "복사", command = copy)
    editMenu.add_command(label = "붙여넣기", command = paste)

    label = Label(window, text = "[파일] → [열기] 에서 파일을 선택해주세요")
    label.pack()

    #text 위젯 생성
    textPanel = Text(window)
    textPanel.pack(expand=1, anchor=CENTER)
    window.mainloop()
