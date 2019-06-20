'''
다음 실행 예시처럼 교환할 돈을 입력받아서, 최소한의 동전의 개수로 교환해 주는 파이썬 코드를 작성하시오.
예시)
바꿀 돈 -->7777
500원: 15 , 100원: 2 , 50원: 1 , 10원 2 , 나머지: 7
'''
from tkinter.simpledialog import *

## 전역 변수 ##
OUTSIZE = 4
PADSIZE = 5

window = None # Root Frame
inputChange = None # 돈을 입력하는 Entry
moneyList = ["50000", "10000", "5000", "1000", "500", "100", "50", "10", "나머지"]
labelList = [] # Label 객체를 담고있는 list
outEntry = [] # 지폐, 동전 개수를 출력하는 Entry객체를 담고있는 list

## 함수부 ##
def clickCalc(event = None) :
    global inputChange, moneyList, outEntry
    money = inputChange.get()
    if money == "" or not money.isdigit():
        messagebox.showinfo("Error", "잘못된 입력값을 받았습니다\n다시 확인해주세요")
        for i in range(len(moneyList)):
            outEntry[i].delete(0, END)
            outEntry[i].insert(0, 0)
        inputChange.delete(0, END)
        return

    money = int(money)
    for i in range(len(moneyList)) :
        outEntry[i].delete(0, END)
        if moneyList[i].isdigit() :
            outEntry[i].insert(0, money//int(moneyList[i]))
            money %= int(moneyList[i])
        else :
            outEntry[i].insert(0, money)

## 메인 코드부 ##
if __name__ == '__main__':
    window = Tk()
    #window.geometry("500x500")
    window.title("거스름돈 계산기 ver 0.1")
    window.resizable(height=True, width=False)

    inputFrame = tkinter.Frame(window)
    inputFrame.pack()

    label1 = Label(inputFrame, text="거스름돈 : ")
    label1.grid(row=0, column=0)

    inputChange = Entry(inputFrame, width=20)
    inputChange.grid(row=0, column=1, pady=PADSIZE, padx=PADSIZE)

    btnCalc = Button(inputFrame, text ="계산", width = 10, command=clickCalc)
    btnCalc.grid(row=0, column=2)

    outputFrame = tkinter.Frame(window)
    outputFrame.pack()

    # Label 생성
    for moneyLabel in moneyList :
        if moneyLabel.isdigit() :
            labelList.append(Label(outputFrame, text=moneyLabel + "원"))
        else:
            labelList.append(Label(outputFrame, text=moneyLabel))

    # Label 출력
    for i in range(len(labelList)) :
        if i < OUTSIZE :
            labelList[i].grid(row=1, column=i)
        else :
            labelList[i].grid(row=3, column=i - OUTSIZE)

    # Entry 생성
    for i in range(len(labelList)) :
        outEntry.append(Entry(outputFrame, textvariable=StringVar().set("0"), width=10))
        if i < OUTSIZE :
            outEntry[i].grid(row=2, column=i, pady=PADSIZE, padx=PADSIZE)
        else :
            outEntry[i].grid(row=4, column=i - OUTSIZE, pady=5, padx=5)
        outEntry[i].insert(0, 0)

    window.bind("<Return>", clickCalc)
    window.mainloop()