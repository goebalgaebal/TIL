## 트리뷰 활용
from tkinter import *
from tkinter import ttk

window = Tk()
window.geometry("800x500")

sheet = ttk.Treeview(window)

# 첫번째 열 만들기
sheet.column('#0', width = 70) # 첫 컬럼의 내부 이름
sheet.heading('#0', text = '제목1')

# 두번째 이후 열 만들기
sheet["columns"] = ("A", "B", "C") # 두번째 이후 컬럼의 내부이름(내맘대로)
sheet.column("A", width = 70);  sheet.heading('A', text = "제목2")
sheet.column("A", width = 70);  sheet.heading('B', text = "제목3")
sheet.column("A", width = 70);  sheet.heading('C', text = "제목4")

# 내용 채우기
sheet.insert('', 'end', text = "1열값1", values = ('2열값1', '3열값1', '4열값1'))
sheet.insert('', 'end', text = "1열값2", values = ('2열값2', '3열값2', '4열값2'))
sheet.insert('', 'end', text = "1열값3", values = ('2열값3', '3열값3', '4열값3'))

sheet.pack()
window.mainloop()