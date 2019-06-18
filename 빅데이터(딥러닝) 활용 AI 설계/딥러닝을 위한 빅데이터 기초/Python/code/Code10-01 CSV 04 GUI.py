## 트리뷰 활용
from tkinter import ttk
import csv
from tkinter.filedialog import *

def openCSV() :
    global csvList
    # 파일 선택
    filename = askopenfilename(parent=None, filetypes=(("CSV 파일", "*.csv;"), ("모든 파일", "*.*")))

    # 데이터 csvList에 읽어오기
    csvList = []
    with open(filename) as rfp:
        reader = csv.reader(rfp)
        headerList = next(reader)

        for clist in reader:
            csvList.append(clist)
        print(csvList)

    # 기존 시트 클리어 - 하위 포함
    sheet.delete(*sheet.get_children())

    # 첫번째 열 헤더 만들기
    sheet.column('#0', width=70)  # 첫 컬럼의 내부 이름
    sheet.heading('#0', text=headerList[0])

    # 두번째 이후 열 만들기
    sheet["columns"] = headerList[1:]
    for colName in headerList[1:] :
        sheet.column(colName, width = 70) # 내부이름
        sheet.heading(colName, text=colName) # 실제 이름

    # 내용 채우기
    for row in csvList :
        sheet.insert("", "end", text=row[0], values=row[1:])
    sheet.pack(expand = 1, anchor = CENTER)

def saveCSV() :
    pass

#####################
## 전역변수 선언부 ##
#####################
csvList = [] # 불러온 CSV 데이터를 저장하는 list


if __name__ == '__main__':
    window = Tk()
    window.geometry("600x500")

    # 메뉴 생성
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="CSV 처리", menu=fileMenu)
    fileMenu.add_cascade(label="CSV 열기", command=openCSV)
    fileMenu.add_cascade(label="CSV 저장", command=saveCSV)

    # treeview 생성
    sheet = ttk.Treeview(window)
    window.mainloop()