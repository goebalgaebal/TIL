from tkinter.filedialog import *
import math
import numpy as np
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

#################
## 함수 선언부 ##
#################
def changeValue(list):
    return [float(v) / 255 for v in list]

def studyCSV() :
    global csv, train_data, train_label, test_data, test_label, clf

    # 0. 훈련데이터, 테스트데이터 준비
    filename = askopenfilename(parent=window,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == None or filename == "":
        return
    csv = pd.read_csv(filename)
    train_data = csv.iloc[:, 1:].values
    train_data = list(map(changeValue, train_data))
    train_label = csv.iloc[:, 0].values

    # 1. Classifire 생성(선택) --> 머신러닝 알고리즘 선택
    clf = svm.SVC(gamma="auto")

    # 2. 데이터로 학습 시키기
    clf.fit(train_data, train_label)
    status.configure(text="TRAIN COMPLETE")

def studyDump() :
    global csv, train_data, train_label, test_data, test_label, clf
    filename = askopenfilename(parent=window,
                                filetypes=(("덤프 파일", "*.dmp;"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return

    clf = joblib.load(filename)
    status.configure(text="LOAD COMPLETE")

def studySave() :
    global csv, train_data, train_label, test_data, test_label, clf
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension=".", filetypes=(("덤프 파일", "*.dmp;"), ("모든 파일", "*.*")))

    if saveFp == "" or saveFp == None:
        return

    # 학습된 모델 저장하기
    joblib.dump(clf, saveFp.name)
    status.configure(text="SAVE COMPLETE")

def studyScore():
    global csv, train_data, train_label, test_data, test_label, clf
    if clf == None :
        return

    filename = askopenfilename(parent=window,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == None or filename == "":
        return
    csv = pd.read_csv(filename)
    test_data = csv.iloc[:, 1:].values
    test_data = list(map(changeValue, test_data))
    test_label = csv.iloc[:, 0].values

    results = clf.predict(test_data)
    score = metrics.accuracy_score(results, test_label)
    status.configure(text = "정답률 : {0:.2f} %".format(score * 100))

def predictMouse() :
    global csv, train_data, train_label, test_data, test_label, clf
    global window, canvas, paper, VIEW_X, VIEW_Y
    if clf == None :
        status.configure(test = "모델을 먼저 생성하세요")
        return

    window.geometry(str(VIEW_X) + 'x' + str(VIEW_Y))
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X, bg="black")
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')
    canvas.pack(expand=1, anchor=CENTER)

    canvas.bind("<Button-3>", rightMouseClick)
    canvas.bind("<Button-1>", leftMouseClick)
    canvas.bind("<B1-Motion>", leftMouseMove)
    canvas.bind("<ButtonRelease-1>", leftMouseDrop)

def rightMouseClick() :
    pass


def leftMouseClick() :
    global leftMousePressYN
    leftMousePressYN = True

def leftMouseMove() :
    pass

def leftMouseDrop() :
    pass

#####################
## 전역변수 선언부 ##
#####################
# 머신러닝 관련 전역 변수
csv, train_data, train_label, test_data, test_label, clf = [None]*6

VIEW_X, VIEW_Y = 280, 280
window, canvas, paper = [None] * 3

leftMousePressYN = False

#################
## 메인 코드부 ##
#################
if __name__ == '__main__':
    window = Tk()
    window.title("머신러닝 툴 (MNIST) ver 0.01")
    window.geometry("500x500")
    window.resizable(width=True, height=True)

    # 메뉴 생성
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="학습", menu=fileMenu)
    fileMenu.add_cascade(label="CSV 파일로 새로 학습", command=studyCSV)
    fileMenu.add_separator()
    fileMenu.add_cascade(label="학습모델 불러오기", command=studyDump)
    fileMenu.add_cascade(label="학습모델 저장", command=studySave)
    fileMenu.add_separator()
    fileMenu.add_cascade(label="정답률", command=studyScore)

    predictMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="예측", menu=predictMenu)
    predictMenu.add_cascade(label="그림파일 불러오기", command=None)
    predictMenu.add_separator()
    predictMenu.add_cascade(label="마우스로 직접 쓰기", command=predictMouse)


    status = Label(window, text = "STATUS : ", bd = 1, relief = SUNKEN, anchor = W)
    status.pack(side = BOTTOM, fill = X)

    window.mainloop()
