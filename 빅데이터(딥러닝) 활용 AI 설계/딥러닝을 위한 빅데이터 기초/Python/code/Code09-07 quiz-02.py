import csv
from tkinter.filedialog import *
from tkinter import *
from tkinter import ttk

if __name__ == '__main__':
    filename = askopenfilename(parent = None, filetypes=(("CSV 파일", "*.csv;"), ("모든 파일", "*.*")))

    csvList = []
    with open(filename) as rfp :
        reader = csv.reader(rfp)
        headerList = next(reader)

        for clist in reader :
            csvList.append(clist)

    window = Tk()
    window.geometry("800x500")

    sheet = ttk.Treeview(window)
    horizontalScrollbar = ttk.Scrollbar(window, orient="horizontal", command = sheet.xview)
    horizontalScrollbar.pack(side="bottom", fill=X)

    # 첫번째 열 만들기
    sheet.column('#0', width=60)  # 첫 컬럼의 내부 이름
    sheet.heading('#0', text="INDEX")

    # 두번째 이후 열 만들기
    sheet["columns"] = tuple(headerList)  # 두번째 이후 컬럼의 내부이름(내맘대로)
    for i in range(len(sheet["columns"])):
        sheet.column(sheet["columns"][i], minwidth = 60, anchor	= "center");
        sheet.heading(sheet["columns"][i], text=sheet["columns"][i])

    # 내용 채우기
    index = 1
    for i in range(len(csvList)) :
        tmp = []
        for val in csvList[i] :
            tmp.append(val)
        sheet.insert('', 'end', text=str(index), values=tuple(tmp))
        index += 1

    sheet.pack(expand = 1, fill=BOTH)
    window.mainloop()